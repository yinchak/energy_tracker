import json
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant

DOMAIN = "energy_tracker"

async def async_setup_platform(hass: HomeAssistant, config, async_add_entities: AddEntitiesCallback, discovery_info=None):
    # 假設 JSON 數據儲存喺一個檔案（要你調整路徑）
    try:
        with open("/path/to/your/data.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        hass.components.logger.error(f"無法讀取 JSON 檔案: {e}")
        return

    # 提取總數據
    monthly_on_time = int(data.get("MonthlyOnTime", 0))
    monthly_on_time_ai = int(data.get("MonthlyOnTimeAI", 0))
    ai_saving = int(data.get("AISaving", 0))

    # 提取每日數據
    monthly_details = data.get("MonthlyOnTimeDetail", [])
    monthly_ai_details = data.get("MonthlyOnTimeAIDetail", [])

    # 創建感應器
    sensors = [
        TotalOnTimeSensor("monthly_on_time", monthly_on_time),
        TotalOnTimeSensor("monthly_on_time_ai", monthly_on_time_ai),
        TotalOnTimeSensor("ai_saving", ai_saving)
    ]

    # 為每個日子創建感應器
    for detail, ai_detail in zip(monthly_details, monthly_ai_details):
        day = detail["Day"]  # 例如 "02-01"
        on_time = detail["OnTime"]
        on_time_ai = ai_detail["OnTime"]
        date_key = f"2025_{day.replace('-', '_')}"  # 例如 "2025_02_01"
        sensors.append(DailyOnTimeSensor(f"on_time_{date_key}", on_time))
        sensors.append(DailyOnTimeSensor(f"on_time_ai_{date_key}", on_time_ai))

    async_add_entities(sensors)