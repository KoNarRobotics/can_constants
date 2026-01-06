#pragma once


#include <array>
#include <memory>
#include <vector>


namespace canc {

struct CanMsg {
  uint32_t id;
  uint8_t data[64];
  uint8_t size;
  bool fdcan = false;
};


enum class CanStructureRequestState : uint8_t { NOT_REQUESTED = 0, RECEIVED = 1, INCOMPLETE = 2 };


/// @brief Class to send structures over CAN bus
///
/// **CAN Frame Data Structure:**
/// ```
/// ┌─────────────────┬────────────┬─────────────┐
/// │ Field           │ Size       │ Notes       │
/// ├─────────────────┼────────────┼─────────────┤
/// │ CAN ID          │ Variable   │ Frame ID    │
/// │ Segment Index   │ 1 byte     │ Max 256     │
/// │ Structure Data  │ 7/63 bytes | CAN/FDCAN   │
/// └─────────────────┴────────────┴─────────────┘
/// ```
///
/// @tparam T The structure type to be sent over CAN
/// @note Maximum size of a structure to be send must be less than
/// 1792 bytes for CAN2.0, or 16128 bytes for FDCAN
template <typename T, bool FdCan = false> class CanStructureSender {
  using Type = T;

public:
  CanStructureSender() {
    if constexpr(FdCan) {
      static_assert(sizeof(Type) <= 16128,
                    "CanStructureSender: Structure size exceeds maximum Extended CAN data size");
    } else {
      static_assert(sizeof(Type) <= 1792, "CanStructureSender: Structure size exceeds maximum CAN data size");
    }
  }
  ~CanStructureSender() = default;

  /// @brief Pack the structure into CAN messages
  /// @param structure The structure to be packed
  /// @return Vector of CAN messages ready to be sent
  std::vector<CanMsg> pack(uint32_t can_id, const Type &structure) {
    std::vector<CanMsg> messages;
    size_t total_size = sizeof(Type);
    size_t offset     = 0;
    size_t index      = 0;
    while(total_size > 0) {
      CanMsg msg;
      msg.id    = can_id;
      msg.fdcan = FdCan;
      msg.size  = frame_size + 1; // +1 for segment index size all the frames are -1 to fit the index data and
      uint8_t size_to_copy = (total_size > frame_size) ? frame_size : static_cast<uint8_t>(total_size);
      msg.data[0]          = static_cast<uint8_t>(index++);
      std::memcpy(msg.data + 1, reinterpret_cast<const uint8_t *>(&structure) + offset, size_to_copy);
      messages.push_back(msg);
      total_size -= size_to_copy;
      offset += size_to_copy;
    }
    return messages;
  }

  /// @brief Prepare the unpacker for a new structure
  ///
  /// This will clear the internal buffers and prepare for a new unpacking process
  void start_unpacking() {
    std::memset(_rx_buffor, 0, sizeof(Type));
    std::memset(_decoded_parts, 0, sizeof(_decoded_parts));
  }

  /// @brief This will unpack the structure from the CAN message
  /// @param msg received CAN message don't have to be in order
  ///
  /// @note This function shoule be called for each received CAN message with the correct frame ID
  /// It will also clean internal buffers when the structure is fully unpacked
  /// @return true if unpacking was finished false otherwise
  bool unpack(const CanMsg &msg) {
    size_t total_size     = sizeof(Type);
    size_t total_segments = total_size / frame_size + ((total_size % frame_size) ? 1 : 0);
    size_t segment_index  = msg.data[0];
    if(segment_index >= total_segments) {
      request_state_ = CanStructureRequestState::INCOMPLETE;
      return false;
    }
    size_t size_to_copy =
    (segment_index < total_segments - 1) ? frame_size : static_cast<size_t>(total_size - segment_index * frame_size);
    std::memcpy(_rx_buffor + segment_index * frame_size, msg.data + 1, size_to_copy);
    _decoded_parts[segment_index] = true;

    for(size_t i = 0; i < total_segments; ++i) {
      if(!_decoded_parts[i]) {
        request_state_ = CanStructureRequestState::INCOMPLETE;
        return false;
      }
    }
    _struct = *reinterpret_cast<Type *>(_rx_buffor);
    start_unpacking();
    request_state_ = CanStructureRequestState::RECEIVED;
    return true;
  }

  const Type &get_unpacked_structure() const {
    return _struct;
  }

  const CanStructureRequestState &get_request_state() const {
    return request_state_;
  }

  void reset_request_state() {
    request_state_ = CanStructureRequestState::NOT_REQUESTED;
  }

private:
  static const constexpr size_t frame_size = FdCan ? 63 : 7;
  uint8_t _rx_buffor[sizeof(Type)];
  Type _struct;
  bool _decoded_parts[sizeof(Type) / frame_size + 1]{ false };
  CanStructureRequestState request_state_{ CanStructureRequestState::NOT_REQUESTED };
};


} // namespace canc