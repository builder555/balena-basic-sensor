import pytest
import json
from unittest.mock import MagicMock, patch, call
from devicemqttpub import DeviceMQTTPubWrapper


class TestWrapperWithException:
    def test_raise_exception_when_mqtt_is_unreachable(self, fake_device):
        with pytest.raises(Exception) as e:
            DeviceMQTTPubWrapper(device=fake_device, name='my-device')
        assert e.value.args[0] == 'MQTT broker is unreachable'

@pytest.mark.usefixtures('patch_mqtt')
class TestWrapper:
    def test_can_connect_to_mqtt_server(self, fake_device):
        mqtt = DeviceMQTTPubWrapper(device=fake_device, name='my-device')
        assert mqtt.is_connected

    def test_publishes_messages_with_device_name_as_topic(self, fake_device, fake_mqtt_client):
        device_name = 'my-device'
        DeviceMQTTPubWrapper(device=fake_device, name=device_name)
        fake_device.on_active()
        assert fake_mqtt_client.get_publish_topic() == device_name

    def test_publishes_OUTPUT_TRUE_when_device_is_ACTIVATED(self, fake_device, fake_mqtt_client):
        DeviceMQTTPubWrapper(device=fake_device, name='my-device')
        fake_device.on_active()
        assert fake_mqtt_client.get_publish_payload() == '1'

    def test_publishes_OUTPUT_FALSE_when_device_is_DEACTIVATED(self, fake_device, fake_mqtt_client):
        DeviceMQTTPubWrapper(device=fake_device, name='my-device')
        fake_device.on_inactive()
        assert fake_mqtt_client.get_publish_payload() == '0'

    def test_can_publish_a_message_when_connection_timed_out(self, fake_device, fake_mqtt_client):
        DeviceMQTTPubWrapper(device=fake_device, name='my-device')
        simulate_timeout(fake_mqtt_client)
        fake_device.on_active()
        assert fake_mqtt_client.reconnect.called
        assert fake_mqtt_client.publish.call_count == 2
        

def simulate_timeout(fake_client):
    unpublished_message = MagicMock()
    unpublished_message.is_published = MagicMock(return_value=False)
    fake_client.publish = MagicMock(return_value=unpublished_message)

@pytest.fixture
def fake_device():
    return MagicMock()

@pytest.fixture
def fake_mqtt_client():
    client = MagicMock()
    client.get_publish_payload = lambda: client.publish.call_args.kwargs.get('payload')
    client.get_publish_topic = lambda: client.publish.call_args.kwargs.get('topic')
    client.publish = MagicMock()
    return client

@pytest.fixture()
def patch_mqtt(fake_mqtt_client):
    fake_mqtt = MagicMock()
    fake_mqtt.Client = MagicMock(return_value=fake_mqtt_client)
    with patch('devicemqttpub.main.mqtt', new=fake_mqtt):
        yield
