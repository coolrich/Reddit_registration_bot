import math
import random
from abc import ABC
from time import sleep
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement


class SignUpFor(ABC):
    def _printing(self, field: WebElement, text: str):
        field.click()
        self.imitation_of_human_delay(2, 4)
        for char in text:
            field.send_keys(char)
            self.imitation_of_human_delay()
        self.imitation_of_human_delay(5, 12)

    @staticmethod
    def wait(seconds: float):
        print("Waiting for", f"{math.floor(seconds / 60.0)}m:{round(seconds % 60, 2)}s")
        sleep(seconds)

    @staticmethod
    def imitation_of_human_delay(t1=0.1, t2=0.3):
        delay = t1 + random.random() * (t2 - t1)
        SignUpFor.wait(round(delay, 2))
