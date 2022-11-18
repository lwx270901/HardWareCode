import os
import sys

from modules.command.command import LocalCommand
# from ..command.command import RemoteCommand



class File:
  def __init__(self):
    pass

  def __del__(self):
    pass

  class Local:
    def __init__(self):
      pass

    def is_existed(self, local_path):
      return os.path.exists(local_path)

    def copy(self, src, dest):
      if not os.path.exists(src):
        raise RuntimeError("File::Local::copy_to: source file does not exist")

      copy_cmd = "cp {} {}".format(src, dest)
      local_cmd = LocalCommand()
      local_cmd.exec(copy_cmd)
      if not local_cmd.is_succeed():
        print("File::Local::copy_to: failed to copy file, reason: {}".format(
               local_cmd.get_error()))
        return False
      return True

    def __del__(self):
      pass