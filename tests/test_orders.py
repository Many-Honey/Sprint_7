import json
import allure
import pytest
import requests
from urls import *


# тесты для ручки /api/v1/orders
class TestOrders:


    order_data = {
        "firstName": "Мария",
        "lastName": "Иванова",
        "address": "Дыбенко, 14",
        "metroStation": 6,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2025-06-06",
        "comment": ""
    }

    @allure.title('Проверка успешного создания заказа при указании цвета самоката {color}')
    @allure.description('Проверяем что при указании значения {color} в поле "color" заказ будет успешно создан, вернется код 201 и трек заказа')
    @pytest.mark.parametrize('color', [["BLACK"], ["GREY"], [""], ["BLACK", "GREY"]])
    def test_specify_color_in_order_code201(self, color):
        self.order_data["color"] = color
        json_string = json.dumps(self.order_data)
        response = requests.post(URL_ORDERS, data=json_string)
        assert response.status_code == 201
        assert 'track' in response.json()

    @allure.title('Проверка, что в тело ответа возвращается список заказов.')
    @allure.description('Проверяем, что при запросе списка заказов нового зарегистрированного курьера в теле ответа вернется ключ "orders" с пустым списком')
    def test_courier_gets_list_of_orders(self, register_new_courier_return_login_password_delete_courier):
        #/v1/orders?courierId=1
        # получаем id курьера через логин
        login_pass = register_new_courier_return_login_password_delete_courier
        payload_login = {"login": login_pass[0],
                         "password": login_pass[1]}
        response_login = requests.post(URL_LOGIN, data=payload_login)
        courier_id = response_login.json()['id']
        # отправляем запрос на получения списка заказов курьера используя его id
        response_list_of_orders = requests.get(f'{URL_ORDERS}?courierId={courier_id}')
        assert response_list_of_orders.status_code == 200
        assert 'orders' in response_list_of_orders.json()
        assert response_list_of_orders.json()['orders'] == []





