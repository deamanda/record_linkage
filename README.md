# record_linkage
![prosept_workflow](https://github.com/deamanda/record_linkage/actions/workflows/prosept_workflows.yml/badge.svg?event=push)

# Стек технологий
<div id="badges" align="center">
  <img src="https://img.shields.io/badge/Python%203.11-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/FastAPI%20-white?style=for-the-badge&logo=fastapi&"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
</div>

# Описание проекта

### Регистрация и авторизация.
Пользователь имеет возможность зарегистрироваться и авторизоваться в системе. Получить доступ к своему ЛК,
изменить свои данные.

### Импорт данных.
Есть возможность загрузить данные из файлов с расширением csv. Загрузки данных о дилерах, загрузка продуктов заказчика,
загрузка товаров дилера.

### Главная страница.
На главной странице отображаются товары дилеров. Присутствует возможность фильтрации по статусу сопоставления, 
поиска по названию и сортировки товаров по времени и цене.

### Страница сопоставления.
На странице сопоставления отображаются данные выбранного для сопоставления товара дилера, а также варианты предложенные
ML моделью. Количество выводимых вариантов пользователь настраивает самостоятельно, по умолчанию 5.

### Сопоставленные товары.
Сопоставленные товары записываются в базу данных для дальнейшего использования. И доступны на странице сопоставленных товаров.

### Статистика и аналитика. 
Пользователь имеет возможность просмотреть статистику по сопоставлениям за выбранные период времени. Доступны такие параметры как:
общее количество сопоставлений, количество сопоставлений текущего пользователя, пользователя с конкретным ID, сопоставление
по дилеру с ID. Пользователю так же выводится процент выбираемых позиций.

### Логирование.
Реализована система логирование исключений. На уровне проекта в папке logs сохраняются файлы с логами.

### Версионирование.
В проекте реализовано версионирование API. На данный момент доступна версия v1.

# Установка проекта.

## Установка проекта из репозитория  GitHub.
### Установить Python 3.11
- Для Windows https://www.python.org/downloads/
- Для Linux 
```
sudo apt update
sudo apt -y install python3-pip
sudo apt install python3.11
``` 
### Клонировать репозиторий и перейти в него в командной строке.
```
https://github.com/deamanda/record_linkage.git
``` 
###  Развернуть виртуальное окружение.
```
python -m venv venv

``` 
 - для Windows;
```
venv\Scripts\activate.bat
``` 
 - для Linux и MacOS.
``` 
source venv/bin/activate

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
- В файле .env заполнить данные БД и секрета. Пример заполнения.
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
DB_HOST=db
DB_PORT=5432
SECRET=moi_secret123123123123
``` 
- Запустить main.py

## Установка контейнера Docker
### Склонировать репозиторий
```
https://github.com/deamanda/record_linkage.git
``` 
### Перейти в ветку main
```
git checkout main
``` 
### Перейти в папку infra
```
cd infra
``` 
### В файле .env заполнить данные БД и секрета. Пример заполнения.
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
DB_HOST=db
DB_PORT=5432
SECRET=moi_secret123123123123
``` 
### Запустить сборку образа
```
sudo docker-compose up -d
``` 

---

### Применить миграции
```
docker-compose exec backend alembic upgrade head
``` 
# Документация API первой версии будет доступна по адресу.
```
http://localhost/docs/v1
``` 
