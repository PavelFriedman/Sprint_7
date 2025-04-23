import requests
import allure
import pytest
import json
from data import OrderData
from urls import Urls

class TestOrderCreate:

    @allure.title('Проверка создания и отмены заказа с разными параметрами цвета')
    @allure.description(
        'Система должна позволять указать в заказе один цвет самоката, выбрать сразу оба или не указывать вовсе. '
        'После создания заказ отменяется, чтобы не оставлять тестовые данные.'
    )
    @pytest.mark.parametrize('order_data', [
        OrderData.order_data_grey_1,
        OrderData.order_data_black_2,
        OrderData.order_data_two_colors_3,
        OrderData.order_data_no_colors_4
    ])
    def test_order_create_and_cancel(self, order_data):
        # 1. Создаём заказ
        payload = json.dumps(order_data)
        headers = {'Content-Type': 'application/json'}
        create_resp = requests.post(
            Urls.URL_orders_create,
            data=payload,
            headers=headers,
            timeout=5
        )
        assert create_resp.status_code == 201, f"Ошибка создания заказа, статус: {create_resp.status_code}"
        create_data = create_resp.json()
        assert 'track' in create_data, "Ответ не содержит ключа 'track'"

        # 2. Отменяем заказ, передавая track в query-параметре
        track = create_data['track']
        cancel_url = f"{Urls.URL_orders_cancel}?track={track}"
        cancel_resp = requests.put(cancel_url, timeout=5)
        assert cancel_resp.status_code == 200, f"Ошибка отмены заказа, статус: {cancel_resp.status_code}"
        cancel_data = cancel_resp.json()
        assert cancel_data.get('ok') is True, f"Неверный ответ при отмене заказа: {cancel_data}"
