from datetime import datetime
from dht11 import dht11
import os
import json
import time
import RPi.GPIO as GPIO


class sensio:
    def __init__(self, sensors=None):
        self.sensors = sensors
        # currently use json as storage so we need this
        if not os.path.exists('./dht11.json'):
            with open('./dht11.json', mode='w+') as f:
                json.dump([], f)
		f.close()

    def run(self):
        while True:
            dt = datetime.now().__str__()
            for s in self.sensors:
                if isinstance(s, dht11.DHT11):
                    res = s.read()
                    with open('./dht11.json', mode='r+') as f:
                        feeds = json.load(f)
                        entry = {'ts': dt,
                                 'temperature': res.temperature,
                                 'humidity': res.humidity}
                        feeds.append(entry)
			print(feeds)
		    with open('./dht11.json', mode='w') as f:
                        json.dump(feeds, f)
			f.close()
            time.sleep(5)


def main():
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    sensors = []
    # read temperature and humidity data from pin 3
    sensors.append(dht11.DHT11(pin=3))
    sense = sensio(sensors)
    sense.run()


if __name__ == '__main__':
    main()
