import cantools
import os
import shutil

class can_db_builder:
  def __init__(self): 
    self.modules = {}
    self.db = None

  def add_module(self, module):
    if not hasattr(module, 'db') or not isinstance(module.db, list):
      raise ValueError(f"Module {module} must have an attribute 'db' of type list with can Messages")
    self.__check_for_collisions(module)
    self.modules[module] = module.db
    
  def db_build(self):
    db = []
    for module in self.modules:
      db += module.db
    self.db =  cantools.database.can.Database(db)
    return self.db

  def dump_file(self,file_name):
    cantools.database.dump_file(self.db, file_name)

  def __check_for_collisions(self,module):
    ids = {}
    for mod in self.modules.keys():
      for a in mod.db:
        ids[a.frame_id] = (a,mod)

    messages_to_check = module.db
    for message in messages_to_check:
      if message.frame_id in ids:
        print(f"""\033[91m 
                  Collision detected in can frame: 
                    NAME={message.name}
                    ID={message.frame_id} 
                    In file: {module.__file__}
                  Existing message: 
                    NAME={ids[message.frame_id][0].name}
                    ID={message.frame_id} 
                    From file: {ids[message.frame_id][1].__file__}
                  \033[0m
              """)
        
  def generate_C_code(self,db_file, output_dir):
    os.system(f'python3 -m cantools generate_c_source --use-float --database-name can {db_file}')
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    for file_name in ['can.dbc', 'can.h', 'can.c']:
      src_file = file_name
      dest_file = os.path.join(output_dir, file_name)
      if os.path.exists(dest_file):
        os.remove(dest_file)
      shutil.move(src_file, output_dir)

  def generate_docs(self, file_out):
    doc_lines = ["# CAN frames Documentation\n"]
    for module, messages in self.modules.items():
        doc_lines.append(f"# Module: {module.__package__.upper()}")
        for msg in messages:
          doc_lines.append(f"### Msg: {msg.name}")
          doc_lines.append(f"- { 'ID [Extended]' if msg.is_extended_frame else 'ID'} : ***{hex(msg.frame_id)}***")  
          doc_lines.append(f"- Senders: ***{', '.join(msg.senders) if msg.senders else 'Unknown'}***")
          doc_lines.append(f"- Receivers: ***{', '.join(msg.receivers) if msg.receivers else 'Unknown'}***")
          doc_lines.append(f"- DLC: {msg.length } bytes")
          
          doc_lines.append("#### Signals:")
          for signal in msg.signals:
              doc_lines.append(f"  - **{signal.name}**")
              # doc_lines.append(f"    - Start Bit: {signal.start}")
              doc_lines.append(f"    - Length: ***{signal.length}*** bits")
              # doc_lines.append(f"    - Scale: {signal.scale}, Offset: {signal.offset}")
              # doc_lines.append(f"    - Min: {signal.minimum}, Max: {signal.maximum}")
              doc_lines.append(f"    - Unit: ***{signal.unit or 'None'}***")
              doc_lines.append("")

    # Save documentation to a file
    with open(f"{file_out}", "w") as f:
        f.write("\n".join(doc_lines))