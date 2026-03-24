import os
import re

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

URL = "https://appbrewery.github.io/gym/"
ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

Chrome_options = webdriver.ChromeOptions()
Chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
Chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=Chrome_options)
driver.get(URL)
wait = WebDriverWait(driver, 2)
try:
    # login = driver.find_element(By.ID, value="login-button")
    login = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login.click()

    # email = driver.find_element(By.ID, value="email-input")
    email = wait.until(EC.presence_of_element_located((By.ID, "email-input")))
    email.clear()
    email.send_keys(ACCOUNT_EMAIL)

    # password = driver.find_element(By.ID, value="password-input")
    password = wait.until(EC.presence_of_element_located((By.ID, "password-input")))
    password.clear()
    password.send_keys(ACCOUNT_PASSWORD)

    # submit = driver.find_element(By.ID, value="submit-button").click()
    submit = wait.until(EC.presence_of_element_located((By.ID, "submit-button")))
    submit.click()

    class_lst = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Schedule_dayGroup__y79__")))
    booked_count = 0
    waitlisted_count = 0
    already_booked_waitlisted_count = 0
    title = ""
    formated_date = ""
    for day in class_lst:
        date = day.find_element(By.CLASS_NAME, "Schedule_dayTitle__YBybs").text

        if "Tue" in date:
            lst = day.find_elements(By.CLASS_NAME, "ClassCard_cardHeader__D9pf3")
            for item in lst:
                if "6:00" in item.text:
                    button = item.find_element(By.TAG_NAME, "button")
                    title = item.find_element(By.TAG_NAME, "h3").text
                    # title=item.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']")
                    formated_date = date.split("(")[1].replace(')', '')
                    if button.text == "Booked":
                        print(f"Already Booked: {title} on {formated_date}")
                        already_booked_waitlisted_count += 1
                    elif button.text == "Waitlisted":
                        print(f"Already on waitlist: {title} on {formated_date}")
                        already_booked_waitlisted_count += 1
                    elif button.text == "Join Waitlist":
                        print(f"Joined waitlist for: {title} on {formated_date}")
                        waitlisted_count += 1
                    else:
                        button.click()
                        print(f"Booked: {title} on {formated_date}")
                        booked_count += 1

    print(
        f"--- BOOKING SUMMERY --- \n "
        f"Classes booked: {booked_count}\n "
        f"Waitlists joined: {waitlisted_count}\n "
        f"Already booked/waitlisted: {already_booked_waitlisted_count}\n "
        f"Total {formated_date} classes processed: {booked_count + waitlisted_count + already_booked_waitlisted_count}")

except NoSuchElementException:
    print("Login failed")
    driver.quit()
