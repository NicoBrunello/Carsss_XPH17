from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")


logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient("Pynq", useWebsocket=True)
myAWSIoTMQTTClient.configureIAMCredentials("AKIAI73IV36OVPLH5YSA", "SAf2GQfSEOT3P8e/Bf+Mvr4yPGjV+CXDnp3TzzYb")

myAWSIoTMQTTClient.configureEndpoint("aogjd1jvq4dtd.iot.us-west-2.amazonaws.com", 443)
myAWSIoTMQTTClient.configureCredentials("root-CA.crt")
	

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
	myAWSIoTMQTTClient.publish("sdk/test/Python", "New Message " + str(loopCount), 1)
	loopCount += 1
	time.sleep(1)
