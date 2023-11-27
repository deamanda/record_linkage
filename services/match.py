from io import StringIO

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sentence_transformers import SentenceTransformer


def get_embeddings(names: list):
    model = SentenceTransformer("cointegrated/rubert-tiny2")
    return model.encode(names)


async def create_embeddings_factory(file):
    content = await file.read()
    df_factory = pd.read_csv(StringIO(content.decode()), delimiter=";")
    df_factory_name = df_factory[["id", "name"]]
    embeddings_factory = get_embeddings(list(df_factory_name["name"]))
    df_factory_name["embeddings_factory"] = embeddings_factory.tolist()

    return embeddings_factory, df_factory_name


async def match(market_prod_names: list, count_var: int, file):
    if not (0 < count_var < 26):
        count_var = 5
    embeddings_market = get_embeddings(market_prod_names)
    embeddings_product, df_factory_name = await create_embeddings_factory(file)

    result = []
    for emb in embeddings_market:
        distances = cdist(
            np.expand_dims(emb, axis=0), embeddings_product, metric="euclidean"
        )
        index_product = np.argsort(distances)[:, :count_var].tolist()
        result.append(df_factory_name.loc[index_product[0], "id"].tolist())
    return result
