from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC


class ProfilePage:
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait

    def connect(self):
        try:
            try:
                connect_btn = self.browser.find_element_by_css_selector(
                    '.pv-s-profile-actions.pv-s-profile-actions--connect.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')
                connect_btn.click()
            except Exception as e:
                print(e, "Dropdown connect")
                more_btn = self.browser.find_element_by_css_selector(
                    '.ml2.artdeco-dropdown__trigger--placement-bottom.ember-view')
                more_btn.click()
                time.sleep(1)
                connect_btn = self.browser.find_element_by_css_selector(
                    '.pv-s-profile-actions.pv-s-profile-actions--connect.artdeco-dropdown__item')
                connect_btn.click()
            time.sleep(1)
            try:
                add_a_note_btn = self.browser.find_element_by_css_selector('.mr1.artdeco-button.artdeco-button--muted.artdeco-button--3.artdeco-button--secondary.ember-view')
                add_a_note_btn.click()
                time.sleep(1)
                msg_textarea = self.browser.find_element_by_css_selector('.send-invite__custom-message')
                msg_textarea.send_keys('Hi there, excited to work with you as a fellow HP Summer Scholar.')
                send_btn = self.browser.find_element_by_css_selector(
                    '.ml1.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view')
                send_btn.click()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        time.sleep(1)


class FeedPage:
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait

    def go_to_profile_page(self, link):
        try:
            self.browser.get(str(link))
        except Exception as e:
            print(e)
            return False
        sleep(2)
        return ProfilePage(self.browser, self.wait)


class LoginPage:
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector("input[name='session_key']")
        password_input = self.browser.find_element_by_css_selector("input[name='session_password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.btn__primary--large.from__button--floating'))
        )
        login_button.click()
        sleep(2)
        try:
            security = self.browser.find_element_by_xpath('//*[@id="app__container"]/main/h1')
            n = input()
        except Exception as e:
            print(e)
        sleep(2)
        return FeedPage(self.browser, self.wait)


class HomePage:
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait
        self.browser.get('https://www.linkedin.com/')

    def go_to_login_page(self):
        login_btn = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/nav/a[3]'))
        )
        login_btn.click()
        return LoginPage(self.browser, wait)


email = input("Please enter your email address... ")
password = getpass.getpass(prompt="Password...(Typed characters will not be visible )")

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
wait = WebDriverWait(browser, 10)

home_page = HomePage(browser, wait)
sleep(2)
login_page = home_page.go_to_login_page()
sleep(2)
feed_page = login_page.login(email, password)
sleep(2)

df = pd.read_excel('hp-new.xlsx', skiprows=1, usecols=['LinkedIn'])
for i in df['LinkedIn']:
    profile_page = feed_page.go_to_profile_page(i)
    if profile_page:
        profile_page.connect()
        time.sleep(1)
