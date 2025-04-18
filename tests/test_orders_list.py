import requests
import allure
from urls import Urls

class TestOrdersListGet:

    @allure.title('Проверка получения списка заказов')
    @allure.description(
        'Проверяется код ответа и структура тела: поле orders должно быть списком, а если список не пустой, у первого заказа должен быть ключ id.'
    )
    def test_orders_list_get_success(self):
        response = requests.get(Urls.URL_orders_create)
        assert response.status_code == 200, f"Ожидается статус 200, получен {response.status_code}"
        response_data = response.json()
        assert 'orders' in response_data, "В ответе отсутствует ключ 'orders'"
        orders = response_data['orders']
        assert isinstance(orders, list), "Поле 'orders' не является списком"
        if orders:
            assert 'id' in orders[0], "У первого заказа отсутствует поле 'id'"
        else:
            allure.attach("Список заказов пуст", name="Информация", attachment_type=allure.attachment_type.TEXT)
