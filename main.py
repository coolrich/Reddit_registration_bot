import pprint
import sys
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_recaptcha_solver import RecaptchaSolver
from selenium_recaptcha_solver.exceptions import RecaptchaException


# from selenium.webdriver.common.proxy import Proxy, ProxyType


class SignUpForReddit:
    def __init__(self, use_proxy: bool):
        self.is_re_test = False

        self.__proxy_list = ["39.59.1.14:8080", "118.31.112.32:80"]
        self.__use_proxy = use_proxy
        self.__user_agent_headers = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/37.0.2049.0 Safari/537.36'
        self.__reg_url = "https://www.reddit.com/account/register/?experiment_d2x_2020ify_buttons=enabled" \
                         "&use_accountmanager=true&experiment_d2x_google_sso_gis_parity=enabled" \
                         "&experiment_d2x_onboarding=enabled&experiment_d2x_am_modal_design_update=enabled"
        self.__email = "craftsman94.test@gmail.com"
        self.__password = "some_password"
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        chrome_opts = self.__init_chrome_opts()
        # capabilities = self.__get_capabilities_with_proxy()
        self.__chrome = webdriver.Chrome(options=chrome_opts)
        # self.__check_for_use_proxy()

    def __init_chrome_opts(self) -> Options:
        chrome_opts = Options()
        chrome_opts.add_argument(f'--user-agent={self.__user_agent_headers}')
        chrome_opts.add_argument("--disable-notifications")
        chrome_opts.add_experimental_option("detach", True)
        return chrome_opts

    def __go_to_reddit(self) -> None:
        self.__chrome.implicitly_wait(12)
        self.__chrome.get(self.__reg_url)

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
        self.__reg_username = self.__chrome.find_element(by=By.ID, value="regUsername")

    def __get_reg_field(self):
        self.__reg_field = self.__chrome.find_element(by=By.ID, value="regPassword")

    def __printing_password(self):
        for char in self.__password:
            self.__reg_field.send_keys(char)
            self.__wait(0.1)

    def __submit_regfield(self):
        self.__reg_field.send_keys(Keys.ENTER)

    def __solve_captcha(self):
        try:
            solver = RecaptchaSolver(driver=self.__chrome)
            recaptcha_iframe = WebDriverWait(self.__chrome, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
            self.recaptcha_exception_test()
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        except RecaptchaException as rec_exc:
            print(rec_exc)
        except StaleElementReferenceException as sere:
            print(sere)

    def recaptcha_exception_test(self):
        if self.is_re_test:
            self.is_re_test = False
            raise RecaptchaException()

    def __get_cont_butt(self):
        self.__continue_button = self.__chrome.find_element(by=By.CSS_SELECTOR, value="button.SignupButton")

    def __click_continue(self):
        self.__continue_button.click()

    def __quit_browser(self):
        self.__chrome.quit()

    @staticmethod
    def __wait(seconds):
        sleep(seconds)

    def __check_for_use_proxy(self):
        if self.__use_proxy and self.__proxy_list:
            self.__set_new_proxy()

    def __check_for_use_proxy_and_restart(self):
        if self.__use_proxy and self.__proxy_list is not None:
            self.__set_new_proxy()
            self.__restart_webdriver()

    def __set_new_proxy(self):
        # new_proxy_opt = Options().add_argument(f"--proxy-server={self.proxy_list.pop()}")
        if len(self.__proxy_list) != 0:
            proxy = f"{self.__proxy_list.pop()}"
            self.__chrome.capabilities['proxy'] = {
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy,
                "proxyType": "MANUAL",
            }
            print("Proxy changed to ", self.__chrome.capabilities['proxy'])
        else:
            print("There is no proxy left!")

    def __restart_webdriver(self):
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        self.__chrome.refresh()
        self.execute()

    def __check_for_completed_signup(self):
        try:
            WebDriverWait(self.__chrome, 3).until(EC.url_to_be("https://www.reddit.com/"))
        except TimeoutException as toe:
            print(toe)
            self.__check_for_use_proxy_and_restart()

    def __execute(self):
        # input("Enter any key to continue...")
        self.__go_to_reddit()
        self.__printing_email()
        self.__wait(2)
        self.__save_value_from_reg_name()
        self.__get_reg_field()
        self.__printing_password()
        self.__wait(2)
        self.__submit_regfield()
        self.__wait(2)
        self.__get_cont_butt()
        self.__click_continue()
        self.__wait(2)
        self.__solve_captcha()
        self.__click_continue()
        self.__check_for_completed_signup()
        # sys.exit()
        # self.__quit_browser()
        return {
            'username': self.__reg_username,
            'email': self.__email,
            'password': self.__password,
            'API_key': None
        }

    @staticmethod
    def create_accounts(number_of_acc: int):
        for i in range(1, number_of_acc + 1):
            acc_details = SignUpForReddit(True).__execute()
            pprint.pp(acc_details)
    input("Done. Press enter to close the program...")

