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
    # 從 entry.data 攞 JSON 數據
    data = entry.data.get("energy_data", {})

    # 提取總數據
    monthly_on_time = int(data.get("MonthlyOnTime", 0))
    monthly_on_time_ai = int(data.get("MonthlyOnTimeAI", 0))
    ai_saving = int(data.get("AISaving", 0))

    # 提取每日數據
    monthly_details = data.get("MonthlyOnTimeDetail", [])
    monthly_ai_details = data.get("MonthlyOnTimeAIDetail", [])

    # 創建感應器
    sensors = [
        TotalOnTimeSensor(hass, entry, "monthly_on_time", monthly_on_time),
        TotalOnTimeSensor(hass, entry, "monthly_on_time_ai", monthly_on_time_ai),
        TotalOnTimeSensor(hass, entry, "ai_saving", ai_saving)
    ]

    # 為每個日子創建感應器（包括節省）
    for detail, ai_detail in zip(monthly_details, monthly_ai_details):
        day = detail["Day"]  # 例如 "02-01"
        on_time = detail["OnTime"]
        on_time_ai = ai_detail["OnTime"]
        daily_saving = on_time - on_time_ai  # 每日節省
        date_key = f"2025_{day.replace('-', '_')}"  # 例如 "2025_02_01"
        sensors.append(DailyOnTimeSensor(hass, entry, f"on_time_{date_key}", on_time))
        sensors.append(DailyOnTimeSensor(hass, entry, f"on_time_ai_{date_key}", on_time_ai))
        sensors.append(DailyOnTimeSensor(hass, entry, f"daily_saving_{date_key}", daily_saving))

    # 加入感應器
    async_add_entities(sensors)
