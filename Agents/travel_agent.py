# agents/travel_agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskflowai import Agent  # type: ignore
from utils.main_utils import LoadModel
from logger.logger_config import logging
from exception.custom_exception import CustomException
from tools.search_flights import SearchFlights
from tools.get_weather_data import GetWeatherData


class TravelAgent:
    @classmethod
    def initialize_travel_agent(cls):
        """
        Initializes and returns the Travel Agent.
        """
        try:
            logging.info("Initializing the Travel Agent.")

            travel_agent = Agent(
                role="وكيل السفر",  # Arabic for "Travel Agent"
                goal="مساعدة المسافرين في استفساراتهم",  # Arabic for "Assist travelers with their queries"
                attributes="ودود، مجتهد، ومفصل في تقديم التقارير للمستخدمين",  # Arabic for "friendly, hardworking, and detailed in reporting back to users"
                llm=LoadModel.load_groq_model("meta-llama/llama-4-scout-17b-16e-instruct"),
                tools=[
                    SearchFlights.search_flights_tool(),
                    GetWeatherData.fetch_weather_data()
                ]
            )

            logging.info("Travel Agent initialized successfully.")
            return travel_agent

        except Exception as e:
            logging.info("An unexpected error occurred")
            raise CustomException(sys, e)
