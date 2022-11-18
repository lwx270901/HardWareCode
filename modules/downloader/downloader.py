import os
import sys
import urllib.request

class Downloader:
  def __init__(self, fetcher = None):
    if not fetcher:
      raise RuntimeError("No Fetcher set to Downloader")
    self.fetcher = fetcher

  def __del__(self):
    pass

  def download(self, url, save_to = "."):
    if not len(url):
      raise RuntimeError("Invalid URL")
    self.fetcher.set_url(url)
    self.fetcher.save(save_to)

  def checkconnect(self, url):
    try:
        urllib.request.urlopen(url) #Python 3.x
        return True
    except:
        return False