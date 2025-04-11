from homeassistant.components.sensor import SensorEntity

class TotalOnTimeSensor(SensorEntity):
    def __init__(self, name, value):
        self._state = value
        self._name = f"Energy Tracker {name.replace('_', ' ').title()}"
        self._unique_id = f"energy_tracker_{name}"

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
    def __init__(self, name, value):
        self._state = value
        self._name = f"Energy Tracker {name.replace('_', ' ').title()}"
        self._unique_id = f"energy_tracker_{name}"

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