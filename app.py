from devicemqttpub import DeviceMQTTPubWrapper
from piinput import SensorAdaptor
from time import sleep
import os

if __name__ == '__main__':
    pin = int(os.environ.get('PIN','17'))
    output = os.environ.get('OUTPUT','output')
    inverting = os.environ.get('INVERTING','false')
    sensor = SensorAdaptor(pin_number=pin, is_inverting=inverting=='true')
    sensor.auto_trigger(period=10)
    mqtt = DeviceMQTTPubWrapper(device=sensor, name=output)
    while True:
        sleep(1)
