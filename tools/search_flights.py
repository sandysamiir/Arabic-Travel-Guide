import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import AmadeusTools  # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException

class SearchFlights:
    @classmethod
    def search_flights_tool(cls):
        try:
            logging.info("Initiating flight search using AmadeusTools.")
            search_flights = AmadeusTools.search_flights
            logging.info("Flight search initiated successfully.")
            return search_flights
        except Exception as e:
            logging.info("Failed to initiate flight search.")
            raise CustomException(sys, e)
