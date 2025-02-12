import allure
import requests
from urls import *


# тесты для ручки /api/v1/courier
class TestCreateCourier:

    message_400 = 'Недостаточно данных для создания учетной записи'
    message_409 = 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка успешной регистрации курьера в системе')
    @allure.description('Проверяем, что передав в тело запроса обязательные уникальные поля "login", "password", "firstName" курьер успешно создастся, вернется код ответа 201 и в теле ответа будет {"ok": True}')
    # проверка успешной регистрации курьера в системе
    def test_successful_creation_code201(self, generate_request_body):
        payload = generate_request_body
        response = requests.post(URL_COURIER, data=payload)
        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Проверка невозможности регистрации курьера без указания логина')
    @allure.description('Проверяем, что не указав логин в теле запроса на регистрацию курьера в ответе вернется код 400 и сообщение {"code": 400, "message": "Недостаточно данных для создания учетной записи"}')
    # попытка зарегистрироваться без логина выдает ошибку
    def test_create_courier_without_login_code400(self, generate_request_body):
        payload = generate_request_body
        payload["login"] = ""
        response = requests.post(URL_COURIER, data=payload)
        assert response.status_code == 400
        assert response.json()['code'] == 400
        assert response.json()['message'] == self.message_400

    @allure.title('Проверка невозможности регистрации курьера без указания пароля')
    @allure.description('Проверяем, что не указав логин в теле запроса на регистрацию курьера в ответе вернется код 400 и сообщение {"code": 400, "message": "Недостаточно данных для создания учетной записи"}')
    # попытка зарегистрироваться без пароля выдает ошибку
    def test_create_courier_without_password_code400(self, generate_request_body):
        payload = generate_request_body
        payload["password"] = ""
        response = requests.post(URL_COURIER, data=payload)
        assert response.status_code == 400
        assert response.json()['code'] == 400
        assert response.json()['message'] == self.message_400

    @allure.title('Проверка невозможности регистрации 2х курьеров c одинаковым логином')
    @allure.description('Проверяем, что запрос на регистрацию курьера с использованием уже зарегистрированного логина вернет код 409 и сообщение {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}')
    # попытка зарегистрировать одного и того же пользователя дважды выдает ошибку
    def test_create_two_couriers_with_same_login_code409(self, generate_request_body):
        payload = generate_request_body
        response_1 = requests.post(URL_COURIER, data=payload)
        assert response_1.status_code == 201
        response_2 = requests.post(URL_COURIER, data=payload)
        assert response_2.status_code == 409
        assert response_2.json()['code'] == 409
        assert response_2.json()['message'] == self.message_409

