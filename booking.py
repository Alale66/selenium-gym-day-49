import os
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Booking:
    def __init__(self):
        return

    def booking_process(self, wait):
        try:
            class_lst = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Schedule_dayGroup__y79__")))
            booked_count = 0
            waitlisted_count = 0
            already_booked_waitlisted_count = 0
            booked_details = ""
            waitlisted_details = ""
            already_booked_waitlisted_details = ""
            title = ""
            formated_date = ""
            for day in class_lst:
                date = day.find_element(By.CLASS_NAME, "Schedule_dayTitle__YBybs").text

                if "Tue" in date or "Thu" in date:
                    lst = day.find_elements(By.CLASS_NAME, "ClassCard_cardHeader__D9pf3")
                    for item in lst:
                        if "6:00" in item.text:
                            button = item.find_element(By.TAG_NAME, "button")
                            title = item.find_element(By.TAG_NAME, "h3").text
                            # title=item.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']")
                            if "(" in date:
                                formated_date = date.split("(")[1].replace(')', '')
                            else:
                                formated_date = date

                            if button.text == "Booked":
                                # print(f"Already Booked: {title} on {formated_date}")
                                already_booked_waitlisted_details += f"{title} on {formated_date}\n"
                                already_booked_waitlisted_count += 1
                            elif button.text == "Waitlisted":
                                # print(f"Already on waitlist: {title} on {formated_date}")
                                already_booked_waitlisted_details += f"{title} on {formated_date}\n"

                                already_booked_waitlisted_count += 1
                            elif button.text == "Join Waitlist":
                                # print(f"Joined waitlist for: {title} on {formated_date}")
                                waitlisted_details += f"{title} on {formated_date}\n"

                                waitlisted_count += 1
                            else:
                                button.click()
                                # print(f"Successfully booked: {title} on {formated_date}")
                                booked_details += f"{title} on {formated_date}\n"

                                booked_count += 1

            print("\n\n--- BOOKING SUMMERY ---")
            print(
                f"Classes booked: {booked_count}\n "
                f"Waitlists joined: {waitlisted_count}\n "
                f"Already booked/waitlisted: {already_booked_waitlisted_count}\n "
                f"Total {formated_date} classes processed: {booked_count + waitlisted_count + already_booked_waitlisted_count}")

            print("\n\n--- DETAILED CLASS LIST ---")
            if booked_details != "":
                print(f"[New Booking] {booked_details}")
            if waitlisted_details != "":
                print(f"[New Waitlist] {waitlisted_count}")
            if already_booked_waitlisted_details != "":
                print(f"[Already Booked/ on Waitlist] {already_booked_waitlisted_details}")
        except NoSuchElementException:
            print("Booking the classes failed")
            raise
