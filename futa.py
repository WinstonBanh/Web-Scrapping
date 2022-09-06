from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import json


url = 'https://futabus.vn/'

driver = webdriver.Chrome()
driver.get(url)


data = [['Departure', 'Arrival', 'Date', 'Bus No', 'Departure Time', 'Arrival Time', 'Bus Fare', '# of seats', 'Pickup Location', 'Dropoff Location']]


def newEntry(departure, destination):
    submit = driver.find_element(By.CLASS_NAME, 'buy-btn')
    time.sleep(0.5)
    submit.click()
    time.sleep(0.5)
    
    options = driver.find_elements(By.CLASS_NAME, 'route-option')
    for index, option in enumerate(options):
        date = '15 Sep 2022'
        bus_no = index + 1
        dep_arr = option.find_element(By.CLASS_NAME, 'header')
        dep, arr = dep_arr.text.strip().split(' ')
        fare_n_seats = option.find_element(By.CLASS_NAME, 'label')
        fare_n_seats = fare_n_seats.text.strip().split(' ')
        fare = fare_n_seats[0]
        seats = int(fare_n_seats[-2])
        pickup_dropoff = option.find_elements(By.CLASS_NAME, 'route-line')
        pickup = pickup_dropoff[0].text.strip().split('\n')[0]
        dropoff = pickup_dropoff[1].text
        data.append([departure, destination, date, bus_no, dep, arr, fare, seats, pickup, dropoff])
    driver.back()

def chooseDate():
    date_input = driver.find_element(By.CLASS_NAME, 'controls')
    date_input.click()
    time.sleep(0.5)

    next_button = driver.find_element(By.CLASS_NAME, 'next')
    next_button.click()

    tds = driver.find_elements(By.TAG_NAME, 'td')
    thirty = list(filter(lambda el: el.text == '15', tds))[0]
    thirty.click()

departures = driver.find_elements(By.CLASS_NAME, 'place-list-item')[:51]

for index, departure in enumerate(departures):
    print(data)
    time.sleep(0.5) 
    
    departure_input = driver.find_element(By.ID, 'select_origin')
    departure_input.click()

    departures = driver.find_elements(By.CLASS_NAME, 'place-list-item')[:51]
    departure = departures[index]
    departure_text = departure.get_attribute('innerText')
    departure.click()


    time.sleep(0.5)

    destinations = driver.find_elements(By.CLASS_NAME, 'place-list-item')[51:]
    for i, destination in enumerate(destinations):
        dest_input = driver.find_element(By.ID, 'select_destination')
        time.sleep(0.5)
        dest_input.click()
        time.sleep(0.5)
        destinations = driver.find_elements(By.CLASS_NAME, 'place-list-item')[51:]
        destination = destinations[i]
        destination_text = destination.get_attribute('innerText')
        destination.click()
        time.sleep(0.5)
        chooseDate()
        newEntry(departure_text, destination_text)


with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)


with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
