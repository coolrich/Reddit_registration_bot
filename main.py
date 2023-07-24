from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium_recaptcha_solver import RecaptchaSolver
from selenium_recaptcha_solver.exceptions import RecaptchaException


class SignUpForReddit:
    def __init__(self):
        self.user_agent_headers = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
        self.reg_url = "https://www.reddit.com/account/register/?experiment_d2x_2020ify_buttons=enabled&use_accountmanager=true&experiment_d2x_google_sso_gis_parity=enabled&experiment_d2x_onboarding=enabled&experiment_d2x_am_modal_design_update=enabled"
        self.login = "craftsman94.test@gmail.com"
        self.password = "some_password"
        self.reg_username = None
        self.reg_field = None
        self.continue_button = None
        chrome_opts = self.__init_chrome_opts()
        self.chrome = webdriver.Chrome(options=chrome_opts)

    def __init_chrome_opts(self) -> Options:
        chrome_opts = Options()
        chrome_opts.add_argument(f'--user-agent={self.user_agent_headers}')
        chrome_opts.add_argument("--disable-notifications")
        return chrome_opts

    def __go_to_reddit(self) -> None:
        # global chrome
        self.chrome.implicitly_wait(0.5)
        self.chrome.get(self.reg_url)

    def __printing_email(self):
        email_field = self.chrome.find_element(by=By.ID, value="regEmail")
        for char in self.login:
            email_field.send_keys(char)
            self.__wait(0.1)
        email_field.send_keys(Keys.ENTER)

    def __save_value_from_reg_name(self):
        self.reg_username = self.chrome.find_element(by=By.ID, value="regUsername")

    def __get_reg_field(self):
        self.reg_field = self.chrome.find_element(by=By.ID, value="regPassword")

    def __printing_password(self):
        for char in self.password:
            self.reg_field.send_keys(char)
            self.__wait(0.1)

    def __submit_regfield(self):
        self.reg_field.send_keys(Keys.ENTER)

    def __solve_captcha(self):
        solver = RecaptchaSolver(driver=self.chrome)
        recaptcha_iframe = self.chrome.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        is_repeat = True
        while is_repeat:
            try:
                self.__wait(3)
                solver.click_recaptcha_v2(iframe=recaptcha_iframe)
                is_repeat = False
            except RecaptchaException:
                print(RecaptchaException)
                self.__wait(3)
        self.__wait(3)

    def __get_cont_butt(self):
        self.continue_button = self.chrome.find_element(by=By.CSS_SELECTOR, value="button.SignupButton")

    def __click_continue(self):
        self.continue_button.click()

    def __quit_browser(self):
        self.chrome.quit()

    @staticmethod
    def __wait(seconds):
        sleep(seconds)

    def execute(self):
        self.__go_to_reddit()
        input("Enter any key to continue...")
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
        # input("any key to continue...")
        self.__wait(2)
        self.__solve_captcha()
        # self.click_continue()
        input("Press any key to close the program...")
        self.__quit_browser()


SignUpForReddit().execute()
