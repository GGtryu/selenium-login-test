# tests/test_form.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    """Фикстура для запуска Chrome в режиме без интерфейса"""
    options = Options()
    options.add_argument("--headless")              # без окна браузера
    options.add_argument("--no-sandbox")            # важно для CI
    options.add_argument("--disable-dev-shm-usage") # избегает переполнения памяти
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(driver):
    """Проверка успешного входа с правильными данными"""
    driver.get("https://the-internet.herokuapp.com/login")

    # Вводим логин
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("tomsmith")

    # Вводим пароль
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("SuperSecretPassword!")

    # Нажимаем кнопку Login
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Проверяем, что вошли успешно
    success_message = driver.find_element(By.CSS_SELECTOR, ".flash.success")
    assert "You logged into a secure area!" in success_message.text


def test_unsuccessful_login(driver):
    """Проверка неудачного входа с неправильными данными"""
    driver.get("https://the-internet.herokuapp.com/login")

    # Вводим неверный логин
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("invalid_user")

    # Вводим неверный пароль
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("wrong_pass")

    # Нажимаем кнопку Login
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Проверяем наличие сообщения об ошибке
    error_message = driver.find_element(By.CSS_SELECTOR, ".flash.error")
    assert "Your username is invalid!" in error_message.text or "Your password is invalid!" in error_message.text