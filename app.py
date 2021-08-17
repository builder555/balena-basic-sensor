from devicemqttpub import DeviceMQTTPubWrapper
from piinput import SensorAdaptor
from time import sleep
import os

if __name__ == '__main__':
    pin = os.environ.get('pin')
    output = os.environ.get('output')
    sensor = SensorAdaptor(pin_number=pin, is_inverting=False)
    sensor.auto_trigger(period=10)
    mqtt = DeviceMQTTPubWrapper(device=sensor, name=output)
    while True:
        sleep(1)
