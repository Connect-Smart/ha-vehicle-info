# Home Assistant Vehicle Info

Deze integratie biedt een service `vehicle_info.get_vehicle_data` waarmee je via een kenteken voertuigdata kunt ophalen. De data verschijnt als een state object in Home Assistant.

## Installatie

### Via HACS (aanbevolen)
1. Voeg deze repository toe als custom repository in HACS (type: Integration).
2. Installeer `Vehicle Info`.
3. Herstart Home Assistant.

### Handmatig
1. Download de folder `vehicle_info` naar je `custom_components` folder.
2. Herstart Home Assistant.

## Gebruik

Ga naar Ontwikkelaarstools > Services en roep de service aan:
```yaml
service: vehicle_info.get_vehicle_data
data:
  license_plate: XX999X
