import json
import pandas as pd
import pathlib

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

if __name__ == '__main__':
    path = pathlib.Path("data/c25.csv")
    returns = generate_returns(path)

    with open(path.parent / 'monthly-returns.json', "w") as file:
        json.dump(returns, file)
