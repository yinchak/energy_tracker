from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

class TotalOnTimeSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, name: str, value: int):
        """Initialize the sensor."""
        self._attr_has_entity_name = True
        self._attr_unique_id = f"energy_tracker_{entry.entry_id}_{name}"
        self.entity_description = SensorEntityDescription(
            key=name,
            name=f"Energy Tracker {name.replace('_', ' ').title()}",
            native_unit_of_measurement="minutes"
        )
        self._attr_native_value = value
        self._attr_should_poll = False

class DailyOnTimeSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, name: str, value: int):
        """Initialize the sensor."""
        self._attr_has_entity_name = True
        self._attr_unique_id = f"energy_tracker_{entry.entry_id}_{name}"
        self.entity_description = SensorEntityDescription(
            key=name,
            name=f"Energy Tracker {name.replace('_', ' ').title()}",
            native_unit_of_measurement="minutes"
        )
        self._attr_native_value = value
        self._attr_should_poll = False

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor platform."""
    sensors = entry.runtime_data
    async_add_entities(sensors)
