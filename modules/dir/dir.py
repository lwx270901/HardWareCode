import os
import sys

from modules.command.command import LocalCommand

class Dir:
  def __init__(self):
    pass

  def __del__(self):
    pass

  class Local:
    def __init__(self):
      pass

    def is_existed(self, local_path):
      return os.path.isdir(local_path)

    def copy(self, src, dest):
      if not os.path.exists(src):
        raise RuntimeError("Dir::Local::copy: source dir does not exist")

      copy_cmd = "cp -r {} {}".format(src, dest)
      local_cmd = LocalCommand()
      local_cmd.exec(copy_cmd)
      if not local_cmd.is_succeed():
        print("Dir::Local::copy failed to copy dir, reason: {}".format(
               local_cmd.get_error()))
        return False
      return True

    def __del__(self):
      pass