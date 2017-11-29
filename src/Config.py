import json

class Config():
  def logging():
    config = json.load(open('config.json'))
    return config['logging']

  def get_mac():
    config = json.load(open('config.json'))
    return config['mac_address'].upper()