#Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, ссылка)
#Логин тестового ящика: study.ai_172@mail.ru
#Пароль тестового ящика: NextPassword172#

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pymongo import MongoClient


service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(15)
driver.get('https://account.mail.ru/')
driver.maximize_window()
client = MongoClient('127.0.0.1', 27017)
data_base = client['mail_db']
collection = data_base['letters']


elem = driver.find_element(By.NAME, 'username')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)


list_letters = []
last_message = None
while True:
    messages = driver.find_elements(By.XPATH, "//a[contains(@class, 'llc')]")
    if messages[-1] == last_message:
        break
    else:
        try:
            for message in messages:
                link_letter = message.get_attribute('href')
                if link_letter not in list_letters:
                    list_letters.append(link_letter)
                    data_base.letters.insert_one({
                        'sender_letter' : message.find_element(By.XPATH, ".//span[@class='ll-crpt']").text,
                        'subject_letter' : message.find_element(By.XPATH, ".//span[@class='ll-sj__normal']").text,
                        'date_letter' : message.find_element(By.XPATH, ".//div[@class='llc__item llc__item_date']").text,
                        'link_letter' : link_letter
                        })
        except Exception as e:
            print('Больше писем нет')
            break
        last_message = messages[-1]
    action = ActionChains(driver)
    action.move_to_element(messages[-1]).perform()
    sleep(4)
    continue
print(f'всего добавлено {data_base.letters.count_documents({})} писем')

driver.quit()

