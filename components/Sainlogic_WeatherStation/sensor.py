import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID, UNIT_CELSIUS, UNIT_PERCENT, UNIT_DEGREES,
    STATE_CLASS_MEASUREMENT, STATE_CLASS_TOTAL_INCREASING,
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_ILLUMINANCE
)
# Importiamo la costante e la classe
from . import SainlogicStation, sainlogic_ns, CONF_SAINLOGIC_WEATHER_STATION_ID

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

# CORREZIONE: Usiamo la stringa costante come chiave
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_SAINLOGIC_WEATHER_STATION_ID): cv.use_id(SainlogicStation),
}).extend({cv.Optional(t): TYPES[t] for t in TYPES})

async def to_code(config):
    # Recuperiamo l'hub tramite l'ID salvato nella stringa costante
    parent = await cg.get_variable(config[CONF_SAINLOGIC_WEATHER_STATION_ID])
    
    for key in TYPES:
        if key in config:
            sens = await sensor.new_sensor(config[key])
            # Esegue: parent->set_xxx_sensor(sens);
            cg.add(getattr(parent, f"set_{key}_sensor")(sens))