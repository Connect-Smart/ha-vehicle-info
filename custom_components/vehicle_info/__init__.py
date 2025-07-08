import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .vehicle import RDW  # importeer de RDW class

_LOGGER = logging.getLogger(__name__)
DOMAIN = "vehicle_info"

async def async_setup(hass: HomeAssistant, config: dict):
    async def handle_get_vehicle_data(call: ServiceCall):
        license_plate = call.data.get("license_plate")
        if not license_plate:
            _LOGGER.error("No license plate provided")
            return

        try:
            rdw = RDW()
            vehicle = await rdw.vehicle(license_plate)
            # Haal gewenste attributen op. Zie models.py in Frenck's repo voor alle beschikbare.
            data = {
                "license_plate": vehicle.license_plate,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "type": vehicle.vehicle_type,
                "color": vehicle.color,
                "year": vehicle.year_of_manufacture,
                "vin": vehicle.vin_number,
                "rdw": vehicle.__dict__,  # Alles als attribuut (optioneel)
            }
            hass.states.async_set(
                f"{DOMAIN}.{license_plate.replace('-', '').replace(' ', '').lower()}",
                data["brand"],
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
    _LOGGER.error("DEBUG: vehicle_info async_setup is running!")
    return True
