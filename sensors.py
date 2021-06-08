import Adafruit_DHT
import time
import pytz
import serial
from datetime import datetime

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
# Ouverture du port serie avec :
# '/dev/ttyXXXX' : definition du port d ecoute (remplacer 'X' par le bon nom)
# 9600 : vitesse de communication
serialArduino = serial.Serial('/dev/ttyUSB0', 9600)

class sensors:

    def get_readings(self):
        # DHT22
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        tz_Paris = pytz.timezone('Europe/Paris')
        datetime_Paris = datetime.now(tz_Paris)
        time_str = datetime_Paris.strftime("%Y-%m-%d %H:%M:%S")

        # Analogic sensor from arduino
        serialOutput = serialArduino.readline()
        serialOutput = str(serialOutput, 'ascii')
        serialOutput = serialOutput.replace(' ', '')
        serialOutputArray = serialOutput.split("-")
        soilHumidity = serialOutputArray[0].replace('hum:', '')
        lux = serialOutputArray[1].replace('lux:', '')

        return {
            "time": time_str,
            "temperature": temperature,
            "humidity": humidity,
            "brightness": lux,
            "soilHumidity": soilHumidity
        }




