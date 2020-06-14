import logging
import struct
import datetime
import subprocess

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.const import (TEMP_CELSIUS, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_ILLUMINANCE, DEVICE_CLASS_BATTERY, STATE_UNKNOWN)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'parrot_flowerpower'
CONF_MAC = 'mac'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string,
})

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=15)
SENSOR_TYPES = [
    ['daily_light_integral', 'Daily Light Integral', 'mol/m2/d', None, DEVICE_CLASS_ILLUMINANCE],
    ['soil_ec', 'Soil EC', 'dS/m', None, None],
    ['soil_temperature', 'Soil Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
    ['air_temperature', 'Air Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
    ['soil_moisture', 'Soil Moisture', '%', None, DEVICE_CLASS_HUMIDITY],
    ['calibrated_soil_moisture', 'Calibrated Soil Moisture', '%', None, DEVICE_CLASS_HUMIDITY],
    ['calibrated_air_temperature', 'Calibrated Air Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
    ['battery_level', 'Battery Level', '%', None, DEVICE_CLASS_BATTERY],
    ['calibrated_daily_light_integral', 'Calibrated Daily Light Integral', 'mol/m2/d', None, DEVICE_CLASS_ILLUMINANCE],
]



def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    _LOGGER.debug("Starting flowerpower")
    reader = FlowerPowerDataReader(config.get(CONF_MAC))
    add_devices([ FlowerPowerSensorEntity(reader, key,name,unit,icon,device_class) for [key, name, unit, icon, device_class] in SENSOR_TYPES])

class FlowerPowerDataReader:
    def __init__(self, mac):
        self._mac = mac
        self._state = { }

    def get_data(self, key):
        if key in self._state:
            return self._state[key]
        return STATE_UNKNOWN

    @property
    def mac(self):
        return self._mac

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug("Flowerpower updating data")
        from bluepy.btle import UUID, Peripheral, Scanner,DefaultDelegate
        periph = None
        
        try:
    
            # Connect to device
            _LOGGER.debug('Connecting')
            periph = Peripheral(self._mac)
            
            if (periph is None):
                _LOGGER.debug('Not connected')
            else:
                services=periph.getServices()
                    
#                ['daily_light_integral', 'Daily Light Integral', 'mol/m2/d', None, None],
#    sensors.append(Sensor("Daily Light Integral"    , "39e1fa01-84a8-11e2-afba-0002a5d5c51b", '<H', "mol/m2/d\t", 1.0))
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa01-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['daily_light_integral'] = struct.unpack('H', rawdata)[0]
                    
#                ['soil_ec', 'Soil EC', 'dS/m', None, None],
#    sensors.append(Sensor("SOIL_EC"                 , "39e1fa02-84a8-11e2-afba-0002a5d5c51b", '<H', "\t", 1.0))
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa02-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['soil_ec'] = struct.unpack('H', rawdata)[0]

#                ['soil_temperature', 'Soil Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
#    sensors.append(Sensor("SOIL_TEMPERATURE"        , "39e1fa03-84a8-11e2-afba-0002a5d5c51b", '<H', "C\t", 1.0))
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa03-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['soil_temperature'] = struct.unpack('H', rawdata)[0]/32.0

#    sensors.append(Sensor("AIR_TEMPERATURE"         , "39e1fa04-84a8-11e2-afba-0002a5d5c51b", '<H', "C\t", 1.0))
#                ['air_temperature', 'Air Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa04-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['air_temperature'] = struct.unpack('H', rawdata)[0]/32.0

#    sensors.append(Sensor("SOIL_MOISTURE"           , "39e1fa05-84a8-11e2-afba-0002a5d5c51b", '<H', "%\t", 1.0))
#                ['soil_moisture', 'Soil Moisture', '%', None, DEVICE_CLASS_HUMIDITY],
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa05-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['soil_moisture'] = struct.unpack('H', rawdata)[0]/32.0

#                ['calibrated_soil_moisture', 'Calibrated Soil Moisture', '%', None, DEVICE_CLASS_HUMIDITY],
#    sensors.append(Sensor("CALIBRATED_SOIL_MOISTURE", "39e1fa09-84a8-11e2-afba-0002a5d5c51b", 'f', "%\t", 1.0))
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa09-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['calibrated_soil_moisture'] = struct.unpack('f', rawdata)[0]

#                ['calibrated_air_temperature', 'Calibrated Air Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
#    sensors.append(Sensor("CALIBRATED_AIR_TEMP"     , "39e1fa0a-84a8-11e2-afba-0002a5d5c51b", 'f', "C\t", 1.0))
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa0a-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['calibrated_air_temperature'] = struct.unpack('f', rawdata)[0]

#    sensors.append(Sensor("Battery"                 , UUID(0x2A19), 'B', "%\t", 1.0))
#                ['battery_level', 'Battery Level', '%', None, DEVICE_CLASS_HUMIDITY],
                curr_val_char = periph.getCharacteristics(uuid=UUID(0x2A19))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['battery_level'] = struct.unpack('B', rawdata)[0]

#    ['calibrated_daily_light_integral', 'calibrated Daily Light Integral', 'mol/m2/d', None, DEVICE_CLASS_ILLUMINANCE],
#    sensors.append(Sensor("CALIBRATED_DLI"          , "39e1fa0b-84a8-11e2-afba-0002a5d5c51b", 'f', "mol/m2/d\t", 1.0))
                curr_val_char = periph.getCharacteristics(uuid=UUID("39e1fa0b-84a8-11e2-afba-0002a5d5c51b"))[0]
                if (curr_val_char is None):
                    _LOGGER.debug('Not connected')
                else: 
                    _LOGGER.debug('Reading data')
                    rawdata = curr_val_char.read()
                    _LOGGER.debug("Data:{}".format(' '.join(map(str, list(rawdata)))))
                    self._state['calibrated_daily_light_integral'] = struct.unpack('f', rawdata)[0]

#    sensors.append(Sensor("LIVE_MODE_PERIOD"        , "39e1fa06-84a8-11e2-afba-0002a5d5c51b", '<H', "%\t", 1.0))
#    sensors.append(Sensor("LED"                     , "39e1fa07-84a8-11e2-afba-0002a5d5c51b", '<H', "%\t", 1.0))
#    sensors.append(Sensor("LAST_MOVE_DATE"          , "39e1fa08-84a8-11e2-afba-0002a5d5c51b", '<H', "%\t", 1.0))
#    sensors.append(Sensor("CALIBRATED_DLI"          , "39e1fa0b-84a8-11e2-afba-0002a5d5c51b", 'f', "mol/m2/d\t", 1.0))
#    sensors.append(Sensor("CALIBRATED_EA"           , "39e1fa0c-84a8-11e2-afba-0002a5d5c51b", 'f', "\t", 1.0))
#    sensors.append(Sensor("CALIBRATED_ECB"          , "39e1fa0d-84a8-11e2-afba-0002a5d5c51b", 'f', "dS/m\t", 1.0))
#    sensors.append(Sensor("CALIBRATED_EC_POROUS"    , "39e1fa0e-84a8-11e2-afba-0002a5d5c51b", 'f', "dS/m\t", 1.0))
#    sensors.append(Sensor("Firmware"                , UUID(0x2A26), 'HBBBBB', "\t", 1.0))

                
        except :
            _LOGGER.debug('Not connected, error')

#            _LOGGER.debug('Resetting bluetooth')
#            subprocess.Popen(["sudo", "systemctl", "restart", "bluetooth"]).wait(5)
#            subprocess.Popen(["sudo", "hciconfig", 'hci0', "reset"]).wait(5)
        finally:
            if periph is not None:
                _LOGGER.debug('Disconnecting')
                periph.disconnect()
 
class FlowerPowerSensorEntity(Entity):
    """Representation of a Sensor."""

    def __init__(self, reader, key, name, unit, icon, device_class):
        """Initialize the sensor."""
        self._reader = reader
        self._key = key
        self._name = name
        self._unit = unit
        self._icon = icon
        self._device_class = device_class

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'FlowerPower {}'.format(self._name)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def device_class(self):
        """Return the icon of the sensor."""
        return self._device_class

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._reader.get_data(self._key)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self):
        return '{}-{}'.format(self._reader.mac, self._name)

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._reader.update()
