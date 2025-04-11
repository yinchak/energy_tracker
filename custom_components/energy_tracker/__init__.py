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

    # 儲存數據到 entry.data，畀 sensor.py 用
    entry.data["energy_data"] = data

    # 設置感應器
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
