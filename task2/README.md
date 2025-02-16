# Автотесты API Avito Internship

Данный проект содержит автотесты для проверки API Avito Internship, реализованные с использованием Python и pytest. Тесты покрывают следующие ручки:

1. **Создание объявления (`create_item`)**  
   Создает объявление и возвращает строку в формате:
   ```json
   {"status": "Сохранили объявление - <item_id>"}

2. Получение объявления по ID (get_item_by_id)
Получает объявление по идентификатору, возвращая массив объектов, например:
```json
[
  {
    "createdAt": "2025-02-16 19:40:54.885704 +0300 +0300",
    "id": "36ae21cf-695c-4727-9303-342ded54cb56",
    "name": "dsdsd",
    "price": 10,
    "sellerId": 213152,
    "statistics": {
      "contacts": 2,
      "likes": 5,
      "viewCount": 20
    }
  }
]
```
3. Получение статистики по объявлениям (get_statistics)

4. Получение объявлений по sellerID (get_items_by_seller)

# Требования
```
Python 3.7+
pip
```
# Установка
1. Клонируйте репозиторий:
```
git clone https://github.com/your_username/my_api_tests.git
cd my_api_tests
```
2. Установите зависимости:
```
pip install -r requirements.txt
```

# Запуск тестов
Для запуска автотестов выполните из корневой директории проекта команду:
```
pytest
```
Pytest автоматически обнаружит все тестовые файлы (начинающиеся с test_) и выполнит тесты.

# Настройка
Базовый URL API:
В файле conftest.py указан базовый URL:
```
@pytest.fixture(scope='session')
def base_url():
    return 'https://qa-internship.avito.com/api/1'
```
