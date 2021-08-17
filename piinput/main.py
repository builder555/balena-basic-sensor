from threading import Timer
from .interface import AbstractSensor
try:
    from gpiozero import Button
except:
    Button = None

class SensorAdaptor(AbstractSensor):

    def __init__(self, pin_number, is_inverting=False):
        assert Button, 'This adaptor requires gpiozero library to be installed'
        self.__sensor = Button(pin_number, pull_up=False)
        self.__is_inverting = is_inverting
        self.__period = 0
    
    @property
    def is_on(self):
        if self.__is_inverting:
            return not self.__sensor.is_pressed
        return bool(self.__sensor.is_pressed)

    @property
    def on_active(self): 
        pass

    @property
    def on_inactive(self): 
        pass

    @on_active.setter
    def on_active(self, callback):
        self.__sensor.when_pressed = callback
        self.__on_active = callback

    @on_inactive.setter
    def on_inactive(self, callback):
        self.__sensor.when_released = callback
        self.__on_inactive = callback
    
    def auto_trigger(self, period):
        self.__period = period
        self.__start_update_timer()
    
    def __start_update_timer(self):
        self.timer = Timer(self.__period, self.__trigger_status_update)
        self.timer.start()

    def __trigger_status_update(self):
        if self.is_on:
            self.__on_active()
        else:
            self.__on_inactive()
        self.__start_update_timer()
