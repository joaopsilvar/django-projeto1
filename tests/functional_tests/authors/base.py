import time
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from utils.wsl_display import set_display_windows_if_execute_wsl

class AuhtorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        #definir display do windows caso estiver executando de um wsl
        set_display_windows_if_execute_wsl()
        
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
    
    def get_by_placeholder(self, web_element,placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )
     
    def get_form(self):
        return self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )