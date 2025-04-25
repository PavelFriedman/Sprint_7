import allure
import pytest
from scooter_api import ScooterApi
import data

class TestCreateCounter:
    @allure.title("Создание курьера: успешный запрос")
    @allure.description("Проверка, что курьера можно создать, возвращается код 201 и тело ответа {'ok': true}")
    def test_create_courier_returns_201_and_ok_response(self, manage_courier_credentials):
        payload = manage_courier_credentials
        with allure.step("Отправка запроса на создание курьера"):
            response = ScooterApi.create_courier(payload)
        with allure.step("Проверка кода ответа и тела ответа"):
            assert response.status_code == 201
            assert response.text == '{"ok":true}'

    @allure.title("Создание курьера: дубликат курьера")
    @allure.description("Проверка, что нельзя создать двух одинаковых курьеров с одинаковыми данными")
    def  test_cannot_create_duplicate_couriers(self, manage_courier_credentials):
        payload = manage_courier_credentials
        with allure.step("Создание первого курьера"):
            ScooterApi.create_courier(payload)
        with allure.step("Повторная отправка запроса с теми же данными"):
            response = ScooterApi.create_courier(payload)
        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 409
            assert response.json()["message"] == data.COURIER_LOGIN_ALREADY_USED

    @allure.title("Создание курьера: дубликат логина")
    @allure.description("Проверка, что нельзя создать курьера с уже существующим логином")
    def test_courier_creation_fails_for_duplicate_login(self, manage_courier_credentials):
        payload = manage_courier_credentials
        with allure.step("Создание первого курьера"):
            ScooterApi.create_courier(payload)
        payload_duplicate_login = data.COURIER_CREDENTIALS_ONE
        payload_duplicate_login["login"] = payload["login"] # заменили значение login
        with allure.step("Создание второго курьера с тем же логином"):
            response = ScooterApi.create_courier(payload_duplicate_login)
        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 409
            assert response.json()["message"] == data.COURIER_LOGIN_ALREADY_USED

    @pytest.mark.parametrize('data_test', [data.COURIER_CREDENTIALS_WITHOUT_LOGIN, data.COURIER_CREDENTIALS_WITHOUT_PASSWORD])
    @allure.title("Создание курьера: отсутствие обязательных полей")
    @allure.description("Проверка, что нельзя создать курьера без логина или пароля")
    def test_create_courier_without_required_fields(self, data_test): # проверяет, что нельзя создать курьера без логина и без пароля
        payload = data_test
        with allure.step("Отправка запроса на создание курьера с отсутствующим полем"):
            response = ScooterApi.create_courier(payload)
        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == data.COURIER_CREATION_MISSING_DATA