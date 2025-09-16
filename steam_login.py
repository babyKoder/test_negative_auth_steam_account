import time

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


@pytest.mark.parametrize('link',['https://store.steampowered.com/'])
def test_negative_authorization(browser, link):
    wait = WebDriverWait(browser, 10)
    browser.get(link)

    btn_entrance = wait.until(EC.element_to_be_clickable(
        ('xpath','//*[@id="global_action_menu"]/child::a[contains(@class,"global_action_link")]')
    ))
    btn_entrance.click()
    input_login = wait.until(EC.visibility_of_element_located(
        ('xpath','//*[contains(text(),"Войдите, используя имя")]/following-sibling::input')
    ))
    input_login.send_keys('login')

    input_pass = wait.until(EC.visibility_of_element_located(
        ('xpath', '//*[contains(text(),"Пароль")]/following-sibling::input')
    ))

    input_pass.send_keys('qwerty123')
    btn_auth = wait.until(EC.element_to_be_clickable(
        ('xpath','//button[contains(text(),"Войти")]')
    ))

    btn_auth.click()
    error_message = wait.until(EC.element_to_be_clickable(
        ('xpath','//*[contains(text(),"Пожалуйста, проверьте свой ")]')
    ))

    assert (error_message.text ==
            "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова.")

    time.sleep(2)

