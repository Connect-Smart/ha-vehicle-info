import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

DOMAIN = "vehicle_info"

async def async_setup(hass: HomeAssistant, config: dict):
    async def handle_get_vehicle_data(call: ServiceCall):
        license_plate = call.data.get("license_plate")
        if not license_plate:
            _LOGGER.error("No license plate provided")
            return

        try:
            from vehicle import Vehicle
            v = Vehicle(license_plate)
            await v.async_update()
            data = {
                "brand": v.brand,
                "model": v.model,
                "type": v.type,
                "color": v.color,
                "year": v.year,
                "vin": v.vin,
            }
            hass.states.async_set(
                f"{DOMAIN}.{license_plate.replace('-', '').replace(' ', '').lower()}",
                v.brand,
                data
            )
        except Exception as e:
            _LOGGER.error(f"Error fetching vehicle data: {e}")
            hass.states.async_set(
                f"{DOMAIN}.{license_plate.replace('-', '').replace(' ', '').lower()}",
                "Error",
                {"error": str(e)}
            )

    hass.services.async_register(DOMAIN, "get_vehicle_data", handle_get_vehicle_data)
    return True
