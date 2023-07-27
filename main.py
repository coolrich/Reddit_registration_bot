import pprint
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_recaptcha_solver import RecaptchaSolver
from selenium_recaptcha_solver.exceptions import RecaptchaException
from selenium_stealth import stealth


# from selenium.webdriver.common.proxy import Proxy, ProxyType

class Data:
    """Stores the usernames, emails, passwords, and API keys"""

    def __init__(self):
        self.email_accounts = []
        self.reddit_accounts = []

    def __create(self):
        pass


class CreateSkiffEmails:
    pass


class SignUpForReddit:
    def __init__(self, email: str = "craftsman94.test@gmail.com",
                 password: str = "some_password",
                 is_detached: bool = True,
                 use_proxy: bool = True, ):
        self.is_re_test = False
        self.__use_proxy = use_proxy
        self.__reg_url = "https://www.reddit.com/account/register/?experiment_d2x_2020ify_buttons=enabled" \
                         "&use_accountmanager=true&experiment_d2x_google_sso_gis_parity=enabled" \
                         "&experiment_d2x_onboarding=enabled&experiment_d2x_am_modal_design_update=enabled"
        self.__user_agent_headers = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/37.0.2049.0 Safari/537.36'

        self.__proxy_list = ["39.59.1.14:8080", "118.31.112.32:80", "51.124.209.11:80", "109.254.62.194:9090"]
        self.__used_proxies_list = []
        self.__email = email
        self.__password = password
        self.__reg_username = None
        self.__reg_field = None
        self.__continue_button = None
        chrome_opts = self.__init_chrome_opts(is_detached)
        self.__chrome = webdriver.Chrome(options=chrome_opts, service=ChromeService(
            ChromeDriverManager().install()))
        stealth(self.__chrome,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def __init_chrome_opts(self, is_detached: bool = False) -> Options:
        chrome_opts = Options()
        chrome_opts.add_argument(f'--user-agent={self.__user_agent_headers}')
        chrome_opts.add_argument("--disable-notifications")
        chrome_opts.add_experimental_option("detach", is_detached)
        # chrome_opts.add_argument("--headless")
        chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_opts.add_experimental_option('useAutomationExtension', False)
        return chrome_opts

    def __go_to_reddit_registration_page(self) -> None:
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
        self.__reg_username = self.__chrome.find_element(by=By.ID, value="regUsername").get_attribute("value")

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
            self.__recaptcha_exception_test()
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        except RecaptchaException as rec_exc:
            print(rec_exc)
        except StaleElementReferenceException as sere:
            print(sere)

    def __recaptcha_exception_test(self):
        if self.is_re_test:
            self.is_re_test = False
            raise RecaptchaException()

    def __get_cont_butt(self):
        self.__continue_button = self.__chrome.find_element(by=By.CSS_SELECTOR, value="button.SignupButton")

    def __click_continue(self):
        try:
            self.__continue_button.click()
        except StaleElementReferenceException as sere:
            print(sere)
        except ElementClickInterceptedException as ecie:
            print(ecie)

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
            proxy = self.__proxy_list.pop()
            self.__used_proxies_list.append(proxy)
            self.__chrome.capabilities['proxy'] = {
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy,
                "proxyType": "MANUAL",
            }
            print("Proxy changed to ", self.__chrome.capabilities['proxy'])
        else:
            print("There is no proxy left! Start from begin.")
            self.__proxy_list.extend(self.__used_proxies_list)

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

    def execute(self):
        # input("Enter any key to continue...")
        self.__go_to_reddit_registration_page()
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
        self.__log_out()
        # sys.exit()
        # self.__quit_browser()
        return {
            'username': self.__reg_username,
            'email': self.__email,
            'password': self.__password,
            'API_key': None
        }

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
        dropdown_menu = WebDriverWait(self.__chrome, 5).until(EC.visibility_of_element_located((By.ID, 'USER_DROPDOWN_ID')))
        dropdown_menu.click()
        # log_button = WebDriverWait(self.__chrome, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[matches(text(), \"Log "
        #                                                                                   "Out\", \"i\")]")))
        log_button = self.__chrome.find_element(by=By.XPATH, value="//*[contains(text(), \"Log Out\")]")
        while log_button.tag_name != 'button':
            log_button = log_button.find_element(by=By.XPATH, value='..')
        print('button found!')
        log_button.click()

    def test_login_logout(self):
        self.__log_in()
        self.__log_out()


class RedditAccountsFactory:
    @staticmethod
    def create_accounts(number_of_acc: int = 1):
        for i in range(1, number_of_acc + 1):
            acc_details = SignUpForReddit().execute()
            pprint.pp(acc_details)
        input("Done. Press enter to close the program...")


RedditAccountsFactory.create_accounts(1)
# SignUpForReddit().test_login_logout()
