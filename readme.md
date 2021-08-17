### Balena Blocks: basic sensor

Gets input from a pin and publishes it to specified MQTT topic

Currently supports only Balena Fin and Raspberry Pi devices.

_Usage a block_

Add the following to your `docker-compose.yaml`:

```yaml
  sensor:
    privileged: true
    build: ./basic-sensor
    restart: always
    environment:
      - output=sensor_1 # name of MQTT topic to publish
      - pin=17 # physical pin to use on the device
```

_Tests_

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
$ pipenv shell
$ pytest -vs
```

_Standalone usage_

Publish MQTT message when specified pin is activated/deactivated.

Given the code
```python
>>> from devicemqttpub import DeviceMQTTPubWrapper
>>> from piinput import SensorAdaptor
>>> sensor = SensorAdaptor(pin_number=10, is_inverting=False)
>>> mqtt = DeviceMQTTPubWrapper(device=sensor, name='output')
```
A message with payload '1' will be published under topic 'output' when pin 10 is activated, and payload '0' when deactivated.
