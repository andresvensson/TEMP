#!/usr/bin/python
import Adafruit_DHT
import db
from time import sleep
from datetime import datetime
import configparser
#Setup global variables
sensor = Adafruit_DHT.DHT22
config = configparser.ConfigParser()
PIN17 = 17
PIN27 = 27
SLEEPY_TIME_MINUTES = 5


def read_temperature(pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        return '{0.1f}'.format(temperature), '{0.1f}'.format(humidity)
    else:
        print('Failed to get reading. Try again!')
        return 0, 0


def get_location(sensorID):
    return 'Unknown'


def store_in_database(temp, humidity, curr_sensor):
    data = db.get_reading_dict()
    data["timestamp"] = datetime.now()
    data["sensor"] = curr_sensor
    data["temp"] = temp
    data["humidity"] = humidity
    data["location"] = get_location(curr_sensor)
    db.insert_row(data)
    return True


def main_loop():
    while True:
        config.read('DHT22.cfg')
        t, h = 0, 0
        t, h = read_temperature(PIN17)
        store_in_database(t, h, '1')
        t, h = 0, 0
        read_temperature(PIN27)
        store_in_database(t, h, '2')
        sleep(SLEEPY_TIME_MINUTES * 60)

if __name__ == "__main__":
    main_loop()


# COMPLETED: While loop added with a sleep in between loops.
# COMPLETED: Refactor current sensor calls to a function.
# COMPLETED: Push data to DB.
  
