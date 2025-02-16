import jsonschema
import pytest
from client import APIClient

# Схема успешного ответа (возвращается массив объектов)
create_item_success_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string"}
    },
    "required": ["status"]
}

# Схема для ответов с ошибкой (Not found, Server Error)
bad_request_schema = {
    "type": "object",
    "properties": {
        "result": {
            "type": "object",
            "properties": {
                "messages": {
                    "type": "object",
                    "properties": {
                        "nostrudffb": {"type": "string"},
                        "Ut__": {"type": "string"}
                    },
                    "required": ["nostrudffb", "Ut__"]
                },
                "message": {"type": "string"}
            },
            "required": ["messages", "message"]
        },
        "status": {"type": "string"}
    },
    "required": ["result", "status"]
}


@pytest.fixture
def client(base_url):
    return APIClient(base_url)


def test_create_item_success(client):
    payload = {
        "sellerID": 123456,  # корректное значение: 6 цифр
        "name": "dsds",
        "price": 1,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }
    response = client.create_item(payload)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    # Валидация структуры ответа
    jsonschema.validate(instance=data, schema=create_item_success_schema)


def test_create_item_invalid_sellerID(client):
    """
    Отправляем запрос с некорректным sellerID (например, 5 цифр вместо 6).
    Ожидаем, что API вернёт ошибку (например, статус 400).
    """
    payload = {
        "sellerID": 12345,  # некорректное значение: 5 цифр
        "name": "dsds",
        "price": 1,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }
    response = client.create_item(payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=bad_request_schema)



def test_create_item_not_found(client):
    # Пример эмуляции ошибки Not Found (например, при отсутствии обязательных данных)
    payload = {}  # пустой payload для эмуляции ошибки
    response = client.create_item(payload)
    # Ожидаем статус 404
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=bad_request_schema)


def test_create_item_bad_request(client):
    """
    Отправляем запрос с некорректным sellerID (например, 5 цифр вместо 6)
    и проверяем, что API возвращает Bad Request с ожидаемой структурой ответа.
    """
    payload = {
        "sellerID": 12345,  # некорректное значение: 5 цифр
        "name": "dsds",
        "price": 1,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }
