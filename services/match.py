import numpy as np
from scipy.spatial.distance import cdist
from sentence_transformers import SentenceTransformer


def create_embeddings(list_name):
    """Функция создает и возвращает векторы текста"""
    model = SentenceTransformer("cointegrated/rubert-tiny2")
    return model.encode(list_name)


async def match(embeddings_factory, market_name, count_var=5):
    """Подсчет расстояний между переданными векторами,
    и возврат {count_var} ближайших, это будут рекомендованные варианты
    получает список векторов производителя, список [product_key, product_name] маркетов, число нужных вариантов
    позвращает индексы переданных векторов производителя"""
    if not (0 < count_var < 51):
        count_var = 5
    embeddings_market = create_embeddings(market_name)
    list_index = []
    for emb in embeddings_market:
        distances = cdist(
            np.expand_dims(emb, axis=0), embeddings_factory, metric="euclidean"
        )
        index_vec_product = np.argsort(distances)[:, :count_var].tolist()
        list_index += index_vec_product
    return list_index[0]
