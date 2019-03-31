import time
from Adafruit_IO import Client
from sense_hat import SenseHat
import os
import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

#def getcputemp():
#    res = os.popen('vcgencmd measure_temp').readline()
#    return(res.replace("temp=","").replace("'C\n",""))

aio = Client('cba4b3aa2f0d456a9fbe83c91f15ae0e')

while True :
    sense = SenseHat()
    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    
    #calctemp = 0.0071*temp*temp+0.86*temp-10.0
    calchum=humidity*(2.5-0.029*temp)
    #cputemp = int(float(getcputemp())
    #temp_calibrated = temp - ((cputemp-temp)/2)
    t = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cputemp = t.read()
    cputemp = cputemp.replace('temp=','')
    cputemp = cputemp.replace('\'C\n','')
    cputemp = float(cputemp)
    newtemp = temp - ((cputemp - temp) / 2)

    atmpressure = pressure * (0.986923/1000)  #convert from millibars to atms
    
    print 'pressure: %.0f, temp: %.1f, humidity: %.0f' % (pressure, newtemp, calchum)

    aio.send('raspberrypi1-sensehat-temperature', newtemp)
    aio.send('raspberrypi1-sensehat-pressure', pressure)
    aio.send('raspberrypi1-sensehat-humidity', calchum)
    tophonetemp=client.publish("Tempurature", str(round(newtemp,1)))
    tophonehumid=client.publish("Humidity", str(round(calchum,1)))
    tophonepressure=client.publish("Pressure", str(round(atmpressure,4)))
    
    
    
    time.sleep(10)
