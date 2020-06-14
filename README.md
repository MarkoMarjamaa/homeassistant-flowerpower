# homeassistant-flowerpower
Home Assistant Custom component for Parrot FlowerPower

This is offered AS IS. I'm not going to continue updating this. Feel free to fork. 

FlowerPower has very limited BLE technical documentantion, but for version 1. I have version 2.0.3 so this mainly works with that version. Different versions have different attibutes so your version might not work with this. This version did not give any moisture %, and I think that's because my device is already broken. I release this code, so other's don't have to rewrite it. 

## Installation

1. Find out the MAC address of your FlowerPower with `hcitool lescan`.
1. Put `__init__.py`, `sensor.py`, `manifest.json` into `<config>/custom_components/parrot_flowerpower/` on your home assistant installation (where `<config>` is the directory where your config file resides).
1. Add the following to your `configuration.yaml` (or modify your `sensor` heading, if you already have one):
```yaml
sensor:
  - platform: parrot_flowerpower
    mac: 00:11:22:AA:BB:CC # replace with MAC of your FlowerPower
```
Then restart Home Assistant and if everything works, you'll have some new sensors.
