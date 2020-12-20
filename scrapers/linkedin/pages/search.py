from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging

class SearchPage:
    
    def __init__(self, browser):
        self.browser = browser
        self.stop = False
        logging.basicConfig(filename='search.log',level=logging.DEBUG)
    
    def _get_note(self, profile_name):
        return f"Xin chào {profile_name}! Chúc vui vẻ."

    def _play_with_profile(self, profile_element):

        wait = WebDriverWait(self.browser, 10)
        try:
            profile_name = profile_element.find_element(By.XPATH, './/span[@class="name actor-name"]').text
            connect_button = profile_element.find_element(By.XPATH, './/button[@data-control-name="srp_profile_actions" and starts-with(@aria-label,"Connect")]')
            self._click_button(connect_button)

            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class,"artdeco-modal__actionbar")]')))
            add_note_button = self.browser.find_element(By.XPATH, '//div[contains(@class,"artdeco-modal__actionbar")]//button[@aria-label="Add a note"]')
            self._click_button(add_note_button)
            wait.until(EC.visibility_of_element_located((By.ID, 'custom-message')))
            message_box = self.browser.find_element_by_id('custom-message')
            message_box.send_keys(self._get_note(profile_name))
            send_button = self.browser.find_element(By.XPATH, '//div[contains(@class,"artdeco-modal__actionbar")]//button[@aria-label="Send invitation"]')
            wait.until(EC.visibility_of(send_button))
            self._click_button(send_button)
            wait.until_not(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class,"artdeco-modal__actionbar")]')))
        except Exception as ex:
            print(f'Error {ex}.')
    
    def _parse_current_webpage(self):
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        self.browser.execute_script("window.scrollTo(0,0);")
        footer = self.browser.find_element_by_id('globalfooter-copyright')
        self._move_to(footer)
        profiles = self.browser.find_elements(By.XPATH, '//li[contains(@class,"search-result search-result__occluded-item")]')
        for profile in profiles:
            self._move_to(profile)
            sleep(3)
            # self._play_with_profile(profile)

    def _click_button(self, button):
        actions = ActionChains(self.browser)
        actions.move_to_element(button)
        actions.click(button)
        actions.perform()

    def _move_to(self, element):
        actions = ActionChains(self.browser)
        actions.move_to_element(element)
        actions.perform()
    
    def _go_to_next_page(self):
        # wait = WebDriverWait(self.browser, 20)
        # current_page_element = self.browser.find_element((By.XPATH, '//div[contains(@class, "artdeco-pagination")]//li[contains(@class,"selected")]'))
        try:
            next_page_button = self.browser.find_element(By.XPATH, '//div[contains(@class, "artdeco-pagination")]//button[@aria-label="Next"]')
            self._click_button(next_page_button)
            sleep(10)
        except Exception as ex: 
            print(f'Error {ex}.')
            logging.exception("GO TO NEXT PAGE ERROR", exc_info= True)
            self.stop = True
        # wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="search-results__list list-style-none"]//li')))

    def connect(self, url):
        connection_attempts = 0
        wait = WebDriverWait(self.browser, 10)
        while connection_attempts < 1:
            try:
                self.browser.get(url)
                wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="search-results__list list-style-none "]//li')))
                
                while not self.stop:
                    try:
                        self._parse_current_webpage()
                        sleep(3)
                        self._go_to_next_page()
                    except Exception as ex:
                        print(f'ERROR {ex}!')
                return True
            except Exception as ex:
                connection_attempts += 1
                print(f'Error connecting to {url}.')
                print(f'Attempt #{connection_attempts}.')
        return False
 