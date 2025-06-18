import paho.mqtt.client as mqtt
from database.bottle_db import update_bottle, update_dispenser_temperature
import json

broker = "158.180.44.197"
port = 1883
topic = "iot1/teaching_factory/#"
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

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("iot1/teaching_factory/#", qos=0)

# create function for callback
def on_message(client, userdata, message):
    print(f"topic: {message.topic}")
    payload_str = message.payload.decode('utf-8')
    print(f"message: {payload_str}")
    print("\n")

    # Repariere das Datum, falls nötig
    if "creation_date" in payload_str:
        import re
        payload_str = re.sub(r'("creation_date"\s*:\s*)(\d{4}-\d{2}-\d{2})', r'\1"\2"', payload_str)

    try:
        payload = json.loads(payload_str)
    except Exception as e:
        print(f"Fehler beim Parsen des JSON: {e}")
        return

    topic = message.topic

    if "drop_oscillation" in topic:
        bottle_id = payload.get("bottle")
        if not bottle_id:
            return
        update_bottle(bottle_id, {"drop_oscillation": payload["drop_oscillation"]})

    elif "ground_truth" in topic:
        bottle_id = payload.get("bottle")
        if not bottle_id:
            return
        update_bottle(bottle_id, {"is_cracked": payload["is_cracked"]})

    elif "dispenser" in topic:
        bottle_id = payload.get("bottle")
        if not bottle_id:
            return
        dispenser = payload["dispenser"]
        data = {
            "fill_level_grams": payload["fill_level_grams"],
            "recipe": payload["recipe"],
            "vibration-index": payload["vibration-index"],
            "time": payload.get("time")
        }
        update_bottle(bottle_id, {"dispenser": {dispenser: data}})

    elif "temperature" in topic:
        bottle_id = payload.get("bottle")
        if not bottle_id:
            return
        dispenser = payload["dispenser"]
        update_dispenser_temperature(bottle_id, dispenser, payload["temperature_C"])

    elif "final_weight" in topic:
        bottle_id = payload.get("bottle")
        if not bottle_id:
            return
        update_bottle(bottle_id, {"final_weight": payload["final_weight"]})

    elif "recipe" in topic:
        print(f"Recipe empfangen: {payload}")
        # Hier könntest du eine eigene update_recipe-Funktion schreiben,
        # oder die Daten in einer separaten TinyDB speichern.
        # Beispiel:
        # update_recipe(recipe_id, payload)
        print(f"Recipe empfangen: {payload}")


# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")              

# assign function to callback
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe                  
mqttc.on_unsubscribe = on_unsubscribe           

# establish connection
mqttc.connect(host= broker, port = port)                                 

# subscribe
#mqttc.subscribe(topic, qos=0)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
mqttc.loop_forever()

#while True:
#    mqttc.loop(0.5)