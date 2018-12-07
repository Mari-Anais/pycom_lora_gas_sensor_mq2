import time
import pycom
import ujson
import machine


from pytrack import Pytrack
#from LIS2HH12 import LIS2HH12
#from L76GNSS import L76GNSS
from network import WLAN
from mqtt import MQTTClient
from ubinascii import hexlify
from mq import MQ

SLEEP_INTERVAL = 120

SSID = 'LANCOMBEIA'
WIFI_PASSWORD = 'beialancom'
WIFI_SECURITY = WLAN.WPA2

MQTT_SERVER = 'mqtt.beia-telemetrie.ro'
MQTT_PORT = 1883
MQTT_TOPIC = 'citisim/pycom/ST1'

# Disable heartbeat LED
pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

pycom.rgbled(0xFF8C00)

wlan.connect(ssid=SSID, auth=(WIFI_SECURITY, WIFI_PASSWORD))
print('Connecting to Wifi')

while not wlan.isconnected():
    machine.idle()

print('Wifi connection succeded!')

pycom.rgbled(0xFF00FF)
print('Connecting to MQTT...\n')
client_id = 'pytrack_{}'.format(hexlify(wlan.mac()).decode('utf-8'))
mqtt_client = MQTTClient(client_id, MQTT_SERVER, port=MQTT_PORT)
mqtt_client.connect()
print('Connected to MQTT as {}'.format(client_id))

pycom.rgbled(0x001400)


#py = Pytrack()
#li = LIS2HH12(py)

# after 240 seconds of waiting without a GPS fix it will
# return None, None
#gnss = L76GNSS(py, timeout=10)
mq2 = MQ('P15')
while True:
    pycom.rgbled(0x000014)

    print('\n\n** MQ2 Gas Sensor ppm value')
    mq2_gas_value = mq2.MQRead()
    print('MQ2 GAS_Value: {}'.format(mq2_gas_value))

    payload = {'mq2': mq2_gas_value}

    print('Sending MQTT message...\n')
    mqtt_client.publish(MQTT_TOPIC, ujson.dumps(payload))

    pycom.rgbled(0x001400)

    print('Sleeping for {} seconds.\n'.format(SLEEP_INTERVAL))
    time.sleep(10)
