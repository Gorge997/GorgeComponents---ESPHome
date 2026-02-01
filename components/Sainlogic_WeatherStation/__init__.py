import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

# Nome della piattaforma (deve corrispondere alla cartella)
CODEOWNERS = ["@Gorge997"]

sainlogic_ns = cg.esphome_ns.namespace('sainlogic_weather_station')
SainlogicStation = sainlogic_ns.class_('MeteoStation', cg.PollingComponent)

# Questa stringa è la chiave magica per collegare i sensori
CONF_SAINLOGIC_WEATHER_STATION_ID = "sainlogic_weather_station_id"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(SainlogicStation),
}).extend(cv.polling_component_schema('60s'))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add_global(cg.RawStatement('#include "Sainlogic_WeatherStation.h"'))