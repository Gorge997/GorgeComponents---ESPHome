import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID, UNIT_CELSIUS, UNIT_PERCENT, UNIT_DEGREES,
    STATE_CLASS_MEASUREMENT, STATE_CLASS_TOTAL_INCREASING,
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_ILLUMINANCE
)
from . import SainlogicStation, sainlogic_ns

# Definiamo una stringa per l'ID del componente padre
CONF_SAINLOGIC_ID = "sainlogic_weather_station_id"

TYPES = {
    "temperature":     sensor.sensor_schema(unit_of_measurement=UNIT_CELSIUS, device_class=DEVICE_CLASS_TEMPERATURE, state_class=STATE_CLASS_MEASUREMENT),
    "humidity":        sensor.sensor_schema(unit_of_measurement=UNIT_PERCENT, device_class=DEVICE_CLASS_HUMIDITY, state_class=STATE_CLASS_MEASUREMENT),
    "wind_direction":  sensor.sensor_schema(unit_of_measurement=UNIT_DEGREES, icon="mdi:compass", accuracy_decimals=0),
    "wind_avg":        sensor.sensor_schema(unit_of_measurement="m/s", icon="mdi:weather-windy", accuracy_decimals=1),
    "wind_gust":       sensor.sensor_schema(unit_of_measurement="m/s", icon="mdi:weather-gusts", accuracy_decimals=1),
    "rain_instant":    sensor.sensor_schema(unit_of_measurement="mm", icon="mdi:weather-rainy", accuracy_decimals=2),
    "rain_total":      sensor.sensor_schema(unit_of_measurement="mm", icon="mdi:weather-pouring", state_class=STATE_CLASS_TOTAL_INCREASING),
    "lux":             sensor.sensor_schema(unit_of_measurement="lx", device_class=DEVICE_CLASS_ILLUMINANCE, state_class=STATE_CLASS_MEASUREMENT),
    "uv_index":        sensor.sensor_schema(unit_of_measurement="index", icon="mdi:sun-wireless", accuracy_decimals=1),
}

# La correzione: usiamo cv.use_id(SainlogicStation) associato a una stringa
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(SainlogicStation): cv.use_id(SainlogicStation),
}).extend({cv.Optional(t): TYPES[t] for t in TYPES})

async def to_code(config):
    # Recupera il componente padre tramite il suo ID di classe
    parent = await cg.get_variable(config[SainlogicStation])
    
    for key in TYPES:
        if key in config:
            sens = await sensor.new_sensor(config[key])
            # Il nome della funzione nel file .h deve essere set_NOME_sensor
            cg.add(getattr(parent, f"set_{key}_sensor")(sens))