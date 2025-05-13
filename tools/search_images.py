import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger.logger_config import logging
from exception.custom_exception import CustomException

class PexelsImages:
    API_KEY = os.getenv("PEXELS_API_KEY")  # Use environment variable if available
    BASE_URL = "https://api.pexels.com/v1/search"
    @classmethod
    def search_images(cls, query, per_page=6):
        try:
            logging.info(f"Searching images on Pexels with query: {query}")
            headers = {"Authorization": cls.API_KEY}
            params = {"query": query, "per_page": per_page}
            response = requests.get(cls.BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            images = response.json().get("photos", [])
            #return images
            
            valid_images = []
            
            for image in images:
                image_url = image.get("src", {}).get("original")  # Use 'original' for the highest quality image
                if cls.is_image_url_valid(image_url):
                    valid_images.append(image_url)
                else:
                    logging.info(f"Image URL {image_url} is not valid. Searching for another valid image.")
            
            if not valid_images:
                logging.warning("No valid images found.")
                return None
            
            logging.info("Images searched successfully.")
            return valid_images
        
        except Exception as e:
            logging.error("Failed to search images from Pexels.")
            raise CustomException(sys, e)

    @staticmethod
    def is_image_url_valid(url: str) -> bool:
        """
        Check if the image URL returns a valid image response (status code 200 and image content-type).
        """
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            logging.info(f"Image URL: {url}")
            logging.info(f"Response: {response.status_code}")
            content_type = response.headers.get('Content-Type', '')
            logging.info(f"Content-Type: {content_type}")
            return response.status_code == 200 and content_type.startswith('image/')
        except Exception as e:
            logging.warning(f"Invalid image URL check failed: {url} → {e}")
            return False
        