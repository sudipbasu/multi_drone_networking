# drone_listener.py
import paho.mqtt.client as mqtt
import sys

if len(sys.argv) != 2:
    print("Usage: python drone_listener.py <drone_id>")
    sys.exit(1)

drone_id = sys.argv[1]
TOPIC = f"drone/commands/{drone_id}"
BROKER = "broker.hivemq.com"

def on_connect(client, userdata, flags, rc):
    print(f"[Drone {drone_id}] Connected to broker. Listening on topic: {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"[Drone {drone_id}] Received command: {command}")
    if command == "takeoff":
        print("Drone is taking off...")
    elif command == "land":
        print("Drone is landing...")
    else:
        print(f"Executing command: {command}")

client = mqtt.Client(client_id=f"Drone_{drone_id}")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
