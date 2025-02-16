import pytest

@pytest.fixture(scope='session')
def base_url():
    # Базовый URL для API
    return 'https://qa-internship.avito.com/api/1'