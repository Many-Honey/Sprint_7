import allure
import requests
from urls import *


# тесты для ручки /api/v1/courier/login
class TestLoginCourier:

    @allure.title('Проверка успешного входа в систему зарегистрированного курьера')
    @allure.description('Проверяем, что передав в тело запроса обязательные данные "login", "password" ранее зарегистрированного курьера, вернется код ответа 200 и в теле ответа будет id курьера')
    # проверка успешного входа в систему зарегистрированного курьера
    def test_successful_login_code200(self, register_new_courier_return_login_password_delete_courier):
        login_pass = register_new_courier_return_login_password_delete_courier
        payload_login = {
            "login": login_pass[0],
            "password": login_pass[1]}
        response = requests.post(URL_LOGIN, data=payload_login)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Попытка входа в систему без указания логина выдает ошибку')
    @allure.description('Проверяем, что при отправке запроса на вход без указания логина вернется код 400 и сообщение {"code": 400, "message": "Недостаточно данных для входа"}')
    # попытка входа в систему без указания логина выдает ошибку
    def test_login_without_login_code400(self, register_new_courier_return_login_password_delete_courier):
        login_pass = register_new_courier_return_login_password_delete_courier
        payload_login = {"login": "",
            "password": login_pass[1]}
        response = requests.post(URL_LOGIN, data=payload_login)
        assert response.status_code == 400
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title('Попытка входа в систему без указания пароля выдает ошибку')
    @allure.description('Проверяем, что при отправке запроса на вход без указания пароля вернется код 400 и сообщение {"code": 400, "message": "Недостаточно данных для входа"}')
    # попытка входа в систему без указания пароля выдает ошибку
    def test_login_without_password_code400(self, register_new_courier_return_login_password_delete_courier):
        login_pass = register_new_courier_return_login_password_delete_courier
        payload_login = {"login": login_pass[0],
                         "password": ""}
        response = requests.post(URL_LOGIN, data=payload_login)
        assert response.status_code == 400
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title('Попытка входа в систему с незарегистрированной парой логин-пароль выдает ошибку')
    @allure.description("Проверяем, что при отправке запроса на вход с незарегистрированной парой логин-пароль вернется код 404 и сообщение {'code': 404, 'message': 'Учетная запись не найдена'}")
    # попытка входа в систему с незарегистрированным логином и паролем выдает ошибку
    def test_login_with_unregistered_login_code404(self, generate_request_body):
        payload = generate_request_body
        payload_login = {"login": payload["login"],
            "password": payload["password"]}
        response = requests.post(URL_LOGIN, data=payload_login)
        assert response.status_code == 404
        assert response.json() == {'code': 404, 'message': 'Учетная запись не найдена'}


