import os

import pandas as pd
import pytest
from bakery.backend.database import engine
from surprise import Dataset, KNNBasic, Reader, dump


def train():

    df = pd.read_sql("SELECT * FROM ratings", engine)
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df, reader)  # pandas DataFrame
    model = KNNBasic()
    trainset = dataset.build_full_trainset()
    model.fit(trainset)
    file_name = os.path.expanduser("./surprise_model.dump")
    dump.dump(file_name, algo=model)
    return model


def recommend(user, products, model, top_n=3):
    scores = []
    for product in products:
        pred = model.predict(user, product)
        scores.append((product, pred.est))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


@pytest.mark.skip(reason="Run once")
def test_train_recommendation():
    _, loaded_algo = dump.load("./surprise_model.dump")
    r = recommend(2, [1, 2, 3, 4, 5, 6, 7, 8], loaded_algo)
    print(r)
