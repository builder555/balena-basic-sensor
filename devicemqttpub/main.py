import paho.mqtt.client as mqtt
import json

class DeviceMQTTPubWrapper:
    def __init__(self, device, name):
        try:
            self.__is_connected = False
            self.client = mqtt.Client()
            self.client.connect('mqtt', 1883, keepalive=60)
            device.on_active = self._on_activate
            device.on_inactive = self._on_deactivate
            self.__device_name = name
            self.__is_connected = True
        except:
            raise Exception('MQTT broker is unreachable')

    def _publish(self, *a, **kw):
        msg = self.client.publish(*a, **kw)
        if not msg.is_published():
            self.client.reconnect()
            self.client.publish(*a, **kw)

    def _on_activate(self):
        self._publish(topic=self.__device_name, payload='1')

    def _on_deactivate(self):
        self._publish(topic=self.__device_name, payload='0')

    @property
    def is_connected(self):
        return self.__is_connected