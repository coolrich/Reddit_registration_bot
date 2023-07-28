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
    def __init__(self, email: str = "craftsman94.test@gmail.com",
                 password: str = "some_password",
                 is_detached: bool = True,
                 use_proxy: bool = True, ):
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

    def __go_to_reddit_registration_page(self) -> None:
        self.__chrome.implicitly_wait(3)
        try:
            self.__chrome.get(self.__reg_url)
        except WebDriverException as wde:
            print(wde)
            self.__restart_webdriver_with_new_proxy()

    def __printing_email(self):
        try:
            email_field = self.__chrome.find_element(by=By.ID, value="regEmail")
            for char in self.__email:
                email_field.send_keys(char)
                self.__wait(0.1)
            email_field.send_keys(Keys.ENTER)
        except NoSuchElementException as nsee:
            print(nsee)
            # self.__check_for_use_proxy_and_restart()

    def __save_value_from_reg_name(self):
        try:
            self.__reg_username = self.__chrome.find_element(by=By.ID, value="regUsername").get_attribute("value")
        except NoSuchElementException as nsee:
            print(nsee)

    def __get_reg_field(self):
        self.__reg_field = self.__chrome.find_element(by=By.ID, value="regPassword")

    def __printing_password(self):
        try:
            self.__get_reg_field()
            for char in self.__password:
                self.__reg_field.send_keys(char)
                self.__wait(0.1)
            self.__submit_regfield()
        except NoSuchElementException as nsee:
            print(nsee)

    def __submit_regfield(self):
        self.__reg_field.send_keys(Keys.ENTER)

    def __solve_captcha(self):
        try:
            solver = RecaptchaSolver(driver=self.__chrome)
            recaptcha_iframe = WebDriverWait(self.__chrome, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
            self.__recaptcha_exception_test()
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        except RecaptchaException as rec_exc:
            print(rec_exc)
        except StaleElementReferenceException as sere:
            print(sere)
        except TimeoutException as te:
            print(te)

    def __recaptcha_exception_test(self):
        if self.is_re_test:
            self.is_re_test = False
            raise RecaptchaException()

    def __get_cont_butt(self):
        self.__continue_button = self.__chrome.find_element(by=By.CSS_SELECTOR, value="button.SignupButton")

    def __click_continue(self):
        try:
            self.__get_cont_butt()
            self.__continue_button.click()
        except NoSuchElementException as nsee:
            print(nsee)
        except StaleElementReferenceException as sere:
            print(sere)
        except ElementClickInterceptedException as ecie:
            print(ecie)

    def __quit_browser(self):
        self.__chrome.quit()

    @staticmethod
    def __wait(seconds):
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
            return self.__get_new_proxies()

    def __restart_webdriver_with_new_proxy(self):
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        self.__quit_browser()
        self.__recreate_chrome_with_new_proxies()
        self.execute()

    def __recreate_chrome_with_new_proxies(self):
        new_proxy_str = self.__get_new_proxies()
        self.__chrome_opts.add_argument(new_proxy_str)
        self.__quit_browser()
        self.__chrome = webdriver.Chrome(options=self.__chrome_opts)

    def __check_for_completed_signup(self):
        try:
            WebDriverWait(self.__chrome, 3).until(EC.url_to_be("https://www.reddit.com/"))
        except TimeoutException as toe:
            print(toe)
            self.__check_for_use_proxy_and_restart_wd_with_new_proxy()

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
        # log_button = WebDriverWait(self.__chrome, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[matches(text(), \"Log "                                                                                   "Out\", \"i\")]")))
        log_button = self.__chrome.find_element(by=By.XPATH, value="//*[contains(text(), \"Log Out\")]")
        while log_button.tag_name != 'button':
            log_button = log_button.find_element(by=By.XPATH, value='..')
        print('button found!')
        log_button.click()

    def test_login_logout(self):
        self.__log_in()
        self.__log_out()

    def execute(self):
        # input("Enter any key to continue...")
        self.__go_to_reddit_registration_page()
        self.__printing_email()
        self.__wait(1)
        self.__save_value_from_reg_name()
        self.__printing_password()
        self.__wait(1)
        self.__click_continue()
        self.__wait(1)
        self.__solve_captcha()
        self.__click_continue()
        self.__check_for_completed_signup()
        self.__log_out()
        self.__wait(3)
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
            """
            
            
            
            Make a pause...
            
            
            
            """
        pprint.pp(accounts)
        input("Done. Press enter to close the program...")


# SignUpForReddit().test_login_logout()
# RedditAccountsFactory.create_accounts(3)
SignUpForReddit().check_for_proxy()
