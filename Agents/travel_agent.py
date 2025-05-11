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
        try:
            logging.info("Initializing the Travel Agent.")

            travel_agent = Agent(
                role="Travel Agent",
                goal="Assist travelers with their queries",
                attributes="friendly, hardworking, and detailed in reporting back to users",
                llm=LoadModel.load_openai_model(),
                tools=[SearchFlights.search_flights_tool(), GetWeatherData.fetch_weather_data()
                    
                ]
            )

            logging.info("Travel Agent initialized successfully.")
            return travel_agent

        except Exception as e:
            logging.info("An unexpected error occurred")
            raise CustomException(sys, e)
