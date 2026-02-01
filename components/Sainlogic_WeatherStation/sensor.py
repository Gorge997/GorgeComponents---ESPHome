import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    UNIT_CELSIUS, 
    UNIT_PERCENT, 
    UNIT_DEGREES, 
    STATE_CLASS_MEASUREMENT, 
    STATE_CLASS_TOTAL_INCREASING,
    DEVICE_CLASS_TEMPERATURE, 
    DEVICE_CLASS_HUMIDITY, 
    DEVICE_CLASS_ILLUMINANCE
)
# IMPORTANTE: I nomi qui devono corrispondere a __init__.py
from . import SainlogicStation, sainlogic_ns 

TYPES = {
    "wind_direction":  sensor.sensor_schema(unit_of_measurement=UNIT_DEGREES, icon="mdi:compass", accuracy_decimals=0),
    "wind_avg":        sensor.sensor_schema(unit_of_measurement="m/s", icon="mdi:weather-windy", accuracy_decimals=1),
    "wind_gust":       sensor.sensor_schema(unit_of_measurement="m/s", icon="mdi:weather-gusts", accuracy_decimals=1),
    "rain_instant":    sensor.sensor_schema(unit_of_measurement="mm", icon="mdi:weather-rainy", accuracy_decimals=2),
    "rain_total":      sensor.sensor_schema(unit_of_measurement="mm", icon="mdi:weather-pouring", state_class=STATE_CLASS_TOTAL_INCREASING),
    "temperature":     sensor.sensor_schema(unit_of_measurement=UNIT_CELSIUS, device_class=DEVICE_CLASS_TEMPERATURE),
    "humidity":        sensor.sensor_schema(unit_of_measurement=UNIT_PERCENT, device_class=DEVICE_CLASS_HUMIDITY),
    "lux":             sensor.sensor_schema(unit_of_measurement="lx", device_class=DEVICE_CLASS_ILLUMINANCE),
    "uv_index":        sensor.sensor_schema(unit_of_measurement="index", icon="mdi:sun-wireless", accuracy_decimals=1),
}

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(sainlogic_ns): cv.use_id(SainlogicStation),
    **{cv.Optional(t): TYPES[t] for t in TYPES}
})

async def to_code(config):
    parent = await cg.get_variable(config[sainlogic_ns])
    for key in TYPES:
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(getattr(parent, f"set_{key}_sensor")(sens))