import math
import pprint
import re
import trace
import traceback
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_recaptcha_solver import RecaptchaSolver
from selenium_recaptcha_solver.exceptions import RecaptchaException
from urllib3.exceptions import MaxRetryError
# from selenium_stealth import stealth
from selenium.webdriver.common.proxy import Proxy, ProxyType


class CreateSkiffEmails:
    pass


class SignUpForReddit:

    def __init__(self, email: str = "craftsman94.test@gmail.com",
                 password: str = "some_password",
                 is_detached: bool = True,
                 use_proxy: bool = False, ):
        # self.exceptions_tuple = (RecaptchaException, TimeoutException, MaxRetryError, ElementClickInterceptedException, NoSuchElementException)
        self.delay_step = 10*60
        self.__delay_after_failed_attempt = 60
        self.exception_tuple = (
            ElementClickInterceptedException, RecaptchaException, WebDriverException)
        self.__timeout = 3
        self.__use_proxy = use_proxy
        self.__is_proxy_set = False
        self.__is_repeat = True
        self.__is_detached = is_detached
        self.is_re_test = False
        self.__reg_url = "https://www.reddit.com/account/register/?experiment_d2x_2020ify_buttons=enabled" \
                         "&use_accountmanager=true&experiment_d2x_google_sso_gis_parity=enabled" \
                         "&experiment_d2x_onboarding=enabled&experiment_d2x_am_modal_design_update=enabled"
        self.__user_agent_headers = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/37.0.2049.0 Safari/537.36'

        self.__proxy_list = ["199.243.245.94:8080"]
        self.__used_proxies_list = []
        self.__email = email
        self.__password = password
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        self.__chrome_opts = self.__init_chrome_opts(is_detached)
        self.__chrome = webdriver.Chrome(options=self.__chrome_opts)
        # self.__chrome.
        self.__chrome.implicitly_wait(8)

    def __init_chrome_opts(self, is_detached) -> Options:
        chrome_opts = Options()
        chrome_opts.add_argument(f'--user-agent={self.__user_agent_headers}')
        chrome_opts.add_argument("--disable-notifications")
        chrome_opts.add_argument('--disable-blink-features=AutomationControlled')
        chrome_opts.add_experimental_option("detach", is_detached)
        return chrome_opts

    def __display_opts(self):
        print('-' * 100)
        print('Options:')
        pprint.pp(self.__chrome_opts.arguments)
        print('-' * 100)

    def __go_to_reddit_registration_page(self) -> None:
        self.__chrome.get(self.__reg_url)

    def __printing_email(self):
        email_field = self.__chrome.find_element(by=By.ID, value="regEmail")
        for char in self.__email:
            email_field.send_keys(char)
            self.wait(0.1)
        email_field.send_keys(Keys.ENTER)

    def __save_value_from_reg_name(self):
        self.__reg_username = self.__chrome.find_element(by=By.ID, value="regUsername").get_attribute("value")

    def __get_reg_field(self):
        self.__reg_field = self.__chrome.find_element(by=By.ID, value="regPassword")

    def __printing_password(self):
        self.__get_reg_field()
        for char in self.__password:
            self.__reg_field.send_keys(char)
            self.wait(0.1)
        self.__submit_regfield()

    def __submit_regfield(self):
        self.__reg_field.send_keys(Keys.ENTER)

    def __solve_captcha(self):
        solver = RecaptchaSolver(driver=self.__chrome)
        recaptcha_iframe = WebDriverWait(self.__chrome, self.__timeout).until(
            EC.visibility_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
        # self.__recaptcha_exception_test()

        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    def __recaptcha_exception_test(self):
        if self.is_re_test:
            self.is_re_test = False
            raise RecaptchaException()

    def __get_cont_butt(self):
        self.__continue_button = self.__chrome.find_element(by=By.CSS_SELECTOR, value="button.SignupButton")

    def __click_continue(self):
        self.__get_cont_butt()
        self.__continue_button.click()

    def __quit_browser(self):
        self.__chrome.quit()

    @staticmethod
    def wait(seconds: float):
        print("Waiting for", f"{math.floor(seconds / 60.0)}m:{round(seconds % 60, 3)}s")
        sleep(seconds)

    def __restart_chrome(self, delay_after_quitting_in_sec: int = 0):
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        self.__quit_browser()
        self.wait(delay_after_quitting_in_sec)
        self.__recreate_chrome()

    def __get_new_proxies(self):
        proxy_list = self.__proxy_list
        if len(proxy_list) != 0:
            proxy = proxy_list.pop()
            self.__used_proxies_list.append(proxy)
            print("Set new proxy:", proxy)
            return f'--proxy-server={proxy}'
        else:
            self.__proxy_list.extend(self.__used_proxies_list.copy())
            self.__used_proxies_list.clear()
            print('Proxy is not used.')
            return None

    def __proxy_switcher(self):
        if self.__use_proxy:
            proxy_arg = self.__get_new_proxies()
            self.__chrome_opts.add_argument(proxy_arg)
            self.__is_proxy_set = True
            self.__timeout = 20
            print('Change timeout to', self.__timeout)
        else:
            self.__is_proxy_set = False
            self.__timeout = 3
            print('Change timeout to', self.__timeout)

    def __recreate_chrome(self):
        self.__chrome_opts = self.__init_chrome_opts(self.__is_detached)
        self.__proxy_switcher()
        self.__chrome = webdriver.Chrome(options=self.__chrome_opts)

    class SignUpException(Exception):
        def __init__(self, message: str = '', delay: tuple = ()):
            print(message)
            time = delay[0]
            units = delay[1]
            if units == 'х':
                time += 1
                time *= 60
            elif units == 'с':
                time += 60
            self.delay_in_seconds = time
            # print('Delay:', self.delay_in_seconds, 'seconds',
            #       self.delay_in_seconds / 60.0, 'minutes', "(+1 minute additional)")

    def __check_for_completed_signup(self):
        self.check_for_waiting_notification()
        self.check_for_signin()

    def check_for_signin(self):
        WebDriverWait(self.__chrome, self.__timeout).until(EC.url_to_be("https://www.reddit.com/"))

    def check_for_waiting_notification(self):
        # Translate the processing of the exception in exception handler
        try:
            notification = WebDriverWait(self.__chrome, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(), \"Looks like you've been doing that a lot.\")]")))
            notification_text = notification.text
            print(notification_text)
            time_and_units = self.search_for_time(notification_text)
            if time_and_units:
                delay = self.parsing_time_and_units(time_and_units)
                raise SignUpForReddit.SignUpException(delay=delay)
        except TimeoutException:
            pass

    @staticmethod
    def parsing_time_and_units(time_and_units):
        groups_tuple = time_and_units.groups()
        number = int(groups_tuple[0])
        units = groups_tuple[1]
        if units[0] == 'с':
            return number, 'с'
        else:
            return number, 'х'

    @staticmethod
    def search_for_time(notification_text):
        result = re.search(f'(\d+)\s(\w+)', notification_text)
        return result

    def test_execute(self):
        self.__go_to_reddit_registration_page()

    def __go_to_reddit(self):
        self.__chrome.get('https://www.reddit.com/')

    def __log_in(self):
        self.__chrome.get('https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F')
        login_field = self.__chrome.find_element(by=By.ID, value="loginUsername")
        login_field.send_keys('mindcrafter94')
        passwd_field = self.__chrome.find_element(by=By.ID, value="loginPassword")
        passwd_field.send_keys("27JuL15:322023")
        passwd_field.send_keys(Keys.ENTER)

    def __log_out(self):
        dropdown_menu = WebDriverWait(self.__chrome, self.__timeout).until(
            EC.visibility_of_element_located((By.ID, 'USER_DROPDOWN_ID')))
        dropdown_menu.click()
        log_button = self.__chrome.find_element(by=By.XPATH, value="//*[contains(text(), \"Log Out\")]")
        while log_button.tag_name != 'button':
            log_button = log_button.find_element(by=By.XPATH, value='..')
        print('Log Out found!')
        log_button.click()

    def test_login_logout(self):
        self.__log_in()
        self.__log_out()

    def __exception_handler(self, delay_in_seconds=0, exception: Exception = None) -> None:
        print(exception.__class__.__name__)
        self.__restart_chrome(delay_in_seconds)

    def actions(self):
        self.__display_opts()
        self.wait(5)
        self.__go_to_reddit_registration_page()
        self.__printing_email()
        self.wait(1)
        self.__save_value_from_reg_name()
        self.__printing_password()
        self.wait(1)
        self.__click_continue()
        self.wait(1)
        self.__solve_captcha()
        self.__click_continue()
        self.__check_for_completed_signup()
        self.__log_out()
        self.wait(3)
        self.__quit_browser()

    def execute(self):
        while self.__is_repeat:
            try:
                self.actions()
                self.__is_repeat = False
                self.__decrease_delay()
            except (RecaptchaException, TimeoutException, ElementClickInterceptedException) as e:
                self.__exception_handler(delay_in_seconds=self.__delay_after_failed_attempt, exception=e)
                self.__increase_delay()
            except SignUpForReddit.SignUpException as sue:
                self.__exception_handler(sue.delay_in_seconds, exception=sue)
        return {
            'username': self.__reg_username,
            'email': self.__email,
            'password': self.__password,
            'API_key': None
        }

    def check_for_proxy(self):
        self.__recreate_chrome()
        self.__chrome.get('http://www.whatismyip.com')

    class RedditAccountsFactory:
        @staticmethod
        def create_accounts(number_of_acc: int = 1, delay_int_minutes: int = 0, use_proxy: bool = False):
            accounts = []
            for i in range(1, number_of_acc + 1):
                data = Data.email_pswd_list.pop()
                email = data['email']
                pswd = data['pswd']
                acc_details = SignUpForReddit(email=email, password=pswd, use_proxy=use_proxy).execute()
                accounts.append(acc_details)
                minutes = 60 * delay_int_minutes
                # print("Waiting for", delay_int_minutes, "minutes")
                SignUpForReddit.wait(60 * minutes)

            pprint.pp(accounts)

    def __close_page(self):
        self.__chrome.close()
        self.__chrome.switch_to.default_content()

    def __restart_webdriver_without_new_proxy(self, delay_after_quitting_in_min):
        pass

    def __increase_delay(self):
        self.__delay_after_failed_attempt += self.delay_step

    def __decrease_delay(self):
        self.__delay_after_failed_attempt -= self.delay_step


class Data:
    """Stores the usernames, emails, passwords, and API keys"""

    email_pswd_list = [{"email": "craftsman94.test@gmail.com", "pswd": "craftsman94.test@gmail."[::-1]},
                       {"email": "mindblow94@skiff.com", "pswd": "mindblow94@skiff."[::-1]},
                       {"email": "mindblow94.0@skiff.com", "pswd": "mindblow94.0@skiff."[::-1]},
                       {"email": "mindblow94.1@skiff.com", "pswd": "mindblow94.1@skiff."[::-1]}]

    def __init__(self):
        self.reddit_accounts = []

    def __create(self):
        pass

        input("Done. Press enter to close the program...")


# SignUpForReddit().test_login_logout()
# SignUpForReddit().check_for_proxy()


SignUpForReddit.RedditAccountsFactory.create_accounts(3, use_proxy=False)
