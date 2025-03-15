import undetected_chromedriver as webdriver
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils.email_utils import send_email
import os
from dotenv import load_dotenv

load_dotenv()

def paybot():
    try:
        driver = webdriver.Chrome()

        # nav to the login page for the specific shopify account
        print('opening new browser window and navigating to shopify login page')
        shopify_login_url = os.getenv('SHOPIFY_LOGIN_URL')
        driver.get(shopify_login_url)
        time.sleep(7)

        # find the email element, input the email and submit the email form
        print('entering shopify login email')
        shopify_email_el = driver.find_element(By.ID, 'account_email')
        shopify_email = os.getenv('SHOPIFY_EMAIL')
        shopify_email_el.send_keys(shopify_email)
        shopify_email_el.send_keys(Keys.RETURN)
        time.sleep(5)

        # find the password input field, input the password and submit the login form
        print('entering shopify login password')
        shopify_password_el = driver.find_element(By.ID, 'account_password')
        shopify_password = os.getenv('SHOPIFY_PASSWORD')
        shopify_password_el.send_keys(shopify_password)
        shopify_password_el.send_keys(Keys.RETURN)
        print('waiting for shopify page to load...')
        time.sleep(5)

        try:
            remind_me_link_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'remind-me-later-link')))
            print("'Remind me later' link found, clicking it")
            remind_me_link_el.click()
            time.sleep(30)
        except:
            print("'Remind me later' link not found, proceeding to iframe")

        iframe = driver.find_element(By.NAME, "app-iframe")
        driver.switch_to.frame(iframe)
        time.sleep(1)

        # select all the orders
        print("selecting all orders checkbox")
        all_orders_checkbox_el = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/table/thead/tr/th[1]/label/span')
        all_orders_checkbox_el.click()
        time.sleep(1)

        # click the pay all button
        print('clicking pay all button & waiting for stripe payment page to load')
        pay_all_orders_button_el = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/div/div/div/div[2]/button')
        pay_all_orders_button_el.click()
        time.sleep(5)

        # switch into Stripe window
        print('switching focus to current window for stripe page')
        current_window = driver.current_window_handle
        driver.switch_to.window(current_window)

        # fill out form on stripe page
        print('filling email in stripe form')
        stripe_email_el = driver.find_element(By.ID, 'email')
        stripe_email = os.getenv('STRIPE_EMAIL')
        stripe_email_el.send_keys(stripe_email)
        time.sleep(4)

        # close link verification popup
        link_verification_popup_el = driver.find_element(By.CLASS_NAME, "LinkVerificationHeader-cancelButton")
        link_verification_popup_el.click()
        time.sleep(3)

        print('filling name in stripe form')
        stripe_name_el = driver.find_element(By.NAME, 'name')
        stripe_name = os.getenv('STRIPE_NAME')
        stripe_name_el.send_keys(stripe_name)
        time.sleep(1)

        print('entering promo code')
        stripe_promo_code_el = driver.find_element(By.ID, 'promotionCode')
        stripe_promo_code = os.getenv('STRIPE_PROMO_CODE')
        stripe_promo_code_el.send_keys(stripe_promo_code)
        time.sleep(3)

        # apply promo code
        print("clicking apply button for promo code")
        stripe_promo_apply_el = driver.find_element(By.CLASS_NAME, 'PromotionCodeEntry-applyButton')
        stripe_promo_apply_el.click()
        time.sleep(4)

        print('filling card number in stripe form')
        stripe_cardnumber_el = driver.find_element(By.ID, 'cardNumber')
        stripe_cardnumber = os.getenv('STRIPE_CARD_NUMBER')
        stripe_cardnumber_el.send_keys(stripe_cardnumber)
        time.sleep(1)

        print('filling card expiration in stripe form')
        stripe_card_expiry_el = driver.find_element(By.ID, 'cardExpiry')
        stripe_card_expiry_num = os.getenv('STRIPE_CARD_EXP')
        stripe_card_expiry_el.send_keys(stripe_card_expiry_num)
        time.sleep(1)

        print('filling cvc in stripe form')
        stripe_card_cvc_el = driver.find_element(By.ID, 'cardCvc')
        stripe_card_cvc_num = os.getenv('STRIPE_CSV')
        stripe_card_cvc_el.send_keys(stripe_card_cvc_num)
        time.sleep(1)

        print('filling cardholder name in stripe form')
        stripe_cardholder_name_el = driver.find_element(By.ID, 'billingName')
        stripe_cardholder_name = os.getenv('STRIPE_NAME')
        stripe_cardholder_name_el.send_keys(stripe_cardholder_name)
        time.sleep(1)

        print('filling address line1 in stripe form')
        stripe_billing_address1_el = driver.find_element(By.ID, 'billingAddressLine1')
        stripe_billing_address1 = os.getenv('STRIPE_ADDR_!')
        stripe_billing_address1_el.send_keys(stripe_billing_address1)
        time.sleep(1)

        print('filling billing city in stripe form')
        stripe_billing_city_el = driver.find_element(By.ID, 'billingLocality')
        stripe_billing_city = os.getenv('STRIPE_CITY')
        stripe_billing_city_el.send_keys(stripe_billing_city)
        time.sleep(1)

        print('filling zip code in stripe form')
        stripe_billing_zip_el = driver.find_element(By.ID, 'billingPostalCode')
        stripe_billing_zip = os.getenv('STRIPE_ZIP')
        stripe_billing_zip_el.send_keys(stripe_billing_zip)
        time.sleep(2)

        try:
            print('checking for stripepass box')
            stripe_checkbox_el = driver.find_element(By.ID, 'enableStripePass')
            stripe_checkbox_el.click()
            time.sleep(5)
        except:
            pass

        print('clicking pay button')
        stripe_pay_button = driver.find_element(By.CLASS_NAME, 'SubmitButton')
        stripe_pay_button.click()
        time.sleep(18)

        send_email("Nolonger PayBot Ran Successfully",  f"Nolonger PayBot ran sucessfully.")
            
    except Exception as e:
        print("paying for stripe failed")
        error_message = traceback.format_exc()
        send_email("Nolonger Bot Failed", error_message)
        
        driver.quit()

if __name__ == '__main__':
    paybot()