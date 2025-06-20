from paybot import paybot
from config import *

url = FIND_ORDERS_URL

def find_orders():
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            orders_data = response.json()
            orders = orders_data.get('data', {}).get('docs', [])
            
            order_numbers = [order["shopify_order_number"] for order in orders if order.get("fulfillment_status") != "refunded"]
        
            if order_numbers:
                paybot()
                logging.info(f'New orders found, executing paybot')
            else:
                logging.info('No new orders found.')
        
        else:
            logging.error(f"Failed to fetch data. Status code: {response.status_code}")

    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
        send_email("Nolonger paybot failed to check for new orders.", f"Error message: {e}")

if __name__ == '__main__':
    find_orders()
