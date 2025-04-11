from homeassistant.components.sensor import SensorEntity

class TotalOnTimeSensor(SensorEntity):
    def __init__(self, name, value, entry_id):
        self._state = value
        self._name = f"Energy Tracker {name.replace('_', ' ').title()}"
        self._unique_id = f"energy_tracker_{entry_id}_{name}"
        self._attr_should_poll = False

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "minutes"

    @property
    def unique_id(self):
        return self._unique_id

class DailyOnTimeSensor(SensorEntity):
    def __init__(self, name, value, entry_id):
        self._state = value
        self._name = f"Energy Tracker {name.replace('_', ' ').title()}"
        self._unique_id = f"energy_tracker_{entry_id}_{name}"
        self._attr_should_poll = False

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "minutes"

    @property
    def unique_id(self):
        return self._unique_id

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor platform."""
    sensors = entry.runtime_data
    async_add_entities(sensors)

    @property
    def unique_id(self):
        return self._unique_id
