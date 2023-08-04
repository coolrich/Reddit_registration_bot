from random_username import generate as un_generator
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from signup_for import SignUpFor


class SignUpForSkiff(SignUpFor):

    def __init__(self):
        self.nickname = ''
        self.email_domain = '@skiff.com'
        self.email = None
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
        while True:
            self.create_random_username()
            self._printing(field=email_field, text=self.nickname)
            is_unique = self.__is_nickname_unique()
            if is_unique:
                break
            self.__removing_chars_in_field(field=email_field)

    def create_random_username(self):
        self.nickname = un_generator.generate_username(1)[0]

    def execute(self):
        self.__chrome.get('https://app.skiff.com/')
        self.__find_sign_up_button_and_click()
        self.__find_email_field_and_fill_it()
        self.__save_email()
        # self.__find_next_and_click()

    def __is_nickname_unique(self):
        try:
            (WebDriverWait(self.__chrome, 2).
             until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Username has already been '
                                                               'taken.")]'))))
            return False
        except TimeoutException:
            return True

    @staticmethod
    def __removing_chars_in_field(field):
        length = len(field.get_attribute(name='value'))
        for _ in range(length):
            field.send_keys(Keys.BACKSPACE)
            SignUpForSkiff.imitation_of_human_delay(0.01, 0.1)

    def __save_email(self):
        self.__email = self.nickname + self.email_domain

    # def __find_next_and_click(self):
    #     self.__chrome.find_element(by=By.XPATH, value='//*[contains(text(), "Username has already been '
    #                                                   'taken.")]').click()


SignUpForSkiff().execute()
