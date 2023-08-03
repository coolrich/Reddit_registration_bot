from random import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from signup_for import SignUpFor
from random_username import generate as un_generator


class SignUpForSkiff(SignUpFor):

    def __init__(self):
        self.nickname = ''
        options = Options()
        options.add_experimental_option('detach', True)
        self.__chrome = webdriver.Chrome(options=options)

    def __find_sign_up_button_and_click(self):
        inner = WebDriverWait(self.__chrome, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), \"Sign up\")]")))
        print('sign up found!' if inner else 'sign up NOT found!')
        # SignUpForSkiff.random_waiting()
        SignUpFor.imitation_of_human_delay(1, 3)
        inner.find_element(by=By.XPATH, value='..').click()
        print('Click on sign up button.')

    def __find_email_field_and_fill_it(self):
        email_field = self.__chrome.find_element(by=By.XPATH, value='//input[@placeholder = "New email address"]')
        email_field.click()
        print(f'click on email field.')
        self.create_random_username()
        self._printing(field=email_field, text=self.nickname)

    def create_random_username(self):
        self.nickname = un_generator.generate_username(1)[0]

    def execute(self):
        self.__chrome.get('https://app.skiff.com/')
        self.__find_sign_up_button_and_click()
        self.__find_email_field_and_fill_it()


SignUpForSkiff().execute()
