import paho.mqtt.client as mqtt
broker = "158.180.44.197"
port = 1883
topic = "at/house/bulb1"
payload = "on"

# create function for callback
def on_message(client, userdata, message):
    print("message received:")
    print("message: ", message.payload.decode())
    print("\n")

# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")              

# assign function to callback
mqttc.on_message = on_message                          

# establish connection
mqttc.connect(broker,port)                                 

# subscribe
mqttc.subscribe(topic, qos=0)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
#mqttc.loop_forever()

while True:
    mqttc.loop(0.5)