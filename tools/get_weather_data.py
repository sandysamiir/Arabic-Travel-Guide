import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import WebTools # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException

class GetWeatherData:
    @classmethod
    def fetch_weather_data(cls):
        try:
            logging.info("Fetching weather data using WebTools.")
            weather_data = WebTools.get_weather_data
            logging.info(f"Weather data fetched successfully. {weather_data}")
            return weather_data
        except Exception as e:
            logging.info("Failed to fetch weather data.")
            raise CustomException(sys, e)
