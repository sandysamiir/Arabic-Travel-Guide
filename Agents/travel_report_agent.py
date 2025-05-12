# agents/travel_report_agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import Agent # type: ignore
from utils.main_utils import LoadModel
from logger.logger_config import logging
from exception.custom_exception import CustomException
import sys

class TravelReportAgent:
    @classmethod
    def initialize_travel_report_agent(cls):
        """
        Initializes and returns the Travel Report Agent.
        """
        try:
            logging.info("Initializing the Travel Report Agent.")

            travel_report_agent = Agent(
                role="وكيل تقارير السفر",  # Arabic for "Travel Report Agent"
                goal="كتابة تقارير سفر شاملة مع عناصر مرئية",  # Arabic for "Write comprehensive travel reports with visual elements"
                attributes="ودود، مجتهد، يركز على العناصر المرئية، ومفصل في إعداد التقارير",  # Arabic for "friendly, hardworking, visual-oriented, and detailed in reporting"
                llm=LoadModel.load_groq_model("meta-llama/llama-4-maverick-17b-128e-instruct")
            )

            logging.info("Travel Report Agent initialized successfully.")
            return travel_report_agent

        except Exception as e:
            logging.info("An unexpected error occurred")
            raise CustomException(sys, e)
