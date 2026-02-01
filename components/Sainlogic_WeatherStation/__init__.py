import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

# Namespace C++ (deve corrispondere a quello che useresti in C++)
sainlogic_ns = cg.esphome_ns.namespace('sainlogic_weatherstation')
# Classe C++
SainlogicStation = sainlogic_ns.class_('MeteoStation', cg.PollingComponent)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(SainlogicStation),
}).extend(cv.polling_component_schema('60s'))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    # FORZA l'inclusione del file header rinominato
    cg.add_global(cg.RawStatement('#include "Sainlogic_WeatherStation.h"'))