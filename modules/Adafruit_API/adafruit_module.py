# Import library and create instance of REST client.
from Adafruit_IO import *
ADAFRUIT_USER = "izayazuna" #use for unit test
ADAFRUIT_IO_KEY = "aio_UGWB75AXectDhYGRLrmgGv2pGwP8" #use for unittest



class AdafruitModule:
  def __init__(self, user, key):
    self.aio = Client(user, key)
    
  def sendDataToFeed(self, feed_name, feed_data):
    self.aio.send(feed_name, feed_data)
    data = self.aio.receive(feed_name)
    print('Received value: {0}'.format(data.value))
    pass

#Unit Test