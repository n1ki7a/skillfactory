import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

keys = {
    'доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR'
}