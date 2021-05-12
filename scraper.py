

from selenium import webdriver
from parsel import Selector
from time import sleep


def login(username, 
          password,
          webdriverlocation="%USERPROFILE%\Downloads\chromedriver_win32\chromedriver"):
    driver = webdriver.Chrome(webdriverlocation)
    driver.maximize_window()
    
    driver.get('https://www.linkedin.com')
    
    username_field = driver.find_element_by_name('session_key')
    username_field.send_keys(username)
    
    password_field = driver.find_element_by_name('session_key')
    password_field = driver.find_element_by_name('session_password')
    password_field.send_keys(password)
    
    login_btn = driver.find_element_by_class_name('sign-in-form__submit-button')
    login_btn.click()
    sleep(2)
    