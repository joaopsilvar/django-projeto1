import pytest
from .base import AuhtorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized

@pytest.mark.functional_test
class AuthorsRegisterTest(AuhtorsBaseTest):   
    def fill_form_dummy_data(self,form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    @parameterized.expand([
            ('Your username','This field must not be empty'),
            ('Ex.: John','Write your first name'),
            ('Ex.: Doe','Write your last name'),
            ('Your e-mail','The e-mail must be valid.'),
            ('Type your password','Password must not be empty'),
            ('Repeat your password','Please, repeat your password')
    ])
    def test_empty_fields_error_message(self,placeholder,error_messsage):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        
        field = self.get_by_placeholder(form, placeholder)
        field.send_keys('')
        
        if placeholder != 'Your e-mail':
            form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        
        field.send_keys(Keys.ENTER)
        form = self.get_form()
        self.assertIn(error_messsage, form.text)
    
    def test_user_valid_data_register_sucessfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        
        self.get_by_placeholder(form, 'Your username').send_keys('username')
        self.get_by_placeholder(form, 'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('email@email.com')
        self.get_by_placeholder(form, 'Type your password').send_keys('P@ssord1')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('P@ssord1')
        
        form.submit()
        
        self.assertIn('Your user is created, please log in.', self.browser.find_element(By.TAG_NAME, 'body').text)
        
        
        
        
       
    
    