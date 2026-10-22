from django.test import TestCase


import os
import time
 
import pytest
import pytest_check as check
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Create your tests here.

URL = "http://127.0.0.1:8000/"
PASSWORD = "Str0ng!Pass2026"
WRONG_PASS = 'WrongPass123'
USER_NAME = f'student_test'

@pytest.fixture()
def driver():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def page_text(driver):
    body = driver.find_element(By.TAG_NAME, 'body')
    return body.get_attribute('textContent')

def register(driver, username):
    driver.get(f'{URL}/signup/')

    driver.find_element(By.ID, 'id_username').send_keys(username)
    driver.find_element(By.ID, 'id_password1').send_keys(PASSWORD)
    driver.find_element(By.ID, 'id_password2').send_keys(PASSWORD)

    driver.find_element(By.CSS_SELECTOR, 'form button.btn').click()

    time.sleep(2)

    print("Поточна адреса:", driver.current_url)
    print("Текст сторінки:", page_text(driver))

   


def test_register(driver):
    register(driver,USER_NAME)

    text = page_text(driver)

    check.equal(driver.current_url, f'{URL}')
    check.is_in('Реєстрація пройшла успішно', text)
    check.is_in(f'Привіт, {USER_NAME}', text)
    check.is_in('Вийти', text)

