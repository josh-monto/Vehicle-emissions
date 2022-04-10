#Part 2 code responsible for importing vehicle data, publishing all CO2 data to topic,
#and subscribing to appropriate topics to receive max CO2 value from lambda function
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import datetime
import numpy as np
from threading import Lock 


#Starting and end index, st is 0, end is number of devices
device_st = 0
device_end = 5

#Path to the dataset
data_path = "data/vehicle{}.csv"

#Path to certificates
certificate_formatter = "certs/vehicle{}/vehicle{}.certificate.pem"
key_formatter = "certs/vehicle{}/vehicle{}.private.pem"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address and credentials, make sure address is correct endpoint and correct root CA name is written
        self.client.configureEndpoint("a34g9lmiyjjon2-ats.iot.us-west-2.amazonaws.com", 8883)
        self.client.configureCredentials("certs/Amazon-root-CA-1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        
    def customOnMessage(self,message):
        time.sleep(1)
        print("vehicle{} max CO2 -".format(self.device_id), end = " ")
        data = str(message.payload.decode("utf-8","ignore"))
        print(data)
        self.client.disconnectAsync()

	
    # Callback
    def customCallback(self, client, userdata, message):
    	pass
    	
    # Suback callback
    def customSubackCallback(self, mid, data):
    	pass

    # Puback callback
    def customPubackCallback(self,mid):
    	pass


    def publish(self, data):
        #TODO4: fill in this function for your publish
        vehicle_no = "vehicle{}".format(self.device_id)
        data = data.to_dict()
        CO2_data = data["vehicle_CO2"]
        vehicle_data = {vehicle_no : CO2_data}
        self.client.subscribeAsync("Data/{}".format(vehicle_no), 0, ackCallback = self.customSubackCallback)
        #publish data to topic
        print("publishing data for "+ vehicle_no)
        self.client.publishAsync("Data/CO2", json.dumps(vehicle_data), 0, ackCallback=self.customPubackCallback)
        time.sleep(2)

print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

while True:
    print("Initializing MQTTClients...")
    clients = []
    for device_id in range(device_st, device_end):
    	client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    	client.client.connect()
    	clients.append(client)
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish(data[i])

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)





