import json
import aiofiles
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_FILE_PATH

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

class MonthlyDataSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, month_key: str, monthly_data: dict):
        """Initialize the monthly data sensor."""
        self._attr_has_entity_name = True
        self._attr_unique_id = f"energy_tracker_{entry.entry_id}_monthly_data_{month_key}"
        self.entity_description = SensorEntityDescription(
            key=f"monthly_data_{month_key}",
            name=f"Energy Tracker Monthly Data {month_key.replace('_', '-')}",
            native_unit_of_measurement=None
        )
        self._attr_native_value = 0  # 唔用 state，直接用 attributes
        self._attr_should_poll = False
        self._attr_extra_state_attributes = monthly_data

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor platform."""
    # 從 Config Entry 攞 JSON 檔案路徑
    file_path = entry.data[CONF_FILE_PATH]

    # 異步讀取 JSON 數據
    try:
        async with aiofiles.open(file_path, mode="r") as file:
            content = await file.read()
            data = json.loads(content)
    except Exception as e:
        hass.components.logger.error(f"無法讀取 JSON 檔案 {file_path}: {e}")
        return

    # 提取總數據
    monthly_on_time = int(data.get("MonthlyOnTime", 0))
    monthly_on_time_ai = int(data.get("MonthlyOnTimeAI", 0))
    ai_saving = int(data.get("AISaving", 0))

    # 提取每日數據
    monthly_details = data.get("MonthlyOnTimeDetail", [])
    monthly_ai_details = data.get("MonthlyOnTimeAIDetail", [])

    # 按月份分組
    euid_date = data.get("EUIDDate", "").split("#")[-1]  # 例如 "2025-02"
    month_key = euid_date.replace("-", "_")  # 例如 "2025_02"

    # 準備每月數據
    monthly_data = {
        "on_time": {},
        "on_time_ai": {},
        "daily_saving": {}
    }
    for detail, ai_detail in zip(monthly_details, monthly_ai_details):
        day = detail["Day"]  # 例如 "02-01"
        on_time = detail["OnTime"]
        on_time_ai = ai_detail["OnTime"]
        daily_saving = on_time - on_time_ai
        monthly_data["on_time"][day] = on_time
        monthly_data["on_time_ai"][day] = on_time_ai
        monthly_data["daily_saving"][day] = daily_saving

    # 創建感應器
    sensors = [
        TotalOnTimeSensor(hass, entry, "monthly_on_time", monthly_on_time),
        TotalOnTimeSensor(hass, entry, "monthly_on_time_ai", monthly_on_time_ai),
        TotalOnTimeSensor(hass, entry, "ai_saving", ai_saving),
        MonthlyDataSensor(hass, entry, month_key, monthly_data)
    ]

    # 加入感應器
    async_add_entities(sensors)

    # 加入感應器
    async_add_entities(sensors)
