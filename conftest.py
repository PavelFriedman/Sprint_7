# conftest.py
import pytest
import requests
from helpers import create_random_login, create_random_password, create_random_firstname
from urls import Urls

@pytest.fixture
def created_courier():
    """
    Фикстура:
    - генерирует уникальные данные курьера
    - создаёт курьера (POST /courier) и проверяет 201 + {'ok': True}
    - отдаёт в тест payload и тело ответа
    - в teardown авторизуется, получает ID и удаляет курьера
    """
    # Генерация
    payload = {
        'login': create_random_login(),
        'password': create_random_password(),
        'firstName': create_random_firstname()
    }
    # Setup: создание
    create_resp = requests.post(Urls.URL_courier_create, data=payload, timeout=5)
    assert create_resp.status_code == 201, f"Setup failed: expected 201, got {create_resp.status_code}"
    assert create_resp.json() == {'ok': True}, f"Setup failed: unexpected body {create_resp.json()}"

    yield payload, create_resp.json()

    # Teardown: удаляем курьера по ID
    login_resp = requests.post(Urls.URL_courier_login, data=payload, timeout=5)
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get('id')
        if courier_id:
            delete_url = f"{Urls.URL_basic}api/v1/courier/{courier_id}"
            requests.delete(delete_url, timeout=5)
