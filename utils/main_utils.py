import sys
import os
from taskflowai import GroqModels, set_verbosity # type: ignore
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
from logger.logger_config import logging
from exception.custom_exception import CustomException

print(dir(GroqModels))
# Load environment variables
load_dotenv()

# Validate required API keys
required_keys = [
    "GROQ_API_KEY"
]

# Check for missing keys
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    raise CustomException(sys, "Missing required environment variables: " + ', '.join(missing_keys))

# Set verbosity for taskflowai
set_verbosity(True)

class LoadModel:
    @classmethod
    def load_groq_model(cls, model_name):
        """
        Load and return the Groq  model.
        """
        try:
            logging.info(f"Loading Groq {model_name} model.")
            model = GroqModels.custom_model(model_name=model_name)
            logging.info(f"Groq {model_name} model loaded successfully.")
            return model
        except Exception as e:
            logging.info(f"Failed to load Groq {model_name} model")
            raise CustomException(sys, e)