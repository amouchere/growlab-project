try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from bmp280 import BMP280
import Adafruit_DHT
import time
import pytz
import serial
import logging
from datetime import datetime



DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
# Ouverture du port serie avec :
# '/dev/ttyXXXX' : definition du port d ecoute (remplacer 'X' par le bon nom)
# 9600 : vitesse de communication
serialArduino = serial.Serial('/dev/ttyUSB0', 9600)


class sensors:

    def __init__(self):
        self.bus = SMBus(1)
        self.sensor = BMP280(i2c_dev=self.bus)

    def get_readings(self):
        # DHT22
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        logging.info("DHT22 temp: {} & humidity: {}".format(temperature, humidity))
        tz_Paris = pytz.timezone('Europe/Paris')
        datetime_Paris = datetime.now(tz_Paris)
        time_str = datetime_Paris.strftime("%Y-%m-%d %H:%M:%S")

        # Analogic sensor from arduino
        serialOutput = serialArduino.readline()
        serialOutput = str(serialOutput, 'ascii')
        logging.info("Arduino serial: {}".format(serialOutput))
        serialOutput = serialOutput.replace(' ', '')
        serialOutput = serialOutput.replace('\r\n', '')
        serialOutputArray = serialOutput.split("-")
        soilHumidity = serialOutputArray[0].replace('hum:', '')
        lux = serialOutputArray[1].replace('lux:', '')
        soilHumiditypercent = serialOutputArray[2].replace('humpercent:', '')

        # BMP280
         # Ignore first result since it seems stale
        temperatureBMP280 = 0
        pressure = 0
        try:
            temperatureBMP280 = self.sensor.get_temperature()
            pressure = self.sensor.get_pressure()
            time.sleep(0.1)

            temperatureBMP280 = self.sensor.get_temperature()
            pressure = self.sensor.get_pressure()

            logging.info("BMP280 pressure: {}".format(pressure))

        except Exception as e:
            logging.error(type(e).__name__)
            logging.exception(e)

        
        return {
            "time": time_str,
            "temperature": temperature,
            "temperatureBMP280": temperatureBMP280,
            "pressure": pressure,
            "humidity": humidity,
            "brightness": lux,
            "soilHumidity": soilHumidity,
            "soilHumidityPerCent": soilHumiditypercent
        }




