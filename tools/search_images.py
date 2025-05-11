import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import WikipediaTools # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException

class WikiImages:
    @classmethod
    def search_images(cls):
        try:
            logging.info("Searching images using WikipediaTools.")
            images = WikipediaTools.search_images
            logging.info("Images searched successfully.")
            return images
        except Exception as e:
            logging.info("Failed to search images from Wikipedia.")
            raise CustomException(sys, e)