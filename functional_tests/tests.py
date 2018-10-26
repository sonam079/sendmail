from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from basic.models import SubscribedEmail
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from basic.views import home
import time
import re


# Tests the basic functionality of the website with user perspective
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):  # Starts the webdriver
        self.browser = webdriver.Firefox()

        # self.browser.implicitly_wait(3)

    # Shuts down the webdriver
    def tearDown(self):
        self.browser.quit()

    # Tests the links and forms in the Homepage
    def test_homepage_links_and_forms_post_method(self):
        # Fetches the browser page from the current url
        self.browser.get(self.live_server_url)
        # Checks if title of the fetched browser page matches "vPhrase"
        self.assertIn('vPhrase', self.browser.title)
        # Checks if header of the fetched browser page is "Send Mail"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Send Mail', header_text)
        # If the correct form is rendered in home_page
        form = self.browser.find_element_by_tag_name('form')
        # by checking the placeholder of the email input field
        inputbox = form.find_element_by_id('id_email_address')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'spam.free@yourmail.com')
        # Email input is provided
        inputbox.send_keys('abc@gmail.com')
        # Browser waits for 1 sec
        time.sleep(1)
        button = self.browser.find_element_by_id('subscribe')
        # Submits the input Email
        button.click()

        saved_email = SubscribedEmail.objects.first()
        pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        # If the input email is of valid format
        if re.match(pattern, saved_email.email_address):
            # and matches the user input previously given
            self.assertEqual(saved_email.email_address, 'abc@gmail.com')

            request = HttpRequest()
            request.method = "POST"
            response = home(request)
            # print(response)
            # Checks if the anchor tag with link text "Log In"
            anchor = self.browser.find_element_by_link_text('Log In')
            # has a valid href url
            self.assertIn(reverse('login'), anchor.get_attribute('href'))
            # Checks if the anchor tag with link text "Upload Templates"
            upload_template = self.browser.find_element_by_link_text('Upload Templates')
            # has a valid href url
            self.assertIn(reverse('basic:upload_templates'), upload_template.get_attribute('href'))

        else:
            # If the email is of invalid format, the test ends with failure meassage
            self.fail('Finish the test!')
        # If the already existing email can be used to register
        form = self.browser.find_element_by_tag_name('form')
        # by again providing the previous email input
        inputbox = form.find_element_by_id('id_email_address')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'spam.free@yourmail.com')

        inputbox.send_keys('abc@gmail.com')
        # If the input is similar to previous one i.e "abc@gmail.com"
        if SubscribedEmail.objects.filter(email_address='abc@gmail.com').exists():
            # self.fail()# then the 'user already exists' error is displayed and form is not accepted
            print("User already exists")
        else:
            time.sleep(1)  # Else the form is submitted by cicking the submit button
            button = self.browser.find_element_by_id('subscribe')
            button.click()


    def test_if_upload_template_possible_without_login(self):
        self.browser.get(self.live_server_url)

        upload_button = self.browser.find_element_by_link_text('Upload Templates')
        upload_button.click()
        time.sleep(5)

        response= self.client.post('/login/')
        print(response)# Would display 404 error page

    # Testing login with user perceptive
    def test_Testing_the_Login_page(self):
        self.browser.get(self.live_server_url)

        login_button = self.browser.find_element_by_link_text('Log In')
        login_button.click()
        time.sleep(4)
        # print(self.browser.current_url)

        User.objects.create_user(username='test', password='qwerty1234', is_active=True)

        #print(User.objects.first())

        header_text = self.browser.find_element_by_tag_name(
            'h2').text  # Checks if header of the fetched browser page is "Send Mail"

        self.assertIn('Login', header_text)
        # If the corect form is rendered
        form = self.browser.find_element_by_tag_name('form')
        inputbox = form.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox1 = form.find_element_by_id('id_password')
        inputbox1.send_keys('qwerty1234')
        # print("asdf")
        button = form.find_element_by_tag_name('button')
        button.click()
        time.sleep(5)


        # self.assertEqual(self.browser.current_url,'/')
