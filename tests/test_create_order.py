import allure
import pytest
from scooter_api import ScooterApi


class TestCreateOrder:
    @pytest.mark.parametrize('color', [
        ["BLACK", "GREY"],
        ["BLACK"],
        ["GREY"],
        []
    ])
    @allure.title("Создание заказа: различные варианты цветов")
    @allure.description("Проверка, что заказ создаётся с разными комбинациями цветов и возвращает track")
    def test_create_order_with_different_color_options(self, create_data_and_cancel_order, color):
        data_order, track_container = create_data_and_cancel_order  # Распаковка фикстуры
        data_order["color"] = color
        with allure.step("Отправка запроса на создание заказа"):
            response = ScooterApi.create_order(data_order)
        with allure.step("Проверка кода ответа и наличия track"):
            assert response.status_code == 201
            assert "track" in response.json()
        with allure.step("Сохранение track для отмены заказа"):
            track_container["track"] = response.json()["track"]