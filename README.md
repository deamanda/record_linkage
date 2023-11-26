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

# Docker
### Склонировать репозиторий
```
https://github.com/deamanda/record_linkage.git
``` 
### Перейти в ветку dev/rash
```
git checkout dev/rash
``` 
### Перейти в папку infra
```
cd infra
``` 
### Запустить сборку образа
```
sudo docker-compose up -d
``` 

### Применить миграции
```
docker-compose exec backend alembic upgrade head
``` 
### Документация по адресу
```
http://localhost/docs/v1
``` 

