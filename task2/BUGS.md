# Баги
1. Тест: test_create_item_invalid_sellerID
Заголовок: при некорректном sellerID в /api/1/item создается объявление

payload тела запроса /api/1/item:
```
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
```

2. Тест: test_create_item_not_found
Заголовок: пустом теле запроса /api/1/item создается объявление

payload тела запроса /api/1/item:
```
payload = {}
```