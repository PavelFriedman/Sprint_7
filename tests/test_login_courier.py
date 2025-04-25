import allure
import pytest
import data
from scooter_api import ScooterApi
from helper import Helper

class TestLoginCounter:
    @allure.title("Логин курьера: успешная авторизация")
    @allure.description("Проверка, что курьер может авторизоваться и возвращается id")
    def test_courier_successful_login_returns_id(self, register_new_courier_and_return_login_password):
        login_pass = register_new_courier_and_return_login_password
        payload = {  # собираем данные из списка для body (можно было сразу вернуть словарь в фикстуре, сделано для демонстрации вариантов использования)
                "login": login_pass[0],
                "password": login_pass[1],
                "first_name": login_pass[2]
        }
        with allure.step("Отправка запроса на авторизацию курьера"):
            response = ScooterApi.login_courier(payload)
        with allure.step("Проверка кода ответа и наличия id"):
            assert response.status_code == 200
            assert 'id' in response.json()

    @pytest.mark.parametrize("modify_field", ["login", "password"])
    @allure.title("Логин курьера: отсутствие обязательных полей")
    @allure.description("Проверка, что авторизация с пустым логином или паролем возвращает ошибку")
    def test_courier_login_without_required_fields_returns_error(self, register_new_courier_and_return_login_password, modify_field):
        login_pass = register_new_courier_and_return_login_password
        payload = { # данные созданного пользователя
            "login": login_pass[0],
            "password": login_pass[1],
            "first_name": login_pass[2]
        }
        payload[modify_field] = ""  # Подменяем одно из значений в реальных кредах под кейс
        with allure.step("Отправка запроса на авторизацию с пустым полем"):
            response = ScooterApi.login_courier(payload)
        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == data.LOGIN_MISSING_DATA

    @pytest.mark.parametrize("modify_field", ["login", "password"])
    @allure.title("Логин курьера: некорректные данные")
    @allure.description("Проверка, что авторизация с некорректным логином или паролем возвращает ошибку")
    def test_courier_login_incorrect_login_returns_error(self, register_new_courier_and_return_login_password, modify_field):
        login_pass = register_new_courier_and_return_login_password
        payload = { # данные созданного пользователя
            "login": login_pass[0],
            "password": login_pass[1],
            "first_name": login_pass[2]
        }
        payload[modify_field] = Helper.random_string()  # Подменяем одно из значений в реальных кредах под кейс
        with allure.step("Отправка запроса на авторизацию с некорректным полем"):
            response = ScooterApi.login_courier(payload)
        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == data.ACCOUNT_NOT_FOUND

    @allure.title("Логин курьера: несуществующий пользователь")
    @allure.description("Проверка, что авторизация под несуществующим пользователем возвращает ошибку")
    def test_courier_login_with_nonexistent_credentials_returns_error(self):
        payload = data.NON_EXISTENT_COURIER_CREDENTIALS
        with allure.step("Отправка запроса на авторизацию с несуществующими данными"):
            response = ScooterApi.login_courier(payload)
        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == data.ACCOUNT_NOT_FOUND
