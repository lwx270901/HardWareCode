import os
import re
import sys
import json

from ..dir.dir import Dir

class JsonReader:
  def __init__(self):
    self.data = dict()
    self.json_file = ""

  """
  Read a json file.
  - If json file does not exist, throw exception RuntimeError
  - This method should be called before other operations on json data
  """
  def read_json_file(self, json_file):
    if not os.path.isfile(json_file):
      raise RuntimeError("Json file %s does not exist" % json_file)

    self.json_file = json_file
    with open(self.json_file, 'r') as f:
      self.data = json.load(f)
    self.data = self._substitute_template_vars(self.data)
    return self.data

  """
  Retrieve data from json data by a key
  - Return None if the data at key is not found
  """
  def get_value_by_key(self, key):
    if not self.data:
      try:
        self.read_json_file(self.json_file)
      except RuntimeError as e:
        return None

    if key in self.data.keys():
      return self.data.get(key)
    else:
      return None

  """
  Json data read from json file may contains template variables.
  This method is to replace all those template variables by values
  from environment variables.
  """
  def _substitute_template_vars(self, data):
    for key in data.keys():
      value = data.get(key)
      if isinstance(value, str):
        temp_var = re.match(r'(.*?)\${(\w+)}(.*?)', value)
        if temp_var:
          data[key] = os.path.expandvars(data[key])
      elif isinstance(value, dict):
        value = self._substitute_template_vars(value)
    return data