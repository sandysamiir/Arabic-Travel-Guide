import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import WikipediaTools # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException

class WikiArticles:
    @classmethod
    def fetch_articles(cls):
        try:
            logging.info("Fetching articles using WikipediaTools.")
            articles = WikipediaTools.search_articles
            logging.info("Articles fetched successfully.")
            return articles
        except Exception as e:
            logging.info("Failed to fetch articles from Wikipedia.")
            raise CustomException(sys, e)