# conftest.py
import pytest
import requests
from helpers import create_random_login, create_random_password, create_random_firstname
from urls import Urls

@pytest.fixture
def created_courier():
    """
    Фикстура:
      1) Генерирует данные курьера
      2) Создаёт курьера (POST) — проверка 201 и {'ok': True}
      3) Логинится (POST) — проверка 200 и получение id
      4) Передаёт в тест payload и courier_id
      5) Teardown: удаляет курьера (DELETE) — проверка 200 и {'ok': True}
    """
    # 1) генерация данных
    payload = {
        'login': create_random_login(),
        'password': create_random_password(),
        'firstName': create_random_firstname()
    }

    # 2) создание
    create_resp = requests.post(Urls.URL_courier_create, data=payload, timeout=5)
    assert create_resp.status_code == 201, f"Setup: ожидали 201, получили {create_resp.status_code}"
    assert create_resp.json() == {'ok': True}, f"Setup: unexpected body {create_resp.json()}"

    # 3) логин для получения id
    login_resp = requests.post(Urls.URL_courier_login, data=payload, timeout=5)
    assert login_resp.status_code == 200, f"Setup login: ожидали 200, получили {login_resp.status_code}"
    courier_id = login_resp.json()['id']
    assert isinstance(courier_id, int), f"Setup login: неверный id {courier_id}"

    # Передаём данные в тест
    yield payload, courier_id

    # 5) teardown: удаление
    delete_url = f"{Urls.URL_basic}api/v1/courier/{courier_id}"
    delete_resp = requests.delete(delete_url, timeout=5)
    assert delete_resp.status_code == 200, f"Teardown: ожидали 200, получили {delete_resp.status_code}"
    assert delete_resp.json() == {'ok': True}, f"Teardown: unexpected body {delete_resp.json()}"
