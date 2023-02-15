from selenium import webdriver
import time
from dotenv import load_dotenv
import os
from modules.utils import readEventCollection, formatDateTime
load_dotenv()

def fillEventsOnIntranet(eventfile = "events.csv") :
    cohortPosition = [-1, 9, 8, 7, 6, 5, 4, 3, 2, 14, 13, 12, 11 , 1 , 10, 0]
    # initialize browser driver
    DRIVER_PATH = os.getenv('DRIVER_PATH')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(os.getenv('HBTN_HOST'))

    # Fill out login page.
    email = driver.find_element('xpath', '//*[@id="user_email"]')
    password = driver.find_element('xpath', '//*[@id="user_password"]')
    email.send_keys(os.getenv('HBTN_USERNAME'))
    password.send_keys(os.getenv('HBTN_PASSWORD'))

    login = driver.find_element('xpath', '//*[@id="new_user"]/div[4]/input')
    login.click()

    time.sleep(2)

    # read csv content to fill out forms
    csvcontents = readEventCollection(eventfile)
    for row in csvcontents:
        # Find events
        driver.find_element('xpath', '/html/body/div[1]/ul/li[6]/a').click()
        driver.find_element('xpath', '/html/body/main/article/a').click()

        # Set type of event 
        driver.find_element('xpath', '//*[@id="event_event_type"]').send_keys("default")
        title = driver.find_element('xpath', '//*[@id="event_title"]')
        title.send_keys(row['Title'])
        time.sleep(1)
        # Event starts at
        startDate, startTime = formatDateTime(row['startAt'])

        driver.find_element('xpath', '//*[@id="new_event"]/div[4]/div/div/div[1]/div/div[1]/input').send_keys(startDate)
        driver.find_element('xpath', '//*[@id="new_event"]/div[4]/div/div/div[1]/div/div[2]/div/div/input').send_keys(startTime)
        time.sleep(1)

        # Event ends at
        endDate, endTime = formatDateTime(row['endAt'])
        driver.find_element('xpath', '//*[@id="new_event"]/div[4]/div/div/div[2]/div/div[1]/input').send_keys(endDate)
        driver.find_element('xpath', '//*[@id="new_event"]/div[4]/div/div/div[2]/div/div[2]/div/div/input').send_keys(endTime)
        time.sleep(1)

        driver.find_element('xpath', '//*[@id="event_location"]').send_keys(row['location'])

        position = cohortPosition.index(int(row['cohortNumber'])) + 1
        driver.find_element('xpath', '//*[@id="new_event"]/div[7]/div/div/div[2]/div/span['+ str(position) +']').click()

        # Show textarea for accessibility 
        js = "document.getElementById('event_description').style.display = 'block'"
        driver.execute_script(js)

        driver.find_element('xpath', '//*[@id="event_description"]').send_keys(row['description'])
        # time.sleep(2)
        # Next  button 
        driver.find_element('xpath', '//*[@id="new_event"]/div[11]/input').click()
        time.sleep(2)

