import csv
import datetime
from time import sleep, time

from selenium import webdriver

from .pages.login import LoginPage
from .pages.profile import ProfilePage
from .pages.search import SearchPage

def get_driver():
    # initialize options
    options = webdriver.ChromeOptions()
    # pass in headless argument to options
    # options.add_argument('--headless')

    # initialize driver
    chrome_driver = "C:\\_workspace\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
    return driver

class Page:
    def __init__(self):
        self.browser = get_driver()

    def login(self):
        return LoginPage(self.browser)

    def profile(self):
        return ProfilePage(self.browser)

    def search(self):
        return SearchPage(self.browser)
    
