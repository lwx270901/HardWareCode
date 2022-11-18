import os
import sys

from command.command import LocalCommand

class LocalProcess:
  def __init__(self):
    pass

  def get_pid(self, process_name = ""):
    return Process.get_pid(process_name, LocalCommand())

  def get_process_name(self, pid = -1):
    return Process.get_process_name(pid, LocalCommand())

  def is_process_alive(self, id):
    return Process.is_process_alive(id, LocalCommand())

  def kill_process(self, id):
    return Process.kill_process(id, LocalCommand())
 
  def send_signal(self, id, signal_number):
    return Process.send_signal(id, signal_number, LocalCommand())

  def __del__(self):
    pass


class Process:
  def __init__(self):
    pass

  @staticmethod
  def get_pid(process_name = "", cmd = None):
    if not len(process_name):
      raise RuntimeError("LocalProcess: Missing process name to get PID")
    cmd.exec("ps -C {} -o pid=".format(process_name))
    if cmd.is_succeed():
      cmd.exec("ps -C {} -o pid= |  tr -s ' ' | cut -d\" \" -f2".format(process_name))
      return (True, cmd.get_output())
    else:
      return (False, cmd.get_error())

  @staticmethod
  def get_process_name(pid = -1, cmd = None):
    if pid == -1:
      raise RuntimeError("LocalProcess: Missing valid PID to get its process name")
    cmd.exec("ps -q {} -o comm=".format(pid))
    if cmd.is_succeed():
      return (True, cmd.get_output())
    else:
      return (False, cmd.get_error())

  @staticmethod
  def is_process_alive(id, cmd = None):
    process_id = -1
    if isinstance(id, str):
      ok, process_id = self.get_pid(id)
      if not ok:
        return False
    elif isinstance(id, int):
      process_id = id
    cmd.exec("kill -0 {}".format(process_id))
    if cmd.is_succeed():
      return True
    else:
      return False

  @staticmethod
  def kill_process(id, cmd = None):
    process_id = -1
    if isinstance(id, str):
      ok, process_id = Process.get_pid(id, cmd)
      if not ok:
        return False
    elif isinstance(id, int):
      process_id = id
    cmd.exec("kill -9 {}".format(process_id))
    if cmd.is_succeed():
      return True
    else:
      return False

  @staticmethod
  def send_signal(id, signal_number, cmd = None):
    process_id = -1
    if isinstance(id, str):
      ok, process_id = Process.get_pid(id, cmd)
      if not ok:
        return False
    elif isinstance(id, int):
      process_id = id
    cmd.exec("kill -{} {}".format(signal_number, process_id))
    if cmd.is_succeed():
      return True
    else:
      return False

  def __del__(self):
    pass