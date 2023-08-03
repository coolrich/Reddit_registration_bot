from random import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class SignUpForSkiff:

    def __init__(self):
        options = Options()
        options.add_experimental_option('detach', True)
        self.__chrome = webdriver.Chrome(options=options)

    def execute(self):
        self.__chrome.get('https://app.skiff.com/')
        signup_button = self.__find_sign_up_button()
        signup_button.click()

    def __find_sign_up_button(self):
        inner = WebDriverWait(self.__chrome, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), \"Sign up\")]")))
        print(inner.text)
        self.random_waiting()
        return inner.find_element(by=By.XPATH, value='..')


    @staticmethod
    def random_waiting(t1=0.5, t2=1.5):
        waiting_time = t1 + random()*(t2 - t1)
        sleep(3)


SignUpForSkiff().execute()
