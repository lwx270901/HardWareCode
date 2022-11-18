from threading import Lock
class Singleton(type):
  _instances = {}
  _lock = Lock()
  def __call__(cls, *args, **kwargs):
    with cls._lock:
      if cls not in cls._instances:
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance
    return cls._instances[cls]


import os
import sys
import logging
class Logger(metaclass=Singleton):
  def __init__(self, llv, quiet, log_file_path):
    self.log_level     = llv
    self.quiet         = quiet
    self.log_file_path = log_file_path

    self.logfile_fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    self.console_fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    self.logger      = logging.getLogger('nvx')
    self.logger.setLevel(logging.DEBUG)

    if not self.quiet:
      self._add_console_log_handler()
    self._add_log_file_handler()

  def _add_log_file_handler(self):
    self.logger.addHandler(self._create_log_file_handler())

  def _add_console_log_handler(self):
    self.logger.addHandler(self._create_console_log_handler())

  def _create_log_file_handler(self):
    log_file_handler = logging.FileHandler(self.log_file_path, 'a');
    log_file_handler.setLevel(self.log_level)
    log_file_handler.setFormatter(self.logfile_fmt)
    return log_file_handler

  def _create_console_log_handler(self):
    console_log_handler = logging.StreamHandler(sys.stdout);
    console_log_handler.setLevel(self.log_level)
    console_log_handler.setFormatter(self.console_fmt)
    return console_log_handler

  def debug(self, message):
    self.logger.debug(message)

  def info(self, message):
    self.logger.info(message)

  def warn(self, message):
    self.logger.warn(message)

  def error(self, message):
    self.logger.error(message)

  def critical(self, message):
    self.logger.critical(message)