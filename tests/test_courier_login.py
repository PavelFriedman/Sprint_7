import requests
import allure
import pytest
from data import Data
from urls import Urls
from helpers import create_random_login, create_random_password

class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    @allure.description('Happy path. Проверяются код и присутствие ID в ответе.')
    def test_courier_login_success(self):
        response = requests.post(Urls.URL_courier_login, data=Data.valid_courier_data, timeout=5)
        assert response.status_code == 200, f"Ожидается 200, получен {response.status_code}"
        body = response.json()
        assert 'id' in body and isinstance(body['id'], int), f"В ответе нет корректного поля 'id': {body}"

    @allure.title('Проверка ошибки аутентификации с несуществующими данными')
    @allure.description('Передаются либо случайный логин, либо неверный пароль — ожидаем 404 и сообщение.')
    @pytest.mark.parametrize('bad_credentials', [
        {'login': create_random_login(), 'password': create_random_password()},
        Data.courier_data_with_wrong_password
    ])
    def test_courier_login_nonexistent_data_not_found(self, bad_credentials):
        response = requests.post(Urls.URL_courier_login, data=bad_credentials, timeout=5)
        assert response.status_code == 404, f"Ожидается 404, получен {response.status_code}"
        body = response.json()
        # Проверяем, что есть сообщение об ошибке
        assert 'message' in body, f"В ответе нет поля 'message': {body}"
        assert 'не найдена' in body['message'].lower(), f"Неправильное сообщение: {body['message']}"
        # Если API отдаёт код в теле
        if 'code' in body:
            assert body['code'] == 404, f"Ожидается code=404, получен {body['code']}"

    @allure.title('Проверка ошибки аутентификации с пустым логином или паролем')
    @allure.description('Проверяются два варианта: пустой логин и пустой пароль — ожидаем 400 и сообщение.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '',                    'password': create_random_password()},
        {'login': Data.valid_login,      'password': ''}
    ])
    def test_courier_login_empty_credentials_bad_request(self, empty_credentials):
        response = requests.post(Urls.URL_courier_login, data=empty_credentials, timeout=5)
        assert response.status_code == 400, f"Ожидается 400, получен {response.status_code}"
        body = response.json()
        assert 'message' in body, f"В ответе нет поля 'message': {body}"
        assert 'недостаточно данных' in body['message'].lower(), f"Неправильное сообщение: {body['message']}"
        if 'code' in body:
            assert body['code'] == 400, f"Ожидается code=400, получен {body['code']}"
