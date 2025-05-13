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
from tools.search_images import PexelsImages


class WebResearchAgent:
    @classmethod
    def initialize_web_research_agent(cls):
        """
        Initializes and returns the Web Research Agent.
        """

        try:
            logging.info("Initializing Web Research Agent.")
            web_research_agent = Agent(
                role="وكيل البحث على الويب",  # Arabic for "Web Research Agent"
                goal="البحث عن الوجهات والعثور على الصور ذات الصلة",  # Arabic for "Research destinations and find relevant images"
                attributes="مجتهد، شامل، دقيق، يركز على الصور",  # Arabic for "diligent, thorough, comprehensive, visual-focused"
                llm=LoadModel.load_groq_model("meta-llama/llama-4-scout-17b-16e-instruct"),
                tools=[SerperSearch.search_web(), 
                       WikiArticles.fetch_articles(), 
                       search_pexels_images
                       ]
            )
            logging.info("Web Research Agent initialized successfully.")
            return web_research_agent

        except Exception as e:
            logging.info("Error initializing Web Research Agent")
            raise CustomException(sys, e)
    
def search_pexels_images(query: str):
    """Searches for relevant images on Pexels for a given query."""
    return PexelsImages.search_images(query)    