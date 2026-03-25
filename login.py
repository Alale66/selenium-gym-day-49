import os
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")


class Login:
    def __init__(self):
        return

    def log_in(self, wait):
        try:
            login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
            login_btn.click()

            email = wait.until(EC.presence_of_element_located((By.ID, "email-input")))
            email.clear()
            email.send_keys(ACCOUNT_EMAIL)

            password = wait.until(EC.presence_of_element_located((By.ID, "password-input")))
            password.clear()
            password.send_keys(ACCOUNT_PASSWORD)

            submit = wait.until(EC.presence_of_element_located((By.ID, "submit-button")))
            submit.click()
        except NoSuchElementException:
            print("Login failed")
            raise
