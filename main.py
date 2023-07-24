from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium_recaptcha_solver import RecaptchaSolver
from selenium_recaptcha_solver.exceptions import RecaptchaException

test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
reg_url = "https://www.reddit.com/account/register/?experiment_d2x_2020ify_buttons=enabled&use_accountmanager=true&experiment_d2x_google_sso_gis_parity=enabled&experiment_d2x_onboarding=enabled&experiment_d2x_am_modal_design_update=enabled"
login = "craftsman94.test@gmail.com"
password = "some_password"

def go_to_reddit():
    global chrome
    chrome = get_driver()
    chrome.implicitly_wait(0.5)
    chrome.get(reg_url)

# Get Chrome driver
def get_driver():
    global chrome
    chrome_opts = Options()
    chrome_opts.add_argument(f'--user-agent={test_ua}')
    chrome_opts.add_argument("--disable-notifications")
    return webdriver.Chrome(options=chrome_opts)


def typing_email():
    email_field = chrome.find_element(by=By.ID, value="regEmail")
    for char in login:
        email_field.send_keys(char)
        sleep(0.1)
    email_field.send_keys(Keys.ENTER)


def get_regname():
    global reg_username
    reg_username = chrome.find_element(by=By.ID, value="regUsername")


def get_regfield():
    global reg_field
    reg_field = chrome.find_element(by=By.ID, value="regPassword")


def typing_password():
    for char in password:
        reg_field.send_keys(char)
        sleep(0.1)

def press_enter():
    reg_field.send_keys(Keys.ENTER)

def solve_captcha():
    solver = RecaptchaSolver(driver=chrome)
    recaptcha_iframe = chrome.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
    is_repeat = True
    while is_repeat:
        try:
            sleep(3)
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            is_repeat = False
        except RecaptchaException:
            print(RecaptchaException)
            sleep(3)
    sleep(3)

def click_continue():
    global continue_button
    continue_button = chrome.find_element(by=By.CSS_SELECTOR, value="button.SignupButton")
    continue_button.click()




go_to_reddit()
typing_email()
sleep(2)
get_regname()
get_regfield()
typing_password()
sleep(2)
press_enter()
sleep(2)
click_continue()
# input("any key to continue...")
sleep(2)
solve_captcha()
click_continue()
input("Press any key to close the program...")
chrome.quit()
