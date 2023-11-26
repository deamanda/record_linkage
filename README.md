# record_linkage

## Стек технологий
- Python 3.11
- FastAPI
- PostgreSQL
- Docker

## Установка проекта из репозитория
### Клонировать репозиторий и перейти в него в командной строке:

## Запуск проекта(dev)
### Установить Python 3.11
- Для Windows https://www.python.org/downloads/
- Для Linux 
```
sudo apt update
sudo apt -y install python3-pip
sudo apt install python3.11
``` 
### Установить систему контроля зависимостей Poetry
```
pip install poetry
``` 
### Установить зависимости
```
poetry install
``` 
### Установка .pre-commit hook
```
pre-commit install
``` 
### Команды для создания миграций
```
alembic revision --autogenerate -m "Migration name"
``` 
### Команды для применения миграций
```
alembic upgrade head
```
### Запуск проекта
- В файле config прописать путь до бд в формате 'postgresql+asyncpg://user:password@host:port/name' c указанием своих user, name, host, port, password 
- Запустить main.py

### Документация по адресу
```
http://127.0.0.1:8000/docs/v1
``` 