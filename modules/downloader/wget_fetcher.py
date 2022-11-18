import os
import sys
from .fetcher import Fetcher
import wget
from urllib3.exceptions import HTTPError

class WgetFetcher(Fetcher):
  def __init__(self):
    self.url = ""
    self.response = None

  def __del__(self):
    pass

  def set_url(self, url):
    if not len(url):
      raise RuntimeError("Invalid URL")
    self.url = url

  def _fetch(self, saved_file):
    if not len(self.url):
      raise RuntimeError("Missing URL")

    try:
      self.response = wget.download(self.url, saved_file)
    except HTTPError as error:
      print("WgetFetcher caught except: {}".format(error))
      return False
    return True
  
  def save(self, target = "."):
    return self._fetch(target)