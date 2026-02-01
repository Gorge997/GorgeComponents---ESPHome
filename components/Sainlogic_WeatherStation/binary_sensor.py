from esphome.components import binary_sensor
import esphome.config_validation as cv
import esphome.codegen as cg
from . import MeteoStation, meteo_ns

CONFIG_SCHEMA = binary_sensor.binary_sensor_schema().extend({
    cv.GenerateID(meteo_ns): cv.use_id(MeteoStation),
})

async def to_code(config):
    parent = await cg.get_variable(config[meteo_ns])
    var = await binary_sensor.new_binary_sensor(config)
    cg.add(parent.set_battery_sensor(var))