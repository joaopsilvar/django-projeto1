import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from utils.wsl_display import set_display_windows_if_execute_wsl
from recipes.tests.test_recipe_base import RecipeMixing

class RecipeBaseFunctionalTest(StaticLiveServerTestCase,RecipeMixing):
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