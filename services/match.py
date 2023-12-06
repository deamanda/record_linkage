import numpy as np

from scipy.spatial.distance import cdist
from sentence_transformers import SentenceTransformer

from fastapi import HTTPException, status

from core.config import logger


def create_embeddings(list_name):
    """Функция создает и возвращает векторы текста"""
    try:
        logger.info("Creating vectors.")
        model = SentenceTransformer("cointegrated/rubert-tiny2")
    except Exception as e:
        logger.critical(f"Error creating vectors. {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error receiving matched items.",
        )
    return model.encode(list_name)


async def match(embeddings_factory, market_name, count_var=5):
    """Подсчет расстояний между переданными векторами,
    и возврат {count_var} ближайших, это будут рекомендованные варианты
    получает список векторов производителя, список [product_key, product_name] маркетов, число нужных вариантов
    позвращает индексы переданных векторов производителя"""
    try:
        logger.info("Product comparison.")
        data_array = np.array(embeddings_factory)
        if not (0 < count_var < 51):
            count_var = 5
        embeddings_market = create_embeddings(market_name)
        list_index = []
        for emb in embeddings_market:
            distances = cdist(
                np.expand_dims(emb, axis=0), data_array, metric="euclidean"
            )
            index_vec_product = np.argsort(distances)[:, :count_var].tolist()
            list_index += index_vec_product
    except Exception as e:
        logger.critical(f"Error when matching products. {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error receiving matched items.",
        )
    new_list = list_index[0]
    for i in range(len(new_list)):
        new_list[i] += 1
    return new_list
