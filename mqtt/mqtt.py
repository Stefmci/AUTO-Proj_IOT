import paho.mqtt.client as mqtt

broker = "158.180.44.197"
port = 1883
topic1 = "iot1/teaching_factory/temperature" #Temperature red, Time, 
topic2 = "iot1/teaching_factory/dispenser_red"  #bottle, fill level grams, time red, recipe, vibration index
topic3 = "iot1/teaching_factory/scale/final_weight"  #final weight grams
payload = "on"



def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()

def on_connect_1(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("iot1/teaching_factory/temperature", qos=0)

def on_connect_2(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("iot1/teaching_factory/dispenser_red", qos=0)


# create function for callback
def on_message(client, userdata, message):
    print(f"topic: {message.topic}")
    print(f"message: {message.payload.decode("utf-8")}")
    print("\n")

# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")              

# assign function to callback
mqttc.on_message = on_message
mqttc.on_connect = on_connect_1
mqttc.on_connect = on_connect_2
mqttc.on_subscribe = on_subscribe                  
mqttc.on_unsubscribe = on_unsubscribe           

# establish connection
mqttc.connect(host= broker, port = port)    

mqttc.connect                             

# subscribe
#mqttc.subscribe(topic, qos=0)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
mqttc.loop_forever()

#while True:
#    mqttc.loop(0.5)