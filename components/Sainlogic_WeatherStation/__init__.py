import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

# Definiamo il namespace e la classe
sainlogic_ns = cg.esphome_ns.namespace('sainlogic_weather_station')
SainlogicStation = sainlogic_ns.class_('MeteoStation', cg.PollingComponent)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(SainlogicStation),
}).extend(cv.polling_component_schema('60s'))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    # Il nome del file deve essere quello che hai sul repo
    cg.add_global(cg.RawStatement('#include "Sainlogic_WeatherStation.h"'))