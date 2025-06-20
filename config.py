from dotenv import load_dotenv
import os
from utils.email_utils import send_email
import time, traceback, requests, logging
from datetime import datetime

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
FIND_ORDERS_URL = os.getenv('FIND_ORDERS_URL')
SHOPIFY_LOGIN_URL = os.getenv('SHOPIFY_LOGIN_URL')
SHOPIFY_EMAIL = os.getenv('SHOPIFY_EMAIL')
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
STRIPE_EMAIL = os.getenv('STRIPE_EMAIL')
STRIPE_NAME = os.getenv('STRIPE_NAME')
STRIPE_PROMO_CODE = os.getenv('STRIPE_PROMO_CODE')
STRIPE_CARD_NUMBER = os.getenv('STRIPE_CARD_NUMBER')
STRIPE_CARD_EXP = os.getenv('STRIPE_CARD_EXP')
STRIPE_CSV = os.getenv('STRIPE_CSV')
STRIPE_ADDR_1 = os.getenv('STRIPE_ADDR_1')
STRIPE_CITY = os.getenv('STRIPE_CITY')
STRIPE_ZIP = os.getenv('STRIPE_ZIP')

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = os.path.join(LOG_DIR, f'log_{timestamp}.log')

LOG_LEVEL = logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)