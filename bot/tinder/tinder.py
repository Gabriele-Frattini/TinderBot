import os
from time import sleep
from selenium import webdriver
from .constants import BASE_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .secrets import emailkey, passwordkey
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib


class Tinder(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/users/gabbe/seleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        super(Tinder, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(BASE_URL)
        sleep(2)

    def logIn(self):
        loginButton = self.find_element_by_css_selector(
            'a[data-testid="appLoginBtn"]'
        )
        loginButton.click()
        sleep(3)

        # print(self.current_window_handle)

    def loginButton(self):

        facebookButton = WebDriverWait(self, 5).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "button[type = 'button'][aria-label = 'Logga in via Facebook'] span")))

        facebookButton = self.find_element_by_css_selector(
            "button[type = 'button'][aria-label = 'Logga in via Facebook'] span"
        )
        facebookButton.click()

        sleep(2)

    def loginFacebook(self):
        workspace = self.window_handles[0]
        popup = self.window_handles[1]
        self.switch_to.window(popup)

        cookies = WebDriverWait(self, 7).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "button[value = '1'][data-testid='cookie-policy-manage-dialog-accept-button']")))

        cookies = self.find_element_by_css_selector(
            "button[value = '1'][data-testid='cookie-policy-manage-dialog-accept-button']"
        )
        cookies.click()

        sleep(2)

        username = self.find_element_by_id(
            'email'
        )

        password = self.find_element_by_id(
            'pass'
        )

        username.send_keys(emailkey)
        password.send_keys(passwordkey)

        sleep(2)
        submit = self.find_element_by_css_selector(
            'input[value="Logga in"]'
        )
        submit.click()
        self._switch_to.window(workspace)

    def startPage(self):

        allow = WebDriverWait(self, 5).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="t492665908"]/div/div/div/div/div[3]/button[1]')))

        allow = self.find_element_by_xpath(
            '//*[@id="t492665908"]/div/div/div/div/div[3]/button[1]'
        )
        allow.click()

        cookies = WebDriverWait(self, 7).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="t-2073920312"]/div/div[2]/div/div/div[1]/div[1]/button')))

        cookies = self.find_element_by_xpath(
            '//*[@id="t-2073920312"]/div/div[2]/div/div/div[1]/div[1]/button'
        )
        cookies.click()

        deny = WebDriverWait(self, 5).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "button[aria-label='Inte intresserad']")))

        deny = self.find_element_by_css_selector(
            "button[aria-label='Inte intresserad']"
        )
        deny.click()

    def swipeClassifier(self, swipes):
        model = joblib.load(
            "C:/Users/gabbe/Downloads/web-scraping/bot/model.pkl")

        for swipe in range(swipes):

            try:
                sleep(3)

                bio = self.find_element_by_css_selector(
                    'div[data-testid="recCard_info"]'
                )
                for i in bio.find_elements_by_tag_name("div"):
                    try:
                        if len(i.text) > 25:
                            X = [i.text]
                            prediction = model.predict(X)[0]

                            print(X, prediction)

                            if prediction == 0:
                                dislike = self.find_element_by_css_selector(
                                    'button[type=button][data-testid="gamepadDislike"]'
                                )
                                dislike.click()

                            elif prediction == 1:
                                like = self.find_element_by_css_selector(
                                    'button[type=button][data-testid="gamepadDislike"]'
                                )
                                like.click()

                    except:
                        discard = self.find_element_by_css_selector(
                            'button[type=button][data-testid="gamepadDislike"]'
                        )
                        discard.click()
                        print("Error occured. Trying again..")

            except:
                cancel = self.find_element_by_css_selector(
                    'button[type=button][data-testid="cancel"]'
                )
                cancel.click()
                continue

    def scrapeBio(self):

        bios = []

        for i in range(50):
            try:
                sleep(1)

                info = self.find_element_by_css_selector(
                    'div[data-testid="recCard_info"]'
                )
                for i in info.find_elements_by_tag_name("div"):
                    try:
                        if len(i.text) > 25:
                            bios.append(str(i.text))
                    except:
                        bios.append(" ")

                swipe = self.find_element_by_css_selector(
                    'button[type=button][data-testid="gamepadDislike"]'
                )
                swipe.click()

            except:
                cancel = self.find_element_by_css_selector(
                    'button[type=button][data-testid="cancel"]'
                )
                cancel.click()
                continue

        with open("training_data.txt", "w", encoding="utf-8") as f:
            for bio in bios:
                f.write(str(bio))
