import csv
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup

from .login import LoginPage

class ProfileInfo:
    def __init__(self):
        self.profile_url = ''
        self.email = ''
        self.ims = ''
        self.birthday = ''
        self.em_name = ''
        self.em_current_title = ''
        self.em_about = ''
        self.em_background = ''
        self.em_skills = ''
        self.em_accom = ''

class ProfilePage:
    
    def __init__(self, browser):
        self.browser = browser
        self.data = None
    
    def connect(self, url):
        self.data = None
        connection_attempts = 0
        while connection_attempts < 3:
            try:
                self.browser.get(url)
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.ID, 'profile-content'))
                )
                connection_attempts = 10
            except Exception as ex:
                connection_attempts += 1
                print(f'Error connecting to {url}.')
                print(f'Attempt #{connection_attempts}.')

        wait = WebDriverWait(self.browser, 10)
        
        required_check_login = False
        
        if(required_check_login):
            try:
                join_to_connect_button = wait.until(EC.presence_of_element_located((By.XPATH), '//a[@data-tracking-control-name="public_profile_top-card-primary-button-join-to-connect"]'))
                sleep(2)
                join_to_connect_button.click()
                LoginPage().connect('https://www.linkedin.com/uas/login')
                return False
            except Exception:
                print ("No join_to_connect_button")
                return False
        
        # click see more links and play arround page simulate a user
        
        try:
            see_more_buttons = self.browser.find_elements(By.XPATH, '//a[@class="lt-line-clamp__more"]')
            for button in see_more_buttons:
                sleep(0.5)
                actions = ActionChains(self.browser)
                actions.move_to_element(button)
                actions.click(button)
                actions.perform()
        except Exception as ex:
            print('see_more_buttons error!')
        
        try:
            see_more_experiences_button = self.browser.find_element(By.XPATH, '//div[contains(@class="pv-experience-section__see-more")]/button')
            sleep(1)
            see_more_experiences_button.click()
        except Exception as ex:
            print('see_more_experiences_button error!', ex)

        try:
            load_more_skills_button = self.browser.find_element(By.XPATH, '//button[contains(@class="pv-skills-section__additional-skills")]')
            sleep(1)
            load_more_skills_button.click()
        except Exception as ex:
            print('load_more_skills_button error!', ex)

        try:
            load_more_accom_button = self.browser.find_element(By.XPATH, '//button[contains(@class="pv-accomplishments-block__expand")]')
            sleep(1)
            load_more_accom_button.click()
        except Exception as ex:
            print('load_more_accom_button error!', ex)

        # scroll to bottom to show contact-div -> get name + job title
        self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

        # get html
        html = self.browser.page_source

        # create soup object
        soup = BeautifulSoup(html, 'html.parser')

        profile_info = ProfileInfo()

        profile_info = self.parse_profile_info(soup, profile_info)

        try:
            contact_see_more_element = self.browser.find_element(By.XPATH, '//a[@data-control-name="contact_see_more"]')
            print ('found contact_see_more button')
            required_check_login = False
            contact_see_more_element.click()
            sleep(10)
            wait.until(
                EC.presence_of_element_located((By.ID, 'pv-contact-info'))
            )

            # get html
            html = self.browser.page_source
            # create soup object
            soup = BeautifulSoup(html, 'html.parser')
            profile_info = self.parse_contact_info(soup, profile_info)
            
        except Exception as ex:
            print ("No contact_see_more element found!", ex)

        print('Parse profile page successed!')
        self.data = profile_info
        return True
        
    def write_to_file(self, data_list, filename):
        for row in data_list:
            with open(filename, 'a') as csvfile:
                writer = csv.DictWriter(csvfile)
                writer.writerow(row)

    def parse_contact_info(self, soup, profile_contact_info):
        profile_section = soup.find('div', class_='pv-profile-section pv-contact-info')
        if(profile_section is None):
            print('Can not get profile section')
            #raise Exception('Can not get profile section')
            return profile_contact_info
        
        try:
            profile_url_section = profile_section.find('section', class_='pv-contact-info__contact-type ci-vanity-url')
            profile_contact_info.profile_url = profile_url_section.find('a', class_='pv-contact-info__contact-link').get_text()
        except Exception as ex:
            print('profile_url', ex)
        try:
            profile_phone_section = profile_section.find('section', class_='pv-contact-info__contact-type ci-phone')
            profile_contact_info.phone = [p.get_text() for p in profile_phone_section.find_all('li', class_='pv-contact-info__ci-container')]
        except Exception as ex:
            print('phone', ex)

        try:    
            profile_email_section = profile_section.find('section', class_='pv-contact-info__contact-type ci-email')
            profile_contact_info.email = profile_email_section.find('a', class_='pv-contact-info__contact-link').get_text()
        except Exception as ex:
            print('email', ex)

        try:
            profile_im_section =  profile_section.find('section', class_='pv-contact-info__contact-type ci-ims')
            profile_contact_info.ims = [ i.get_text() for i in profile_im_section.find_all('li', class_='pv-contact-info__ci-container')]
        except Exception as ex:
            print('ims', ex)

        try:
            profile_birthday_section = profile_section.find('section', class_='pv-contact-info__contact-type ci-birthday')
            profile_contact_info.birthday = profile_birthday_section.find('div', class_='pv-contact-info__ci-container').get_text()
        except Exception as ex:
            print('birthday', ex)

        
        return profile_contact_info

    def parse_profile_info(self, soup, profile_info):
        try:
            profile_info.em_name = soup.find('dt', class_='pv-profile-sticky-header__name').get_text()
        except Exception as ex:
            print('em_name', ex)
        
        try:
            profile_info.em_current_title = soup.find('dd', class_='pv-profile-sticky-header__headline').get_text()
        except Exception as ex:
            print('em_current_title', ex)
        
        try:
            profile_info.em_about = soup.find('p', class_='pv-about__summary-text').get_text()
        except Exception as ex:
            print('em_about', ex)

        try:
            profile_info.em_background = soup.find('section', class_='pv-profile-section background-section').get_text()
        except Exception as ex:
            print('em_background', ex)
        
        try:
            profile_info.em_skills = soup.find('section', class_='pv-profile-section pv-skill-categories-section').get_text()
        except Exception as ex:
            print('em_skills', ex)
        
        try:
            profile_info.em_accom = soup.find('section', class_='pv-profile-section pv-accomplishments-section').get_text()
        except Exception as ex:
            print('em_accom', ex)
        
        return profile_info


