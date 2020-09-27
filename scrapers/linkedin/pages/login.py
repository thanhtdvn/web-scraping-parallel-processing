from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    
    def __init__(self, browser):
        self.browser = browser
    
    def connect(self, url):
        connection_attempts = 0
        wait = WebDriverWait(self.browser, 10)
        while connection_attempts < 1:
            try:
                self.browser.get(url)
                username = wait.until(EC.presence_of_element_located((By.ID, 'username')))
                print ('exits username')
                password = wait.until(EC.presence_of_element_located((By.ID, 'password')))
                print ('exits psw')
                submit = wait.until(EC.presence_of_element_located((By.XPATH, '//form[@class="login__form"]//button[@type="submit"]')))
                print ('exits submit button')
                username.send_keys('truongducthanh88@gmail.com')
                password.send_keys('96543515@vn')
                submit.click()

                #wait.until(EC.presence_of_element_located((By.ID), 'profile-nav-item'))
                return True
            except Exception as ex:
                connection_attempts += 1
                print(f'Error connecting to {url}.')
                print(f'Attempt #{connection_attempts}.')
        return False
