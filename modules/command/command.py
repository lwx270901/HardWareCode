import os
import sys
import subprocess

class LocalCommand:
  def __init__(self):
    self.retcode = 1
    self.output  = ""
    self.error   = ""

  def exec(self, cmd = '') -> tuple:
    if cmd == '':
      raise RuntimeError("LocalCommand: None command passed in as mandatory argument")
    
    process = subprocess.Popen(cmd, shell = True, text = True,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE)
    output, error = process.communicate()
    self.retcode = process.wait()
    self.output = output.strip()
    self.error = error.strip()
    return (self.retcode, self.output, self.error)

  def is_succeed(self):
    return (self.retcode == 0)

  def get_retcode(self):
    return self.retcode

  def get_output(self):
    return self.output

  def get_error(self):
    return self.error

  def __del__(self):
    pass