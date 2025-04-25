from scooter_api import ScooterApi
import allure

class TestGetOrders:
    @allure.title("Получение списка заказов")
    @allure.description("Проверка, что запрос возвращает список заказов в теле ответа")
    def test_response_contains_order_list(self): # проверяет, что тело ответа содержит список заказов
        with allure.step("Отправка запроса на получение списка заказов"):
            response = ScooterApi.get_order()
        with allure.step("Проверка кода ответа и структуры ответа"):
            assert response.status_code == 200
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)  # Проверка, что orders — это список