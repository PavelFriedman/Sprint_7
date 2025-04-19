import requests
import allure
import pytest
from urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname

@pytest.fixture
def courier_payload():
    """
    Фикстура генерирует уникальные данные курьера для тестов.
    После теста курьер будет удалён по ID.
    """
    login = create_random_login()
    password = create_random_password()
    first_name = create_random_firstname()
    payload = {
        'login': login,
        'password': password,
        'firstName': first_name
    }
    yield payload

    # teardown: удаляем созданного курьера
    # сначала авторизуемся, чтобы получить ID
    login_resp = requests.post(Urls.URL_courier_login, data=payload, timeout=5)
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get('id')
        if courier_id:
            delete_url = f"{Urls.URL_basic}api/v1/courier/{courier_id}"
            requests.delete(delete_url, timeout=5)


class TestCourierCreate:

    @allure.title('Проверка успешного создания аккаунта курьера')
    @allure.description('После создания проверяется код 201 и {"ok": true}, затем курьер удаляется фикстурой.')
    def test_create_courier_account_success(self, courier_payload):
        create_resp = requests.post(Urls.URL_courier_create, data=courier_payload, timeout=5)
        assert create_resp.status_code == 201, f"Ожидается 201, получен {create_resp.status_code}"
        assert create_resp.json() == {'ok': True}, f"Ожидается {{'ok': True}}, получено {create_resp.json()}"

    @allure.title('Проверка ошибки при дублировании регистрации курьера')
    @allure.description('Сначала создаём курьера, затем повторно отправляем тот же payload и проверяем код 409.')
    def test_create_courier_account_login_taken_conflict(self, courier_payload):
        # Первый запрос – успешный
        first_resp = requests.post(Urls.URL_courier_create, data=courier_payload, timeout=5)
        assert first_resp.status_code == 201, "Предварительное создание курьера не удалось"

        # Второй запрос с теми же данными – конфликт
        second_resp = requests.post(Urls.URL_courier_create, data=courier_payload, timeout=5)
        assert second_resp.status_code == 409, f"Ожидается 409, получен {second_resp.status_code}"
        # API может возвращать и {"message": "...", "code": 409}
        body = second_resp.json()
        assert 'message' in body, "В ответе нет поля message"
        assert 'логин' in body['message'].lower(), "Сообщение не про дублирование логина"

    @allure.title('Проверка ошибки при создании курьера с пустыми обязательными полями')
    @allure.description('Пустой логин или пароль – проверяем код 400 и сообщение об ошибке.')
    @pytest.mark.parametrize('empty_payload', [
        {'login': '',               'password': create_random_password(),  'firstName': create_random_firstname()},
        {'login': create_random_login(), 'password': '',                'firstName': create_random_firstname()}
    ])
    def test_create_courier_account_with_empty_required_fields(self, empty_payload):
        resp = requests.post(Urls.URL_courier_create, data=empty_payload, timeout=5)
        assert resp.status_code == 400, f"Ожидается 400, получен {resp.status_code}"
        body = resp.json()
        assert 'message' in body, "В ответе нет поля message"
        assert 'недостаточно данных' in body['message'].lower(), f"Неправильное сообщение: {body}"
