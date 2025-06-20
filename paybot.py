from config import *
from utils.selenium_setup import *

def paybot():
    try:
        driver = get_driver()

        browser_wait = WebDriverWait(driver, 15)

        def wait_clickable(by, value):
            return browser_wait.until(EC.element_to_be_clickable((by, value)))
        
        def wait_visible(by, value):
            return browser_wait.until(EC.visibility_of_element_located((by, value)))
                
        def wait_presence(by, value):
            return browser_wait.until(EC.presence_of_element_located((by, value)))

        def close_link_popup():
            try:
                logger.info("waiting for link verification popup to appear...")
                link_verification_popup_btn = wait_visible(By.CSS_SELECTOR, '.LinkActionButton.LinkActionButton--icon.LinkVerificationHeader-cancelButton')
                link_verification_popup_btn.click()
            except NoSuchElementException:
                logger.info("link verification popup not found, continuing")

        # nav to the login page for the specific shopify account
        logger.info('opening new browser window and navigating to shopify login page')
        driver.get(SHOPIFY_LOGIN_URL)

        shopify_login_email_field = wait_clickable(By.ID, "account_email")
        shopify_login_email_field.send_keys(SHOPIFY_EMAIL)
        email_next_btn = wait_clickable(By.NAME, 'commit')
        email_next_btn.click()

        shopify_login_password_field = wait_clickable(By.ID, "account_password")
        shopify_login_password_field.send_keys(SHOPIFY_PASSWORD)
        password_next_btn = wait_clickable(By.NAME, 'commit')
        password_next_btn.click()

        try:
            remind_me_link_el = wait_presence(By.CLASS_NAME, 'remind-me-later-link')
            logger.info("'Remind me later' link found, clicking it")
            remind_me_link_el.click()
        except:
            logger.info("'Remind me later' link not found, proceeding to iframe")

        iframe = wait_presence(By.NAME, "app-iframe")
        driver.switch_to.frame(iframe)

        # select all the orders
        logger.info("selecting all orders checkbox")
        all_orders_checkbox_el = wait_clickable(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/table/thead/tr/th[1]/label/span')
        all_orders_checkbox_el.click()

        # click the pay all button
        logger.info('clicking pay all button & waiting for stripe payment page to load')
        pay_all_orders_button_el = wait_clickable(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/div/div/div/div[2]/button')
        pay_all_orders_button_el.click()
        time.sleep(5)

        # switch into Stripe window
        logger.info('switching focus to current window for stripe page')
        current_window = driver.current_window_handle
        driver.switch_to.window(current_window)

        # fill out form on stripe page
        logger.info('filling email in stripe form')
        stripe_email_el = wait_clickable(By.ID, 'email')
        stripe_email_el.send_keys(STRIPE_EMAIL)

        #close the "link pay" popup on the checkout page if it appears
        close_link_popup()

        logger.info('filling name in stripe form')
        stripe_name_el = wait_clickable(By.NAME, 'name')
        stripe_name_el.send_keys(STRIPE_NAME)

        logger.info('entering promo code')
        stripe_promo_code_el = wait_clickable(By.ID, 'promotionCode')
        stripe_promo_code_el.send_keys(STRIPE_PROMO_CODE)

        # apply promo code
        logger.info("clicking apply button for promo code")
        stripe_promo_apply_el = wait_clickable(By.CLASS_NAME, 'PromotionCodeEntry-applyButton')
        stripe_promo_apply_el.click()

        logger.info('filling card number in stripe form')
        stripe_cardnumber_el = wait_clickable(By.ID, 'cardNumber')
        stripe_cardnumber_el.send_keys(STRIPE_CARD_NUMBER)

        logger.info('filling card expiration in stripe form')
        stripe_card_expiry_el = wait_clickable(By.ID, 'cardExpiry')
        stripe_card_expiry_el.send_keys(STRIPE_CARD_EXP)

        logger.info('filling cvc in stripe form')
        stripe_card_cvc_el = wait_clickable(By.ID, 'cardCvc')
        stripe_card_cvc_el.send_keys(STRIPE_CSV)

        logger.info('filling cardholder name in stripe form')
        stripe_cardholder_name_el = wait_clickable(By.ID, 'billingName')
        stripe_cardholder_name_el.send_keys(STRIPE_NAME)

        logger.info('filling address line1 in stripe form')
        stripe_billing_address1_el = wait_clickable(By.ID, 'billingAddressLine1')
        stripe_billing_address1_el.send_keys(STRIPE_ADDR_1)
        time.sleep(2)

        logger.info('filling billing city in stripe form')
        stripe_billing_city_el = wait_clickable(By.ID, 'billingLocality')
        stripe_billing_city_el.send_keys(STRIPE_CITY)

        logger.info('filling zip code in stripe form')
        stripe_billing_zip_el = wait_clickable(By.ID, 'billingPostalCode')
        stripe_billing_zip_el.send_keys(STRIPE_ZIP)

        try:
            logger.info('checking for stripepass box')
            stripe_checkbox_el = wait_clickable(By.ID, 'enableStripePass')
            stripe_checkbox_el.click()
            time.sleep(5)
        except:
            pass

        logger.info('clicking pay button')
        stripe_pay_button = wait_clickable(By.CLASS_NAME, 'SubmitButton')
        stripe_pay_button.click()
        time.sleep(18)

        send_email("Nolonger PayBot Ran Successfully",  f"Nolonger PayBot ran sucessfully.")
            
    except Exception as e:
        logger.warning("paying for stripe failed")
        error_message = traceback.format_exc()
        send_email("Nolonger Bot Failed", error_message)
        
        driver.quit()

if __name__ == '__main__':
    paybot()