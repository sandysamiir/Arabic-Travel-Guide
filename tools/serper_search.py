import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import WebTools # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException

class SerperSearch:
    @classmethod
    def search_web(cls):
        try:
            logging.info("Performing web search using SerperSearch tool.")
            search = WebTools.serper_search
            logging.info("Web search completed successfully.")
            return search
        except Exception as e:
            logging.info("Failed to perform web search.")
            raise CustomException(sys, e)
