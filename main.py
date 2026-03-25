import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from login import Login
from booking import Booking

URL = "https://appbrewery.github.io/gym/"

Chrome_options = webdriver.ChromeOptions()
Chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
Chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=Chrome_options)
driver.get(URL)
wait = WebDriverWait(driver, 3)

try:
    Login().log_in(wait)
    Booking().booking_process(wait)
except Exception as e:
    print(e)
