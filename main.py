import pprint
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
# from selenium_stealth import stealth
from selenium.webdriver.common.proxy import Proxy, ProxyType


class CreateSkiffEmails:
    pass


class SignUpForReddit:
    class ErrorSignUpException(Exception):
        def __int__(self, exception):
            print("ErrorSignUpException:", exception.msg)

    def __exception_handler(self, exception: Exception) -> None:
        try:
            self.__raise_signup_exception(exception)
        except RecaptchaException as recaptcha_exception:
            print(recaptcha_exception)
            self.__is_repeat = True

    def __raise_signup_exception(self, exception: Exception) -> None:
        try:
            raise self.ErrorSignUpException(exception)
        except self.ErrorSignUpException as esue:
            print(esue)

    def __init__(self, email: str = "craftsman94.test@gmail.com",
                 password: str = "some_password",
                 is_detached: bool = True,
                 use_proxy: bool = True, ):
        self.exceptions_tuple = (RecaptchaException,)
        self.__is_repeat = True
        # self.__is_proxy_set = False
        self.__is_detached = is_detached
        self.is_re_test = False
        self.__use_proxy = use_proxy
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

    def __init_chrome_opts(self, is_detached) -> Options:
        chrome_opts = Options()
        chrome_opts.add_argument(f'--user-agent={self.__user_agent_headers}')
        chrome_opts.add_argument("--disable-notifications")
        chrome_opts.add_argument('--disable-blink-features=AutomationControlled')
        chrome_opts.add_experimental_option("detach", is_detached)
        return chrome_opts

    def __display_opts(self):
        pprint.pp(self.__chrome_opts.arguments)

    def __go_to_reddit_registration_page(self) -> None:
        self.__chrome.implicitly_wait(3)
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
        recaptcha_iframe = WebDriverWait(self.__chrome, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
        self.__recaptcha_exception_test()
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
    def wait(seconds):
        sleep(seconds)

    def __check_for_use_proxy_and_restart_wd_with_new_proxy(self):
        if self.__use_proxy and self.__proxy_list is not None:
            self.__restart_webdriver_with_new_proxy()

    def __get_new_proxies(self):
        proxy_list = self.__proxy_list
        if len(proxy_list) != 0:
            proxy = proxy_list.pop()
            self.__used_proxies_list.append(proxy)
            print("Set new proxy:", proxy)
            return '--proxy-server=%s' % proxy
        else:
            print("There is no proxy left! Start from begin.")
            self.__proxy_list.extend(self.__used_proxies_list.copy())
            self.__used_proxies_list.clear()
            print('Proxy has been turned off.')
            return '--no-proxy-server'

    def __restart_webdriver_with_new_proxy(self):
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        self.__quit_browser()
        self.__recreate_chrome_with_new_proxies()

    def __recreate_chrome_with_new_proxies(self):
        proxy_arg = self.__get_new_proxies()
        self.__chrome_opts.add_argument(proxy_arg)
        self.wait(6)
        self.__quit_browser()
        self.__chrome = webdriver.Chrome(options=self.__chrome_opts)
        # self.__is_proxy_set = True

    def __check_for_completed_signup(self):
        WebDriverWait(self.__chrome, 3).until(EC.url_to_be("https://www.reddit.com/"))

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
        dropdown_menu = WebDriverWait(self.__chrome, 5).until(
            EC.visibility_of_element_located((By.ID, 'USER_DROPDOWN_ID')))
        dropdown_menu.click()
        log_button = self.__chrome.find_element(by=By.XPATH, value="//*[contains(text(), \"Log Out\")]")
        while log_button.tag_name != 'button':
            log_button = log_button.find_element(by=By.XPATH, value='..')
        print('button found!')
        log_button.click()

    def test_login_logout(self):
        self.__log_in()
        self.__log_out()

    def execute(self):
        while self.__is_repeat:
            try:
                self.__is_repeat = False
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
            except self.exceptions_tuple as exception:
                self.__exception_handler(exception)
            finally:
                self.__quit_browser()

        return {
            'username': self.__reg_username,
            'email': self.__email,
            'password': self.__password,
            'API_key': None
        }

    def check_for_proxy(self):
        self.__recreate_chrome_with_new_proxies()
        self.__chrome.get('http://www.whatismyip.com')

    class RedditAccountsFactory:
        @staticmethod
        def create_accounts(number_of_acc: int = 1):
            accounts = []
            for i in range(1, number_of_acc + 1):
                data = Data.email_pswd_list.pop()
                email = data['email']
                pswd = data['pswd']
                acc_details = SignUpForReddit(email=email, password=pswd).execute()
                accounts.append(acc_details)
                five_minutes = 60 * 8
                print("Waiting for", five_minutes / 60, "minutes")
                SignUpForReddit.wait(five_minutes)

            pprint.pp(accounts)


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


SignUpForReddit.RedditAccountsFactory.create_accounts(3)
