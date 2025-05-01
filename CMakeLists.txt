cmake_minimum_required(VERSION 3.20)

project(can_constants VERSION 1.0 LANGUAGES C)


set(can_files
  ${PROJECT_SOURCE_DIR}/can_messages/output/can_messages.c
)

set_source_files_properties(${can_files} PROPERTIES GENERATED TRUE)


add_library(can_constants STATIC
  ${can_files}
)

# Include directories
target_include_directories(can_constants PUBLIC
  ${PROJECT_SOURCE_DIR}/can_messages/output
)
