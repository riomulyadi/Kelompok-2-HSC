import dht
import network
import ntptime
import ujson
import utime

from machine import RTC
from machine import Pin
from time import sleep


from third_party import rd_jwt

from umqtt.simple import MQTTClient


# Konstanta-konstanta aplikasi

# WiFi AP Information
AP_SSID = "TUF"
AP_PASSWORD = "123123123"

# Decoded Private Key
PRIVATE_KEY = (27457045120350810686031336939482909109917283719193652193247353375718938798484885077492699820266505824492296893829618988895793644234968988868689500134314117572759636335288306592962007868655090276107837619291073260197350739300991022801264759046091913700009746362755800234512711656901005618297221086482040919257416871389070353300313908991362409013312207700256913145717543292598174362781264886405624409266491201210722785907678484203896243098751010930315867197759385068555006840417594129472250406116255536695407831659252477034988832402807207280952898747877419365479070420352937956839025580548848805969246576889092617164261, 65537, 24088229034586420055908231207905600533802342870725822459113933040730215071756213320956410407343073666554909474153955374605986715426915742008242237205281360208178403813627973142941294298124617704733146646302997515423453592731583378045707288800434879077402999479271365645109523924274535285863207403274050150199206306834166192269048412347797626885583196135289310729165721430989820939467821958342433935719298869709276876561117799107210910894895453697741284781337504832826547109793334903047312523011242593220092436328406941872585710128948795443293174031033678128685007030747318122709509284063311769655993121653913154075169, 168318636269885475902274174433741113072461681492562756023706373356410722534971473150961038909717073200709584709977564450454842356579502662751112205670541220651356989053431397845520761315840557465815009857406665210374987364744942861677843246958919960537369477330681630826661850021837147564882623935609520751667, 163125401493424852089633285733226944339058577577910337214814284227503606332583804170760266745467427993718525756174949249592759665944234213911099421014055093399798836780090978095845395103256814629182393256298195477326213120695539656385380628373380378928946911888142860588454068121674531509539596235928720827783)

#Project ID of IoT Core
PROJECT_ID = "hsc2020-02"
# Location of server
REGION_ID = "asia-east1"
# ID of IoT registry
REGISTRY_ID = "NPM1704111010010"
# ID of this device
DEVICE_ID = "ESP32"

data = []

# MQTT Information
MQTT_BRIDGE_HOSTNAME = "mqtt.googleapis.com"
MQTT_BRIDGE_PORT = 8883


dht22_obj = dht.DHT22(Pin(4))
led_obj = Pin(23, Pin.OUT)

def suhu():    
    dht22_obj.measure()
    data1 = dht22_obj.temperature()
    print("Temperature: ", data1)
    
def kelembapan():    
    dht22_obj.measure()
    data2 = dht22_obj.humidity()
    print("Kelembapan: ", data2)
    
def led():
    while True:
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        break
    

def connect():
    # Connect to WiFi
    print("Connecting to WiFi...")
    
    # Activate WiFi Radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If not connected, try tp connect
    if not wlan.isconnected():
        # Connect to AP_SSID using AP_PASSWORD
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


def get_client(jwt):
    #Create our MQTT client.
    #
    # The client_id is a unique string that identifies this device.
    # For Google Cloud IoT Core, it must be in the format below.
    #
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    client = MQTTClient(client_id.encode('utf-8'),
                        server=MQTT_BRIDGE_HOSTNAME,
                        port=MQTT_BRIDGE_PORT,
                        user=b'ignored',
                        password=jwt.encode('utf-8'),
                        ssl=True)
    client.set_callback(on_message)

    try:
        client.connect()
    except Exception as err:
        print(err)
        raise(err)

    return client


def publish(client, payload):
    # Publish an event
    
    # Where to send
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'events')
    
    # What to send
    payload = ujson.dumps(payload).encode('utf-8')
    
    # Send    
    client.publish(mqtt_topic.encode('utf-8'),
                   payload,
                   qos=1)
    

# Connect to Wifi
connect()
# Set machine time to now
set_time()

# Create JWT Token
print("Creating JWT token.")
start_time = utime.time()
jwt = rd_jwt.create_jwt(PRIVATE_KEY, PROJECT_ID)
end_time = utime.time()
print("  Created token in", end_time - start_time, "seconds.")

# Connect to MQTT Server
print("Connecting to MQTT broker...")
start_time = utime.time()
client = get_client(jwt)
end_time = utime.time()
print("  Connected in", end_time - start_time, "seconds.")

# Publish a message
print("Publishing message...")
if data == None:
    data = "Fail to read sensor...."

command = input("Input Command : ")

if(command == 'PING'):
    led()
elif(command == 'Baca Suhu'):
    suhu()
elif(command == 'Baca Kelembapan'):
    kelembapan()
else:
    command = input("Input Command : ")

publish(client, data)


# Need to wait because command not blocking
utime.sleep(1)

# Disconnect from client
client.disconnect()


