import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


LINKS = [
    'https://store.steampowered.com/'
]
TIMEOUT = 10

@pytest.mark.parametrize('link', LINKS)
def test_negative_authorization(browser, link):
    wait = WebDriverWait(browser, TIMEOUT)
    browser.get(link)

    btn_entrance_locator = (By.XPATH,'//*[@id="global_action_menu"]/child::a[contains(@class,"global_action_link")]')
    btn_entrance = wait.until(EC.element_to_be_clickable(btn_entrance_locator))
    btn_entrance.click()

    input_login_locator = (By.XPATH,'//*[contains(text(),"Войдите, используя имя")]/following-sibling::input')
    # .//input[@type="text"] вот так находит 4 элемента
    input_login = wait.until(EC.visibility_of_element_located(input_login_locator))
    input_login.send_keys('login')

    input_pass_locator =  (By.XPATH, '//*[contains(text(),"Пароль")]/following-sibling::input')
    input_pass = wait.until(EC.visibility_of_element_located(input_pass_locator))
    input_pass.send_keys('qwerty123')

    btn_auth_locator = (By.XPATH,'//button[contains(text(),"Войти")]')
    btn_auth = wait.until(EC.element_to_be_clickable(btn_auth_locator))
    btn_auth.click()

    error_message_locator = (By.XPATH,'//*[contains(text(),"Пожалуйста, проверьте свой ")]')
    error_message = wait.until(EC.element_to_be_clickable(error_message_locator))

    actual_error = error_message.text
    expected_error = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."
    assert (
        actual_error == expected_error,
        f"Ожидаемое значение - {expected_error}, а Фактическое - {actual_error}"
    )


