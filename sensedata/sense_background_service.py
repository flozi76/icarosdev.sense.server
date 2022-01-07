import signal
import time
import datetime
import sys

import paho.mqtt.client as mqtt
from mqtt.mqtt_client_service import MqttClientService


is_shutdown = False

def stop(sig, frame):
  print(f"SIGTERM at {datetime.datetime.now()}")
  global is_shutdown
  is_shutdown = True

def ignore(sig, frsma):
  print(f"SIGHUP at {datetime.datetime.now()}")

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGHUP, ignore)

print(f"START at {datetime.datetime.now()}")

def main():
    try:
        print("Starting sensedata background service ...")
        mqtt_client = mqtt.Client()
        client = MqttClientService(mqtt_client)
        client.connect()
    finally:
        client.disconnect()

while not is_shutdown:
    main()
    time.sleep(1)

