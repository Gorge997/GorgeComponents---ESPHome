#pragma once
#include "esphome.h"

class MeteoStation : public esphome::PollingComponent {
 private:
  unsigned long last_fast_update = 0;
  const unsigned long FAST_INTERVAL = 15000; // 15 secondi

  // Variabili di accumulo per medie e massimi
  float temp_sum = 0, hum_sum = 0, lux_sum = 0, uv_sum = 0, wind_sum = 0;
  float max_gust = 0;
  int samples_count = 0;

  // Variabile persistente per la pioggia (mm totali dall'avvio)
  float rain_total_acc = 0; 

 public:
  // Puntatori ai sensori definiti in ESPHome
  esphome::binary_sensor::BinarySensor *battery_s{nullptr};
  esphome::sensor::Sensor *wind_dir_s{nullptr};
  esphome::sensor::Sensor *wind_avg_s{nullptr};
  esphome::sensor::Sensor *wind_gust_s{nullptr};
  esphome::sensor::Sensor *rain_inst_s{nullptr};
  esphome::sensor::Sensor *rain_tot_s{nullptr};
  esphome::sensor::Sensor *temp_s{nullptr};
  esphome::sensor::Sensor *hum_s{nullptr};
  esphome::sensor::Sensor *lux_s{nullptr};
  esphome::sensor::Sensor *uv_s{nullptr};

  // Setters (usati dai file Python per collegare i sensori)
  void set_battery_sensor(esphome::binary_sensor::BinarySensor *s) { battery_s = s; }
  void set_wind_direction_sensor(esphome::sensor::Sensor *s) { wind_dir_s = s; }
  void set_wind_avg_sensor(esphome::sensor::Sensor *s) { wind_avg_s = s; }
  void set_wind_gust_sensor(esphome::sensor::Sensor *s) { wind_gust_s = s; }
  void set_rain_instant_sensor(esphome::sensor::Sensor *s) { rain_inst_s = s; }
  void set_rain_total_sensor(esphome::sensor::Sensor *s) { rain_tot_s = s; }
  void set_temperature_sensor(esphome::sensor::Sensor *s) { temp_s = s; }
  void set_humidity_sensor(esphome::sensor::Sensor *s) { hum_s = s; }
  void set_lux_sensor(esphome::sensor::Sensor *s) { lux_s = s; }
  void set_uv_index_sensor(esphome::sensor::Sensor *s) { uv_s = s; }

  // Frequenza di update definita nel YAML (60s)
  MeteoStation() : PollingComponent(60000) {}

  void setup() override {
    ESP_LOGI("meteo", "Avvio Multi-Sensore Meteo...");
  }

  // --- LOOP (Eseguito continuamente) ---
  void loop() override {
    unsigned long now = millis();
    if (now - last_fast_update >= FAST_INTERVAL) {
      last_fast_update = now;
      read_sensors_fast();
    }
  }

  // Lettura ogni 15 secondi
  void read_sensors_fast() {
    ESP_LOGD("meteo", "Campionamento sensori (15s)");

    // --- LOGICA DI LETTURA REALE ---
    // Qui dovrai inserire le tue chiamate ai pin (es. analogRead o I2C)
    float c_temp = 25.0; // Esempio
    float c_wind = 2.5;  // Esempio
    float c_rain = 0.2;  // Esempio mm caduti negli ultimi 15s

    // Accumulo dati
    temp_sum += c_temp;
    wind_sum += c_wind;
    if (c_wind > max_gust) max_gust = c_wind;
    
    rain_total_acc += c_rain; // Incrementa il totale
    samples_count++;
  }

  // --- UPDATE (Eseguito ogni 60s) ---
  void update() override {
    ESP_LOGI("meteo", "Pubblicazione dati al server...");

    if (samples_count > 0) {
      if (temp_s) temp_s->publish_state(temp_sum / samples_count);
      if (wind_avg_s) wind_avg_s->publish_state(wind_sum / samples_count);
      if (wind_gust_s) wind_gust_s->publish_state(max_gust);
      if (rain_tot_s) rain_tot_s->publish_state(rain_total_acc);
      
      // Valori booleani o istantanei
      if (battery_s) battery_s->publish_state(true); 
      if (wind_dir_s) wind_dir_s->publish_state(180); // Esempio Sud
    }

    // Reset accumulatori per il prossimo minuto
    temp_sum = 0; hum_sum = 0; lux_sum = 0; uv_sum = 0; wind_sum = 0;
    max_gust = 0; samples_count = 0;
  }
};