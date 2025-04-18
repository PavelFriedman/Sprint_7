import requests
import allure
import pytest
from data import OrderData
from urls import Urls

class TestOrderCreate:

    @allure.title('Проверка создания заказа с разными параметрами цвета')
    @allure.description(
        'Система должна позволять указать в заказе один цвет самоката, выбрать сразу оба или не указывать вовсе. '
        'Проверяются код и тело ответа для заказов с разными параметрами: серый, черный, оба цвета, цвет не указан.'
    )
    @pytest.mark.parametrize('order_data', [
        OrderData.order_data_grey_1,
        OrderData.order_data_black_2,
        OrderData.order_data_two_colors_3,
        OrderData.order_data_no_colors_4
    ])
    def test_order_create_color_parametrize_success(self, order_data):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(Urls.URL_orders_create, json=order_data, headers=headers, timeout=5)
        response_data = response.json()
        assert response.status_code == 201, f"Ошибка создания заказа, статус: {response.status_code}"
        assert 'track' in response_data, "Ответ не содержит ключа 'track'"
