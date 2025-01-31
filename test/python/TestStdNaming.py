import pytest,sys,os

current_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(current_dir, '../../src/python'))
sys.path.append(module_path)

from util.NamingConstants import *

@pytest.mark.parametrize("input_name, expected_output", [
           ('1_Temperature', '1_TEMPERATURE'),
           ('1_VWC', '1_VWC'),
           ('2_Temperature', '2_TEMPERATURE'),
           ('2_VWC', '2_VWC'),
           ('3_Temperature', '3_TEMPERATURE'),
           ('3_VWC', '3_VWC'),
           ('4_Temperature', '4_TEMPERATURE'),
           ('4_VWC', '4_VWC'),
           ('5_Temperature', '5_TEMPERATURE'),
           ('5_VWC', '5_VWC'),
           ('6_Temperature', '6_TEMPERATURE'),
           ('6_VWC', '6_VWC'),
           ('8_AirPressure', '8_AIR_PRESSURE'),
           ('8_AirTemperature', '8_AIR_TEMPERATURE'),
           ('8_HumiditySensorTemperature', '8_HUMIDITY_SENSOR_TEMPERATURE'),
           ('8_Precipitation', '8_PRECIPITATION'),
           ('8_RH', '8_RH'),
           ('8_Solar', '8_SOLAR'),
           ('8_Strikes', '8_STRIKES'),
           ('8_VaporPressure', '8_VAPOR_PRESSURE'),
           ('8_WindDirection', '8_WIND_DIRECTION'),
           ('8_WindGustSpeed', '8_WIND_GUST_SPEED'),
           ('8_WindSpeed', '8_WIND_SPEED'),
           ('Access_technology', 'ACCESS_TECHNOLOGY'),
           ('accMotion', 'ACC_MOTION'),
           ('Actuator', 'ACTUATOR'),
           ('adc_ch1', 'ADC_CH_1'),
           ('adc_ch2', 'ADC_CH_2'),
           ('adc_ch3', 'ADC_CH_3'),
           ('adc_ch4', 'ADC_CH_4'),
           ('airTemp', 'AIR_TEMPERATURE'),
           ('airtemperature', 'AIR_TEMPERATURE'),
           ('airTemperature', 'AIR_TEMPERATURE'),
           ('altitude', 'ALTITUDE'),
           ('Ana', 'ANA'),
           ('atmosphericpressure', 'ATMOSPHERIC_PRESSURE'),
           ('atmosphericPressure', 'ATMOSPHERIC_PRESSURE'),
           ('Average_current', 'AVERAGE_CURRENT'),
           ('average-flow-velocity0_0_m/s', 'AVERAGE_FLOW_VELOCITY_0_0_MS'),
           ('Average_voltage', 'AVERAGE_V'),
           ('Average_Voltage', 'AVERAGE_V'),
           ('Average_Wind_Speed_', 'AVERAGE_WIND_SPEED'),
           ('avgWindDegrees', 'AVERAGE_WIND_DEGREES'),
           ('barometricPressure', 'BAROMETRIC_PRESSURE'),
           ('batmv', 'BATMV'),
           ('battery', 'BATTERY'),
           ('Battery (A)', 'BATTERY_A'),
           ('battery (v)', 'BATTERY_V'),
           ('Battery (V)', 'BATTERY_V'),
           ('batteryVoltage', 'BATTERY_V'),
           ('battery-voltage_V', 'BATTERY_V'),
           ('Battery (W)', 'BATTERY_W'),
           ('Cable', 'CABLE'),
           ('charging-state', 'CHARGING_STATE'),
           ('Class', 'CLASS'),
           ('command', 'COMMAND'),
           ('conductivity', 'CONDUCTIVITY'),
           ('counterValue', 'COUNTER_VALUE'),
           ('current-flow-velocity0_0_m/s', 'CURRENT_FLOW_VELOCITY_0_0_MS'),
           ('depth', 'DEPTH'),
           ('Device', 'DEVICE'),
           ('DI0', 'DI_0'),
           ('DI1', 'DI_1'),
           ('direction', 'DIRECTION'),
           ('distance', 'DISTANCE'),
           ('down630', 'DOWN_630'),
           ('down800', 'DOWN_800'),
           ('EC', 'EC'),
           ('externalTemperature', 'EXTERNAL_TEMPERATURE'),
           ('fault', 'FAULT'),
           ('Fraud', 'FRAUD'),
           ('gnss', 'GNSS'),
           ('gustspeed', 'GUST_SPEED'),
           ('gustSpeed', 'GUST_SPEED'),
           ('header', 'HEADER'),
           ('Humi', 'HUMI'),
           ('humidity', 'HUMIDITY'),
           ('Hygro', 'HYGRO'),
           ('Leak', 'LEAK'),
           ('linpar', 'LINPAR'),
           ('Max_current', 'MAX_CURRENT'),
           ('Maximum_Wind_Speed_', 'MAX_WIND_SPEED'),
           ('Max_voltage', 'MAX_V'),
           ('Min_current', 'MIN_CURRENT'),
           ('Minimum_Wind_Speed_', 'MIN_WIND_SPEED'),
           ('Min_voltage', 'MIN_V'),
           ('moisture1', 'MOISTURE_1'),
           ('moisture2', 'MOISTURE_2'),
           ('moisture3', 'MOISTURE_3'),
           ('moisture4', 'MOISTURE_4'),
           ('ndvi', 'NDVI'),
           ('O06 / DPI-144', 'O_06_DPI_144'),
           ('Operating_cycle', 'OPERATING_CYCLE'),
           ('packet-type', 'PACKET_TYPE'),
           ('period', 'PERIOD'),
           ('Power', 'POWER'),
           ('precipitation', 'PRECIPITATION'),
           ('pressure', 'PRESSURE'),
           ('Processor_temperature', 'PROCESSOR_TEMPERATURE'),
           ('pulse_count', 'PULSE_COUNT'),
           ('Radio_channel_code', 'RADIO_CHANNEL_CODE'),
           ('Rainfall', 'RAINFALL'),
           ('rain_per_interval', 'RAIN_PER_INTERVAL'),
           ('Rain_per_interval', 'RAIN_PER_INTERVAL'),
           ('raw_depth', 'RAW_DEPTH'),
           ('rawSpeedCount', 'RAW_SPEED_COUNT'),
           ('relativehumidity', 'RELATIVE_HUMIDITY'),
           ('relativeHumidity', 'RELATIVE_HUMIDITY'),
           ('Rest_capacity', 'REST_CAPACITY'),
           ('Rest_power', 'REST_POWER'),
           ('rssi', 'RSSI'),
           ('rtc', 'RTC'),
           ('RTC', 'RTC'),
           ('S1_EC', 'S_1_EC'),
           ('S1_Temp', 'S_1_TEMPERATURE'),
           ('S1_Temp_10cm', 'S_1_TEMPERATURE_10_CM'),
           ('S1_Temp_20cm', 'S_1_TEMPERATURE_20_CM'),
           ('S1_Temp_30cm', 'S_1_TEMPERATURE_30_CM'),
           ('S1_Temp_40cm', 'S_1_TEMPERATURE_40_CM'),
           ('S1_Temp_50cm', 'S_1_TEMPERATURE_50_CM'),
           ('S1_Temp_60cm', 'S_1_TEMPERATURE_60_CM'),
           ('S1_Temp_70cm', 'S_1_TEMPERATURE_70_CM'),
           ('S1_Temp_80cm', 'S_1_TEMPERATURE_80_CM'),
           ('S1_Temp_90cm', 'S_1_TEMPERATURE_90_CM'),
           ('S1_VWC', 'S_1_VWC'),
           ('s4solarRadiation', 'S_4_SOLAR_RADIATION'),
           ('salinity', 'SALINITY'),
           ('salinity1', 'SALINITY_1'),
           ('salinity2', 'SALINITY_2'),
           ('salinity3', 'SALINITY_3'),
           ('salinity4', 'SALINITY_4'),
           ('sensorReading', 'SENSOR_READING'),
           ('shortest_pulse', 'SHORTEST_PULSE'),
           ('Signal', 'SIGNAL'),
           ('Signal_indication', 'SIGNAL_INDICATION'),
           ('Signal_strength', 'SIGNAL_STRENGTH'),
           ('snr', 'SNR'),
           ('soilmoist', 'SOIL_MOISTURE'),
           ('soiltemp', 'SOIL_TEMPERATURE'),
           ('solar', 'SOLAR'),
           ('Solar (A)', 'SOLAR_A'),
           ('solarpanel', 'SOLAR_PANEL'),
           ('solarPanel', 'SOLAR_PANEL'),
           ('solar (v)', 'SOLAR_V'),
           ('Solar (V)', 'SOLAR_V'),
           ('solar-voltage_V', 'SOLAR_V'),
           ('Solar (W)', 'SOLAR_W'),
           ('solmv', 'SOLMV'),
           ('sq110_umol', 'SQ_110_UMOL'),
           ('strikes', 'STRIKES'),
           ('Tamper', 'TAMPER'),
           ('tdskcl', 'TDSKCL'),
           ('Temp', 'TEMPERATURE'),
           ('temperature', 'TEMPERATURE'),
           ('Temperature', 'TEMPERATURE'),
           ('temperature1', 'TEMPERATURE_1'),
           ('temperature2', 'TEMPERATURE_2'),
           ('temperature3', 'TEMPERATURE_3'),
           ('temperature4', 'TEMPERATURE_4'),
           ('temperature5', 'TEMPERATURE_5'),
           ('temperature6', 'TEMPERATURE_6'),
           ('temperature7', 'TEMPERATURE_7'),
           ('temperature8', 'TEMPERATURE_8'),
           ('temperatureReading', 'TEMPERATURE_READING'),
           ('tilt-anlge0_0_Degrees', 'TILT_ANLGE_0_0_DEGREES'),
           ('UNIX_time', 'UNIX_TIME'),
           ('up630', 'UP_630'),
           ('up800', 'UP_800'),
           ('uptime_s', 'UPTIME_S'),
           ('vapourpressure', 'VAPOUR_PRESSURE'),
           ('vapourPressure', 'VAPOUR_PRESSURE'),
           ('vdd', 'VDD'),
           ('Volt', 'V'),
           ('vt', 'VT'),
           ('VWC', 'VWC'),
           ('VWC1', 'VWC_1'),
           ('winddirection', 'WIND_DIRECTION'),
           ('windDirection', 'WIND_DIRECTION'),
           ('windKph', 'WIND_KPH'),
           ('windspeed', 'WIND_SPEED'),
           ('windSpeed', 'WIND_SPEED'),
           ('windStdDevDegrees', 'WIND_STD_DEV_DEGREES')
])


def test_clean_names(input_name, expected_output):
    result = clean_name(input_name)
    assert result == expected_output


