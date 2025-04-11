from homeassistant import config_entries
from homeassistant.const import CONF_FILE_PATH
import voluptuous as vol

DOMAIN = "energy_tracker"

class EnergyTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Energy Tracker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # 驗證用戶輸入嘅檔案路徑
            file_path = user_input[CONF_FILE_PATH]
            try:
                with open(file_path, "r") as file:
                    file.read()
            except Exception as e:
                errors["base"] = "invalid_file_path"
            else:
                return self.async_create_entry(
                    title="Energy Tracker",
                    data={CONF_FILE_PATH: file_path}
                )

        # 顯示表單畀用戶輸入 JSON 檔案路徑
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_FILE_PATH, default="/config/data.json"): str,
            }),
            errors=errors,
        )