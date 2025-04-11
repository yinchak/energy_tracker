import json
import aiofiles
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_FILE_PATH

DOMAIN = "energy_tracker"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Energy Tracker integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Energy Tracker from a config entry."""
    # 從 Config Entry 攞 JSON 檔案路徑
    file_path = entry.data[CONF_FILE_PATH]

    # 異步讀取 JSON 數據
    try:
        async with aiofiles.open(file_path, mode="r") as file:
            content = await file.read()
            data = json.loads(content)
    except Exception as e:
        hass.components.logger.error(f"無法讀取 JSON 檔案 {file_path}: {e}")
        return False

    # 提取總數據
    monthly_on_time = int(data.get("MonthlyOnTime", 0))
    monthly_on_time_ai = int(data.get("MonthlyOnTimeAI", 0))
    ai_saving = int(data.get("AISaving", 0))

    # 提取每日數據
    monthly_details = data.get("MonthlyOnTimeDetail", [])
    monthly_ai_details = data.get("MonthlyOnTimeAIDetail", [])

    # 創建感應器
    sensors = [
        TotalOnTimeSensor("monthly_on_time", monthly_on_time, entry.entry_id),
        TotalOnTimeSensor("monthly_on_time_ai", monthly_on_time_ai, entry.entry_id),
        TotalOnTimeSensor("ai_saving", ai_saving, entry.entry_id)
    ]

    # 為每個日子創建感應器（包括節省）
    for detail, ai_detail in zip(monthly_details, monthly_ai_details):
        day = detail["Day"]  # 例如 "02-01"
        on_time = detail["OnTime"]
        on_time_ai = ai_detail["OnTime"]
        daily_saving = on_time - on_time_ai  # 每日節省
        date_key = f"2025_{day.replace('-', '_')}"  # 例如 "2025_02_01"
        sensors.append(DailyOnTimeSensor(f"on_time_{date_key}", on_time, entry.entry_id))
        sensors.append(DailyOnTimeSensor(f"on_time_ai_{date_key}", on_time_ai, entry.entry_id))
        sensors.append(DailyOnTimeSensor(f"daily_saving_{date_key}", daily_saving, entry.entry_id))

    # 加入感應器
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    entry.runtime_data = sensors
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
