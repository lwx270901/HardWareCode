import os
import sys
from .fetcher import Fetcher
import requests
from urllib3.exceptions import HTTPError

class RequestFetcher(Fetcher):
  def __init__(self):
    self.url = ""
    self.response = None

  def __del__(self):
    pass

  def set_url(self, url):
    if not len(url):
      raise RuntimeError("Invalid URL")
    self.url = url

  def _fetch(self):
    if not len(self.url):
      raise RuntimeError("Missing URL")

    try:
      self.response = requests.get(self.url)
    except HTTPError as error:
      print("RequestFetcher caught except: {}".format(error))
      return False
    return True
  
  def save(self, target = "."):
    if not self._fetch():
      return False

    try:
      open(target, "wb").write(self.response.content)
    except OSError as error:
      print("RequestFetcher caught except: {}".format(error))
      return False
    return True