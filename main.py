import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time, random

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

user = config['user']
password = config['password']
text = config['text']

with open('person_list.txt', 'r', encoding='utf-8') as person_file:  # Прописать удаление использованных никнеймов
    person_list = [line.strip() for line in person_file.readlines()]

def start_selenium():
    PATH = "C:\\drivers\\chromedriver.exe"
    service = Service(executable_path=PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=en_US")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.instagram.com")
    driver.implicitly_wait(10)

    # Пропуск кукі
    pechenki_xpath = "//button[contains(@class, '_a9-- _ap36 _a9_0') and text()='Allow all cookies']"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, pechenki_xpath))
    )
    pechenki_button = driver.find_element(By.XPATH, pechenki_xpath)
    pechenki_button.click()

    driver.implicitly_wait(10)

    # Логування
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    user_input = driver.find_element(By.NAME, "username")
    user_input.send_keys(user)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(password)

    login_xpath = "//button[contains(@class, '_acan') and div[text()='Log in']]"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, login_xpath))
    )
    login_button = driver.find_element(By.XPATH, login_xpath)
    login_button.click()

    # Нот нау вікно
    not_now_xpath = "//div[contains(@class, 'x1i10hfl') and text()='Not now']"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, not_now_xpath))
    )
    not_now_button = driver.find_element(By.XPATH, not_now_xpath)
    not_now_button.click()

    return driver  

def send_message(driver, person, message):
    try:
        # Перехід до Direct messaging
        msg_sec_xpath = "//a[contains(@aria-label, 'Direct messaging')]"
        WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, msg_sec_xpath))
        )
        msg_sec = driver.find_element(By.XPATH, msg_sec_xpath)
        msg_sec.click()

        # нік
        send_button_xpath = "//div[@role='button' and contains(text(), 'Send message')]"
        WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, send_button_xpath))
        )
        send_button = driver.find_element(By.XPATH, send_button_xpath)
        send_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "queryBox"))
        )
        search_input = driver.find_element(By.NAME, "queryBox")
        search_input.send_keys(person)

        time.sleep(5)  # Пауза

        checkbox_xpath = "//input[@aria-label='Radio selection']"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        checkbox = driver.find_element(By.XPATH, checkbox_xpath)
        checkbox.click()

        chat_xpath = "//div[contains(@class, 'x1i10hfl') and contains(text(), 'Chat')]"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, chat_xpath))
        )
        chat_button = driver.find_element(By.XPATH, chat_xpath)
        chat_button.click()

        # Ввод тексту
        message_box = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-placeholder='Message...']"))
        )
        message_box.click()

        for line in message.split('\n'):
            message_box.send_keys(line)
            message_box.send_keys(Keys.SHIFT + Keys.ENTER)
        
        message_box.send_keys(Keys.ENTER)

        time.sleep(5)
    except Exception as e:

        with open('mes_error.txt', 'a', encoding='utf-8') as error_file:
            error_file.write(f"error 1: {person}\n")
        print(f"unknown error: {person}: {e}")

    time.sleep(5)

driver = start_selenium()

for person in person_list:
    send_message(driver, person, text)
    wait_time = random.randint(10, 25) # Пауза між відправками, від 10 до 25
    time.sleep(wait_time)   

driver.quit()
