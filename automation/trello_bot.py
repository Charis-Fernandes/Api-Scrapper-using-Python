from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import date
import json
import os

driver = webdriver.Chrome()
driver.maximize_window()

def login():
    with open('config.json') as configFile:
        credentials=json.load(configFile)
        print(credentials)
        time.sleep(1)
        driver.find_element(By.XPATH, value="//a[@href='https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback%3Fdisplay%3DeyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%253D%253D&display=eyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%3D%3D']").click()
        time.sleep(2)
        username = driver.find_element(
            By.CSS_SELECTOR, value="input[name='username']")
        username.clear()
        username.send_keys(credentials["USERNAME"])        
        submit=driver.find_element(By.CSS_SELECTOR, value="button[type='submit']").click()
        time.sleep(1)
        password = driver.find_element(
            By.CSS_SELECTOR, value="input[name='password']")
        password.clear()
        password.send_keys(credentials["PASSWORD"])
        submit=driver.find_element(By.CSS_SELECTOR, value="button[type='submit']").click()
        time.sleep(3)
        
def navigation():
    time.sleep(3)
    driver.find_element(
        By.XPATH, value="//div[@title='{}']/ancestor::a".format('My Trello board')).click()
    time.sleep(3)
    
def addtask():
        driver.find_element(By.CSS_SELECTOR, value="button[class='O9vivwyDxMqo3q bxgKMAm3lq5BpA iUcMblFAuq9LKn PnEv2xIWy3eSui SEj5vUdI3VvxDc']").click()
        # Locate the textarea and enter a title for the card
        textarea = driver.find_element(By.CSS_SELECTOR, value="textarea[data-testid='list-card-composer-textarea']")
        textarea.clear()
        textarea.send_keys("Bot made this!")
        time.sleep(1)
        add=driver.find_element(By.CSS_SELECTOR, value="button[type='submit']").click()
        time.sleep(3)

def screenshotPage():
    time.sleep(2)
    date_str = date.today().strftime("%d-%m-%Y")
    fpath = os.path.join(os.getcwd(), 'screenshots/{}.png'.format(date_str))
    driver.get_screenshot_as_file(fpath)


def main():
    try:
        driver.get("https://trello.com")
        login()
        navigation()
        addtask()
        screenshotPage()
        input("Bot Operation Completed. Press any key...")
        driver.close()
    except Exception as e:
        print(e)
        driver.close()
        
if __name__ == "__main__":
    main()