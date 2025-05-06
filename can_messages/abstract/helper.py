#
# This file is part of the CAN messages database.
# Created by Patryk Dudziński.
# Date February 18, 2025
#

import cantools
import os
import shutil

class can_db_builder:
  def __init__(self): 
    self.modules = {}
    self.db = None

  def add_module(self, module):
    """
    ### Add a module to the database builder. 
    
    The module must have an **global attribute 'db'** which is a list of can messages.
    Constructed using the abstract classes provided in the Signals.py.

    This function checks for collisions in the database.
    If a collision is detected, an error message is printed and the module is not added to the database.
    """
    if not hasattr(module, 'db') or not isinstance(module.db, list):
      raise ValueError(f"Module {module} must have an attribute 'db' of type list with can Messages")
    if not self.__check_for_collisions(module):
      self.modules[module] = module.db
      print(f"\033[92m Successfully added module \"{module.__name__.split('.')[1]}\" to the database!\033[0m")
    
  def db_build(self):
    """
    ### Build the database from the modules added to the builder.
    """
    db = []
    for module in self.modules:
      db += module.db
    self.db =  cantools.database.can.Database(db)
    return self.db

  def dump_file(self,file_name):
    """
    ### Dump the database to a file.
    The file name must end with .dbc
    """
    cantools.database.dump_file(self.db, file_name)

  def __check_for_collisions(self,module):
    ids = {}
    for mod in self.modules.keys():
      for a in mod.db:
        ids[a.frame_id] = (a,mod)
    has_collision = False
    messages_to_check = module.db
    for message in messages_to_check:
      if message.frame_id in ids:
        print(f"""\033[91m 
                  Collision detected in between existing CAN FRAME IDs!
                  The following messages have the same ID:
                  New message: 
                    NAME={message.name}
                    ID={message.frame_id} 
                    In file: {module.__file__}
                  Existing message: 
                    NAME={ids[message.frame_id][0].name}
                    ID={message.frame_id} 
                    From file: {ids[message.frame_id][1].__file__}
                    \033[93m
                  Please check the IDs of the messages in the database and correct the IDs.
                  The module \"{module.__name__.split('.')[1]}\" will not be added to the database.
                  \033[0m
              """)
        has_collision = True
    return has_collision
        
  def generate_C_code(self,db_file, output_dir,databse_name='can_messages'):
    """
    ### Generate C code from the database file.
      The file name must end with .dbc

      db_file: The database file to generate C code from.
      output_dir: The directory where the generated files will be saved.
      databse_name: The name of the database. This will be used as the prefix for the generated files.
    """
    db="can"
    os.system(f'python3 -m cantools generate_c_source --use-float --database-name {db} {db_file} 1>/dev/null 2>&1')
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    # for file_name in ['can.dbc', f'{db}.h', f'{db}.c']:
    #   src_file = file_name
    #   dest_file = os.path.join(output_dir, file_name)
    #   if os.path.exists(dest_file):
    #     os.remove(dest_file)
    #   shutil.move(src_file, output_dir)

    shutil.move( 'can.dbc', os.path.join(output_dir,f'{databse_name}.dbc'))
    shutil.move( 'can.h', os.path.join(output_dir,f'{databse_name}.h'))
    shutil.move( 'can.c', os.path.join(output_dir,f'{databse_name}.c'))
    c_file = os.path.join(output_dir,f'{databse_name}.c')
    # Modify the generated C file to replace #include "can.h" with the correct header file name
    with open(c_file, "r") as file:
      c_code = file.read()
    c_code = c_code.replace('#include "can.h"', f'#include "{databse_name}.h"')

    with open(c_file, "w") as file:
      file.write(c_code)

    print(f"\033[96m Successfully generated C code {databse_name}.h {databse_name}.c !\033[0m")

  def generate_docs(self, file_out):
    """
    ### Generate documentation from the database.
      The file name must end with .md
    """

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