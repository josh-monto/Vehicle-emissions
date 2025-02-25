#emulator-client.py
# Part 1 Initial edit of emulator-client code, even numbered vehicles subscribe to messages from odd numbered ones
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import datetime
import numpy as np
from threading import Lock 

#Starting and end index, st is 0, end is number of devices
device_st = 0
device_end = 50

#Path to certificates
certificate_formatter = "certs/vehicle{}/vehicle{}.certificate.pem"
key_formatter = "certs/vehicle{}/vehicle{}.private.pem"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        # Broker address and credentials, make sure address is correct endpoint and correct root CA name is written
        self.client.configureEndpoint("a34g9lmiyjjon2-ats.iot.us-west-2.amazonaws.com", 8883)
        self.client.configureCredentials("certs/Amazon-root-CA-1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        
    def customOnMessage(self,message):
        #Show received message
        print("Vehicle_{} received -".format(self.device_id), end = " ")
        data = str(message.payload.decode("utf-8","ignore"))
        print(data)
        #Don't delete this line
        self.client.disconnectAsync()


    # Suback callback
    def customSubackCallback(self,mid, data):
        pass

    # Puback callback
    def customPubackCallback(self,mid):
        pass


    def publish(self):
        #Publish data to topic
        self.client.connect()
        if int(self.device_id) % 2 == 0: #if device id is even, make subscriber
            self.client.subscribeAsync("Test/topic1", 0, ackCallback=self.customSubackCallback)
        else: #if device id is odd, make publisher
            self.client.publishAsync("Test/topic1", "Hello from Vehicle_{}".format(self.device_id), 0, ackCallback=self.customPubackCallback)

print("wait")
lock = Lock()

clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    clients.append(client)

print("send now?")
x = input()
if x == "s":
    for i,c in enumerate(clients):
        c.publish()
    # print("done")
elif x == "d":
    for c in clients:
        c.disconnect()
        print("All devices disconnected")
else:
    print("wrong key pressed")

time.sleep(10)





