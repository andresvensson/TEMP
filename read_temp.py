#!/usr/bin/python

import Adafruit_DHT

#Setup vars
sensor = Adafruit_DHT.DHT22
PIN17 = 17
PIN27 = 27

humidity, temperature = Adafruit_DHT.read_retry(sensor, PIN17)


# Here goes changes later on
# will change print and make it push data to DB

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
        print('Failed to get reading. Try again!')

# testing a repeat with other pin



humidity, temperature = Adafruit_DHT.read_retry(sensor, PIN27)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
        print('Failed to get reading. Try again!')
