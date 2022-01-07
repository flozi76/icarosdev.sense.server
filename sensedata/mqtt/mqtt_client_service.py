import sys
import paho.mqtt.client as mqtt
import json
import pytz
from datetime import datetime, timezone

class MqttClientService:
    topic = "topic/environment/data"
    mqtt_broker = "raspberrypi.local"
    mqtt_broker_port = 1883
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def connect(self):
        self.mqtt_client.connect(self.mqtt_broker,self.mqtt_broker_port,60)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.subscribe(self.topic,0)
        self.mqtt_client.loop_forever()
    
    def disconnect(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def on_connect(self, client, userdata, rc, tc):
        if rc != 0:
            print(f"MQTT Client Connected Broker: {self.mqtt_broker}:{self.mqtt_broker_port}")

    # def start_read_loop(self):
    #     self.mqtt_client.loop_forever()

    def on_message(selfclient, userdata, none, message):
        print("Received message '" + str(message.payload) + "' on topic '"
            + message.topic + "' with QoS " + str(message.qos))
       