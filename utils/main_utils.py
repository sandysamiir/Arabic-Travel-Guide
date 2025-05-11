import sys
import os
from taskflowai import OpenaiModels, set_verbosity # type: ignore
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException


# Load environment variables
load_dotenv()

# Validate required API keys
required_keys = [
    "OPENAI_API_KEY"
]

# Check for missing keys
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    raise CustomException(sys, "Missing required environment variables: " + ', '.join(missing_keys))

# Set verbosity for taskflowai
set_verbosity(True)

class LoadModel:
    @classmethod
    def load_openai_model(cls):
        """
        Load and return the OpenAI GPT-3.5-turbo model.
        """
        try:
            logging.info("Loading OpenAI GPT-3.5-turbo model.")
            model = OpenaiModels.gpt_3_5_turbo
            logging.info("OpenAI GPT-3.5-turbo model loaded successfully.")
            return model
        except Exception as e:
            logging.info("Failed to load OpenAI GPT-3.5-turbo model")
            raise CustomException(sys, e)