import requests
import allure
from urls import Urls

class TestOrdersListGet:

    @allure.title('Проверка получения списка заказов')
    @allure.description(
        'Проверяется код ответа и структура тела: поле orders должно быть непустым списком, у первого заказа должен быть ключ id.'
    )
    def test_orders_list_get_success(self):
        response = requests.get(Urls.URL_orders_create)
        assert response.status_code == 200, f"Ожидается статус 200, получен {response.status_code}"

        response_data = response.json()
        assert 'orders' in response_data, "В ответе отсутствует ключ 'orders'"

        orders = response_data['orders']
        assert isinstance(orders, list), "Поле 'orders' не является списком"
        assert orders, "Список заказов не должен быть пустым"

        first_order = orders[0]
        assert 'id' in first_order, "У первого заказа отсутствует поле 'id'"
