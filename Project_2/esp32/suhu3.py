import dht
import network
import ntptime
import ujson
import utime

from machine import RTC
from machine import Pin
from time import sleep

from umqtt.simple import MQTTClient

# Konstanta-konstanta aplikasi

# WiFi AP Information
AP_SSID = "TUF"
AP_PASSWORD = "123123123"

# MQTT Information
MQTT_BRIDGE_HOSTNAME = "raspberrypi.local"
MQTT_BRIDGE_PORT = 1883

# ID of the Device
DEVICE_ID = "esp32_dht22"

data = [0,0]


dht22_obj = dht.DHT22(Pin(4))

def read_dht22():    
    try:
        dht22_obj.measure()
        data[0] = dht22_obj.temperature()
        data[1] = dht22_obj.humidity()
    except:
        return None
    
    

def connect():
    # Connect to WiFi
    print("Connecting to WiFi...")
    
    # Activate WiFi Radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If not connected, try tp connect
    if not wlan.isconnected():
        # Connect to AP_SSID using AP_PASSWORD
        wlan.active(True)
        wlan.connect(AP_SSID, AP_PASSWORD)
        # Loop until connected
        while not wlan.isconnected():
            pass
    
    # Connected
    print("  Connected:", wlan.ifconfig())


def set_time():
    # Update machine with NTP server
    print("Updating machine time...")

    # Loop until connected to NTP Server
    while True:
        try:
            # Connect to NTP server and set machine time
            ntptime.settime()
            # Success, break out off loop
            break
        except OSError as err:
            # Fail to connect to NTP Server
            print("  Fail to connect to NTP server, retrying (Error: {})....".format(err))
            # Wait before reattempting. Note: Better approach exponential instead of fix wiat time
            utime.sleep(0.5)
    
    # Succeeded in updating machine time
    print("  Time set to:", RTC().datetime())


def on_message(topic, message):
    print((topic,message))


def get_client():
    #Create our MQTT client.
    client = MQTTClient(client_id=DEVICE_ID,
                        server=MQTT_BRIDGE_HOSTNAME,
                        port=MQTT_BRIDGE_PORT)
    client.set_callback(on_message)

    try:
        client.connect()
    except Exception as err:
        print(err)
        raise(err)

    return client

def command(client):
    
    
    mqtt_config_topic = '/devices/{}/config'.format(DEVICE_ID)
    client.subscribe(mqtt_config_topic, qos=1)
    mqtt_command_topic = '/devices/{}/commands/#'.format(DEVICE_ID)
    
    print('Subscribing to {}'.format(mqtt_command_topic))
    while True:
        client.subscribe(mqtt_command_topic, qos=0)
    
    return client


def publish(client, payload):
    # Publish an event
    
    # Where to send
    mqtt_topic = '/devices/temperature'
    
    # What to send
    payload = ujson.dumps(payload).encode('utf-8')
    
    # Send    
    client.publish(mqtt_topic.encode('utf-8'),
                   payload,
                   qos=1)
    
def fungsiX(x):
    print("Data dikirimkan setiap {} Detik !!!".format(x))
    while True:
        read_dht22()
        temp = data[0]
        humd = data[1]
        print("  Temperature: ", temp)
        print("  Kelembapan: ", humd)
        print()
        # Publish a message
        print("Publish Data")
        if data == None:
            suhu = "Fail to read sensor...."
        publish(client, data)
        sleep(x)
    
    

# Connect to Wifi
connect()
# Set machine time to now
set_time()


# Connect to MQTT Server
print("Connecting to MQTT broker...")
start_time = utime.time()
client = get_client()
end_time = utime.time()
print("  Connected in", end_time - start_time, "seconds.")



print("Reading from DHT22")
fungsiX(5)

# Need to wait because command not blocking
utime.sleep(1)

# Disconnect from client
client.disconnect()
