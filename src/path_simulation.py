import json
import pandas as pd
import pathlib
from pandas.core.common import flatten
from random import sample

def generate_returns(path: pathlib.Path):
    c25 = pd.read_csv(path, sep = ";", encoding="UTF-8", decimal= ",")
    c25.index = pd.to_datetime(c25['Date'])
    returns = c25.resample(rule='1M', label='left')\
        .Closingprice\
        .first()\
        .pct_change()\
        .loc[lambda x: x.notna()]

    return dict(
        date = returns.index.map(str).tolist(),
        values = returns.tolist()
    )

def simulate_path(interest_rates: list[float], periods: int=120) -> list[float]:
    realized_path = (sample(population=interest_rates, k=1) for i in range(periods))
    return list(flatten(realized_path))


if __name__ == '__main__':
    path = pathlib.Path("data/c25.csv")
    returns = generate_returns(path)

    with open(path.parent / 'monthly-returns.json', "w") as file:
        json.dump(returns, file)
