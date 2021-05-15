import Adafruit_DHT
import time
import pytz
from datetime import datetime

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

class captors:

    def get_readings(self):
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        tz_Paris = pytz.timezone('Europe/Paris')
        datetime_Paris = datetime.now(tz_Paris)
        time_str = datetime_Paris.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "time": time_str,
            "temperature": temperature,
            "humidity": humidity
        }




