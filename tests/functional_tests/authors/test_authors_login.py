from .base import AuhtorsBaseTest
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

@pytest.mark.functional_test
class AuthorsLoginTest(AuhtorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):    
        string_password = 'pass'
        user = User.objects.create_user(username='user',password=string_password)
        
        #Usuário abre a página de Login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        #Usuário vê o formulário de Login
        form = self.get_form()
        
        #Usuário informa o username e o password
        self.get_by_placeholder(form, 'Type Your username').send_keys(user.username)
        self.get_by_placeholder(form, 'Type Your password').send_keys(string_password)
        
        #Usuário clica em entrar
        form.submit()
        
        self.assertIn(f'Your are logged in with {user.username}.', self.browser.find_element(By.TAG_NAME, 'body').text)
    
    def test_login_create_raises_404_if_not_POST_method(self):
        #Usuário abre a página de Login
        self.browser.get(self.live_server_url + reverse('authors:login_create'))
        
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME,'body').text
        )
    
    def test_login_is_invalid(self):
        #Usuário abre a página de Login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        #Usuário vê o formulário de Login
        form = self.get_form()
        
        #Usuário informa o username e o password
        self.get_by_placeholder(form, 'Type Your username').send_keys('')
        self.get_by_placeholder(form, 'Type Your password').send_keys('')
        
        #Usuário clica em entrar
        form.submit()
        
        self.assertIn('Invalid username or password', self.browser.find_element(By.TAG_NAME, 'body').text)
    
    def test_form_login_invalid_credentials(self):
        #Usuário abre a página de Login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        #Usuário vê o formulário de Login
        form = self.get_form()
        
        #Usuário informa o username e o password
        self.get_by_placeholder(form, 'Type Your username').send_keys('invalid_user')
        self.get_by_placeholder(form, 'Type Your password').send_keys('invalid_password')
        
        #Usuário clica em entrar
        form.submit()
        
        self.assertIn('Invalid credentials', self.browser.find_element(By.TAG_NAME, 'body').text)
        self.assertIn('Invalid credentials', self.browser.find_element(By.TAG_NAME, 'body').text)

            