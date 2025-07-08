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
                "apk_expiration": str(vehicle.apk_expiration) if vehicle.apk_expiration else None,
                "ascription_date": str(vehicle.ascription_date) if vehicle.ascription_date else None,
                "ascription_possible": vehicle.ascription_possible,
                "energy_label": vehicle.energy_label,
                "engine_capacity": vehicle.engine_capacity,
                "exported": vehicle.exported,
                "first_admission": str(vehicle.first_admission) if vehicle.first_admission else None,
                "interior": str(vehicle.interior) if vehicle.interior else None,
                "last_odometer_registration_year": vehicle.last_odometer_registration_year,
                "liability_insured": vehicle.liability_insured,
                "list_price": vehicle.list_price,
                "mass_driveable": vehicle.mass_driveable,
                "mass_empty": vehicle.mass_empty,
                "number_of_cylinders": vehicle.number_of_cylinders,
                "number_of_doors": vehicle.number_of_doors,
                "number_of_seats": vehicle.number_of_seats,
                "number_of_wheelchair_seats": vehicle.number_of_wheelchair_seats,
                "number_of_wheels": vehicle.number_of_wheels,
                "odometer_judgement": str(vehicle.odometer_judgement) if vehicle.odometer_judgement else None,
                "pending_recall": vehicle.pending_recall,
                "taxi": vehicle.taxi,
                "vehicle_type": str(vehicle.vehicle_type) if vehicle.vehicle_type else None,
                "vin_number": vehicle.vin_number,
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
