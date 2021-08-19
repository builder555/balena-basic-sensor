### Balena Blocks: basic sensor

Gets input from a pin and publishes it to specified MQTT topic

Currently supports only Balena Fin and Raspberry Pi devices.

___Usage a block___

Add the following to your `docker-compose.yaml`:

```yaml
  sensor:
    privileged: true
    build: ./basic-sensor
    restart: always
    environment:
      - output=sensor_1
      - pin=17
```
A message with payload "1" is published on `output` topic when the pin is high and "0" when pin is low.

___Available variables___
- `output`: name of MQTT topic to publish
- `pin`: physical pin to use on the device
- `inverting`: whether the output should be inverted, i.e. if set to 'true', will send '0' when pin is high and '1' when low

___Environment variables defaults___
- `output`: "output"
- `pin`: 17
- `inverting`: false

___Tests___

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
$ pipenv shell
$ pytest -vs
```

___Standalone usage___

Publish MQTT message when specified pin changes state.

Given the code
```python
>>> from devicemqttpub import DeviceMQTTPubWrapper
>>> from piinput import SensorAdaptor
>>> from time import sleep
>>> sensor = SensorAdaptor(pin_number=10, is_inverting=False)
>>> mqtt = DeviceMQTTPubWrapper(device=sensor, name='output')
>>> while True:
>>>     sleep(1)
```
A message with payload '1' will be published under topic 'output' when pin 10 is activated, and payload '0' when deactivated.

> N.B. mqtt connects to host 'mqtt' on port 1883
