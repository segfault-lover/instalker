from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from typing import List
from time import sleep
import sys

import config

class Bot:
    def __init__(self, username: str, password: str):
        self.driver = webdriver.Chrome()
        self.driver.get('https://instagram.com')

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name=\"username\"]"))).send_keys(username)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name=\"password\"]"))).send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type=\"submit\"]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        # This sleep is necessary because if the internet is not fast enough, the story is not clickable yet and clicking the profile picture will lead to your own profile
        sleep(2)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/section/div[3]/div[1]/div/div/div[1]/div"))).click()

    def get_viewers(self) -> List[str]:
        sleep(1)

        if len(self.driver.find_elements_by_xpath("/html/body/div[1]/section/div[1]/div/section/div/div[3]/div[2]/button")) == 0:
            print("No one has seen your story yet!")
            return None
        else:
            self.driver.find_elements_by_xpath("/html/body/div[1]/section/div[1]/div/section/div/div[3]/div[2]/button").click()

        scroll_box = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div")))
        last_ht, ht = 0, 1
        names = []
        
        while last_ht != ht:
            last_ht = ht
            sleep(1.5)
            links = scroll_box.find_elements_by_tag_name('a')
            newname = [name.text for name in links if name.text != '']

            [names.append(name) for name in newname if name not in names]

            try:
                scroll_box = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div")))

                ht = self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight; return arguments[0].scrollTop', scroll_box)
            except StaleElementReferenceException:
                scroll_box = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div")))

                ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div/div[1]/div/div[2]/button"))).click()

        return names

if __name__ == '__main__':
    bot = Bot(config.USERNAME, config.PASSWORD)

    all_names = []

    while True:
        names = bot.get_viewers()

        for name in names:
            if name not in all_names:
                all_names.append(name)
            
        for name in all_names:
            if name not in names:
                print('suspect:', name)