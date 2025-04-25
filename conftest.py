import pytest
import requests
import random
import string
import data
from helper import Helper
from scooter_api import ScooterApi


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
@pytest.fixture # фикстура с созданием и удалением курьера
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    yield login_pass

    # удаление созданного курьера
    response =  ScooterApi.login_courier(payload)
    id_courier = str(response.json()['id'])
    ScooterApi.delete_courier(id_courier)


@pytest.fixture # создание кредов для курьера и удаления курьера по этим данным
def manage_courier_credentials():
    payload = Helper.credentials()
    yield payload # вернули креды в тест
    # удаление курьера со созданным
    response = ScooterApi.login_courier(payload) # логинимся под курьером из теста
    if response.status_code == 200:
        id_courier = str(response.json()['id']) # тащим его id из респонса
        ScooterApi.delete_courier(id_courier) # удаляем по id


@pytest.fixture # возвращает данные для создания заказа и отменяет заказ после теста
def create_data_and_cancel_order():
    data_order = data.BLACK_AND_GRAY # данные заказа
    track_container = {}  # Контейнер для хранения track заказа

    yield data_order, track_container

    if "track" in track_container:
        ScooterApi.cancel_order(track_container)