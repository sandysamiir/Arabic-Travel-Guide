# agents/web_research_agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import Agent # type: ignore
from utils.main_utils import LoadModel
from logger.logger_config import logging
from exception.custom_exception import CustomException
from tools.serper_search import SerperSearch
from tools.search_articles import WikiArticles
from tools.search_images import WikiImages


class WebResearchAgent:
    @classmethod
    def initialize_web_research_agent(cls):
        """
        Initializes and returns the Web Research Agent.
        """
        try:
            logging.info("Initializing Web Research Agent.")
            web_research_agent = Agent(
                role="Web Research Agent",
                goal="Research destinations and find relevant images",
                attributes="diligent, thorough, comprehensive, visual-focused",
                llm=LoadModel.load_openai_model(),
                tools=[SerperSearch.search_web(), WikiArticles.fetch_articles(), WikiImages.search_images()],
            )
            logging.info("Web Research Agent initialized successfully.")
            return web_research_agent

        except Exception as e:
            logging.info("Error initializing Web Research Agent")
            raise CustomException(sys, e)