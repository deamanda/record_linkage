import numpy as np
import pandas as pd
import re

from transliterate import translit
from scipy.spatial.distance import cdist
from sentence_transformers import SentenceTransformer


def del_sub_str(string, sub_str):  # заменяем подстроки на пробел
    for i in sub_str:
        string = string.replace(i, " ")
    return string


def norm_name(string: str) -> (str, str):
    """
    Функция нормализации названий и ПОЛУЧЕНИЯ ОБЪЕМА из названия
    Форматирует строку по заданным правилам.
    Подготовка для расчета векторов.
    :param: (str) Строка которую нужно нормализовать
    :return: (str), (str) Отформатированная строка, Строка содержащая объем продукта из названия
    """
    stop_words = ["и", "для", "из", "с", "c", "в", "ф", "п", "д"]
    t = {
        "0.5": "500 ",
        "0.8": "800 ",
        "0.4": "400 ",
        "0.6": "600 ",
        "0.25": "250 ",
        "0.75": "750 ",
        "0.90": "900",
        "0.9": "900 ",
        "0.2": "200 ",
        "0.1": "100 ",
        "0.05": "50 ",
    }
    string = string.lower()
    string = re.sub(
        r"(\d),(\d)", r"\1.\2", string
    )  # заменяем , на . в десятичных числах
    string = re.sub(
        r"(\d+)([лмлкг])", r"\1 \2", string
    )  # отодвигаем л, мл, кг от цифр, если написано слитно
    string = del_sub_str(string, ",-:\"+«»()/'")  # удаляем все символы
    string = del_sub_str(
        string, ["prosept", "просепт"]
    )  # удаляем название производителя
    string = re.sub(r"\bлитр[о]?в?\b", " л", string)  # заменяем литры на л
    string = string.rstrip(".")
    string = " ".join(
        [word.strip() for word in string.split() if word not in stop_words]
    )  # удаляем стоп слова
    template = re.compile(r"([A-Za-z]+)")
    english = [
        s.strip() for s in template.findall(string) if s.strip()
    ]  # ищем английский текст
    for eng in english:  # удаляем английский текст
        string = string.replace(eng, " ")
    for num, num1 in t.items():  # заменяем десятичные дроби на целые значения
        if num in string:
            string = string.replace(num, num1)
            string = string.replace(" л", " мл")
            string = string.replace(" кг", " г")
    string = (
        translit(" ".join(english), "ru") + " " + string
    )  # добавляем в начало строки английский текст транслитом
    string = " ".join(
        [word.strip() for word in string.split() if word.strip()]
    )  # удаляем лишние пробелы
    size = re.findall(r"(\d+\.\d+|\d+)\s*(?:л|г|кг|мл)\b", string) + [
        "0"
    ]  # находим объем в названии
    return string, size[0]


def df_correct(df: pd.DataFrame, name_col: str) -> pd.DataFrame:
    """
    Проверяем датасет, заполняем/удаляем пропуски.
    :param df: Датасет для корректировки, Имя столбца по которому удаляем пропуски
    :return: Датасет без пропусков в нужном столбце
    """
    df.dropna(subset=name_col, inplace=True)
    if name_col == "name":
        df["name_1c"] = df["name_1c"].fillna(df["name"])
    return df


def create_embeddings(list_name):
    """
    Функция получает на вход обученную модель и список названий.
    Возвращает список векторов, расчитанных по названиям.
    :param model: Модель ML
    :param list_name: Список названий товаров
    :return: Список векторов (числового представления названия)
    """
    model = SentenceTransformer("valentaine98/prosept_ser")
    return model.encode(list_name).tolist()


async def match(embeddings_factory, list_emb_market, count_var=0):
    """
    Функция матчинга сопоставляет векторы из 2-х списков.
    Подсчитывает расстояние между векторами и возвращает
    id {count_var} ближайших из списка производителя.
    :param embeddings_factory: list [id: int, size: str, vector: list[float * 312]] Список id, объема и ВЕКТОРОВ названий производителя
    :param list_emb_market: list [size: str, vector: list[float * 312]] Список объемов и ВЕКТОРОВ названий маркетов
    :param count_var: int Число вариантов, которое необходимо вернуть. 0 - вернуть все предсказания.
    :return: list[id: list[int * count_var]] Список предсказаний для каждого элемента list_name_market
    """
    if not (0 < count_var < 51):
        count_var = None
    predict = []

    emb = list(list_emb_market[0])
    size = str(list_emb_market[1])

    emp_temp_id = embeddings_factory[embeddings_factory[:, 1] == size, 0]
    emp_temp_vector = embeddings_factory[embeddings_factory[:, 1] == size, 2]

    if not len(emp_temp_vector):
        emp_temp_id = embeddings_factory[:, 0]
        emp_temp_vector = embeddings_factory[:, 2]

    distances = cdist(
        np.expand_dims(emb, axis=0), list(emp_temp_vector), metric="euclidean"
    )
    index_predict = np.argsort(distances)[:, :count_var].tolist()
    predict.append([emp_temp_id[i] for i in index_predict[0]])
    return predict
