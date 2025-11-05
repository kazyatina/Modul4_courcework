from dotenv import load_dotenv
import os

load_dotenv()

ROOT_DIR = os.path.dirname(__file__)
FILE_JSON = os.path.join(ROOT_DIR, "data/products.json")
# USER_SETTINGS = os.path.join(ROOT_DIR, "user_settings.json")
API_KEY = os.getenv("API_KEY_currency")
# API_KEY_HH =
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")
URL = 'https://api.hh.ru/vacancies'