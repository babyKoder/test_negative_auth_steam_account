import random

import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


LINK = 'https://store.steampowered.com/'
TIMEOUT = 10
LENGTH_PASS = random.randint(1,60)
EMAIL_DOMAIN = 'example.com'
BTN_ENTRANCE_LOCATOR = (By.XPATH, '//*[contains(@class, "global_action_link") and @href]')
INPUT_LOGIN_LOCATOR = (By.XPATH, '//*[@data-featuretarget="login"]//input[@type="text"]')
INPUT_PASS_LOCATOR = (By.XPATH, '//*[@data-featuretarget="login"]//input[@type="password"]')
BTN_AUTH_LOCATOR = (By.XPATH, '//*[@data-featuretarget="login"]//button')
ERROR_MESSAGE_LOCATOR = (By.XPATH, '//*[@data-featuretarget="login"]//button/parent::div/following-sibling::div')


def test_negative_authorization(browser):
    wait = WebDriverWait(browser, TIMEOUT)
    browser.get(LINK)

    btn_entrance = wait.until(EC.element_to_be_clickable(BTN_ENTRANCE_LOCATOR))
    btn_entrance.click()

    input_login = wait.until(EC.visibility_of_element_located(INPUT_LOGIN_LOCATOR))
    input_login.send_keys(Faker().email(True,EMAIL_DOMAIN))

    input_pass = wait.until(EC.visibility_of_element_located(INPUT_PASS_LOCATOR))
    input_pass.send_keys(Faker().password(LENGTH_PASS, True, True, True))

    btn_auth = wait.until(EC.element_to_be_clickable(BTN_AUTH_LOCATOR))
    btn_auth.click()

    wait.until(EC.element_attribute_to_include(BTN_AUTH_LOCATOR, "disabled"))
    wait.until_not(EC.element_attribute_to_include(BTN_AUTH_LOCATOR, "disabled"))

    error_message = wait.until(EC.visibility_of_element_located(ERROR_MESSAGE_LOCATOR))
    actual_error = error_message.text

    expected_error = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."

    assert actual_error == expected_error, f"Ожидаемое значение - {expected_error}, а Фактическое - {actual_error}"
