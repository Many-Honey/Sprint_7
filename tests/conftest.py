import pytest
import requests
import random
import string
from urls import *


# фикстура возвращает тело запроса для создания нового курьера и удаляет созданного курьера в конце теста
@pytest.fixture
def generate_request_body_and_delete_courier(generate_request_body):
    payload = generate_request_body
    yield payload
    # формируем тело запроса для входа в систему
    payload_login = {
        "login": payload.get("login"),
        "password": payload.get("password")
    }
    # отправляем запрос на вход в систему
    response_login = requests.post(URL_LOGIN, data=payload_login)
    # получаем значение id
    r = response_login.json()
    courier_id = r.get("id")
    # формируем тело запроса для удаления курьера
    payload_delete = {
        "id": str(courier_id)#f'{id}'
    }
    # удаляем созданного ранее курьера
    requests.delete(f'{URL_COURIER}/{courier_id}', data=payload_delete)




# фикстура регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
@pytest.fixture
def register_new_courier_return_login_password_delete_courier(generate_request_body):
    # создаём список, чтобы метод мог его вернуть
    login_pass = []
    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(URL_COURIER, data=generate_request_body)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(generate_request_body["login"])
        login_pass.append(generate_request_body["password"])
        login_pass.append(generate_request_body["firstName"])

    # возвращаем список
    yield login_pass

    # формируем тело запроса для входа в систему
    payload_login = {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    # отправляем запрос на вход в систему
    response_login = requests.post(URL_LOGIN, data=payload_login)
    # получаем значение id
    r = response_login.json()
    courier_id = r.get("id")
    # формируем тело запроса для удаления курьера
    payload_delete = {
        "id": str(courier_id)  # f'{id}'
    }
    # удаляем созданного ранее курьера
    requests.delete(f'{URL_COURIER}/{courier_id}', data=payload_delete)


# фикстура возвращает тело запроса для создания нового курьера
@pytest.fixture
def generate_request_body():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    # возвращаем тело запроса
    return payload


