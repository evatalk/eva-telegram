import os
from os.path import abspath, dirname, join

from dotenv import load_dotenv

import telepot

# Create .env file path.
BASE_PATH = abspath(join(dirname(__file__), os.pardir))

dotenv_path = join(BASE_PATH, '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
EVA_HOST_URL = os.getenv('EVA_HOST_URL')
DB = os.getenv("DB")

BOT = telepot.Bot(TELEGRAM_TOKEN)
