from random_username import generate as un_generator
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from signup_for import SignUpFor
from password_generator import generate_pswd

class SignUpForSkiff(SignUpFor):

    def __init__(self):
        self.__nickname = None
        self.__email_domain = '@skiff.com'
        self.__email = None
        self.__password = None
        options = Options()
        options.add_experimental_option('detach', True)
        self.__chrome = webdriver.Chrome(options=options)

    def __find_sign_up_button_and_click(self):
        inner = WebDriverWait(self.__chrome, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), \"Sign up\")]")))
        print('Sign up found!' if inner else 'Sign up NOT found!')
        # SignUpForSkiff.random_waiting()
        SignUpFor.imitation_of_human_delay(1, 3)
        inner.find_element(by=By.XPATH, value='..').click()
        print('Click on sign up button')

    def __find_email_field_and_fill_it(self):
        email_field = self.__chrome.find_element(by=By.XPATH, value='//input[@placeholder = "New email address"]')
        email_field.click()
        print(f'Click on email field')
        while True:
            self.__create_random_username()
            self._printing(field=email_field, text=self.__nickname)
            is_unique = self.__is_nickname_unique()
            if is_unique:
                break
            self.__removing_chars_in_field(field=email_field)

    def __find_password_fields_and_fill_them(self):
        # Password field
        password_field = (WebDriverWait(self.__chrome, 5)
                          .until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder = "Password"]'))))
        password_field.click()
        print(f'Click on password field')
        self.__password = self.__create_random_password()
        self._printing(field=password_field, text=self.__password)

        # Confirm password field
        confirm_password_field = self.__chrome.find_element(by=By.XPATH, value='//input[@placeholder = "Confirm '
                                                                               'password"]')
        confirm_password_field.click()
        print(f'Click on confirm password field')
        self._printing(field=confirm_password_field, text=self.__password)

    def __create_random_username(self):
        self.__nickname = un_generator.generate_username(1)[0]

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
        self.__email = self.__nickname + self.__email_domain

    def __find_next_and_click(self):
        button = self.__chrome.find_element(by=By.XPATH, value='//span[contains(text(), "Next")]')
        for _ in range(3):
            button = button.find_element(by=By.XPATH, value='..')
        button.click()
        print('Click on the next button')

    @staticmethod
    def __create_random_password():
        return generate_pswd()


    def execute(self):
        self.__chrome.get('https://app.skiff.com/')
        self.__find_sign_up_button_and_click()
        self.__find_email_field_and_fill_it()
        self.__save_email()
        self.__find_next_and_click()
        self.__find_password_fields_and_fill_them()
        print('Email:', self.__email, '\nPassword:', self.__password)


# SignUpForSkiff().execute()
