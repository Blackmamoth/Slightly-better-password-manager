from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getlogin()
DB = os.environ.get('DB')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
ROOT_PASS = os.environ.get('ROOT_PASS')
KEY = os.environ.get('KEY')
