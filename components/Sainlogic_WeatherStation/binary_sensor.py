import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import CONF_ID
# Importiamo i nomi corretti e la costante ID dal file __init__
from . import SainlogicStation, sainlogic_ns, CONF_SAINLOGIC_WEATHER_STATION_ID

CONFIG_SCHEMA = binary_sensor.binary_sensor_schema().extend({
    cv.GenerateID(CONF_SAINLOGIC_WEATHER_STATION_ID): cv.use_id(SainlogicStation),
})

async def to_code(config):
    # Recuperiamo l'hub principale
    parent = await cg.get_variable(config[CONF_SAINLOGIC_WEATHER_STATION_ID])
    
    # Creiamo il sensore binario (es. batteria)
    var = await binary_sensor.new_binary_sensor(config)
    
    # Lo colleghiamo al C++ tramite la funzione set_battery_sensor
    cg.add(parent.set_battery_sensor(var))