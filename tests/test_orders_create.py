import requests
import allure
import pytest
from data import OrderData
from urls import Urls

class TestOrderCreate:

    @allure.title('Проверка создания заказа с разными параметрами цвета и отмена после создания')
    @allure.description(
        'Система должна позволять указать в заказе один цвет самоката, выбрать сразу оба или не указывать вовсе. '
        'После создания заказа он отменяется, чтобы не накапливать тестовые данные.'
    )
    @pytest.mark.parametrize('order_data', [
        OrderData.order_data_grey_1,
        OrderData.order_data_black_2,
        OrderData.order_data_two_colors_3,
        OrderData.order_data_no_colors_4
    ])
    def test_order_create_and_cancel(self, order_data):
        headers = {'Content-Type': 'application/json'}
        # Создаём заказ
        response = requests.post(Urls.URL_orders_create, json=order_data, headers=headers, timeout=5)
        assert response.status_code == 201, f"Ошибка создания заказа, статус: {response.status_code}"
        response_data = response.json()
        assert 'track' in response_data, "Ответ не содержит ключа 'track'"

        track = response_data['track']
        # Отменяем заказ, чтобы "почистить" данные
        cancel_payload = {'track': track}
        cancel_response = requests.put(Urls.URL_orders_cancel, json=cancel_payload, timeout=5)
        # Проверяем, что отмена прошла успешно (обычно возвращает 200 или 202)
        assert cancel_response.status_code == 200, f"Ошибка при отмене заказа, статус: {cancel_response.status_code}"
