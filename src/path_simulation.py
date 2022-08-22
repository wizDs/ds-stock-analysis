import json
import pandas as pd
import pathlib
from pandas.core.common import flatten
from random import sample
from typing import Dict
from pydantic import BaseModel
from datetime import datetime

class StockPrice(BaseModel):
    time: datetime
    value: float

class StockReturn(BaseModel):
    time: datetime
    value: float

def generate_returns(path: pathlib.Path) -> Dict[str, int]:
    """
    Empirical stock prices is transformed into 
    pct. stock returns for c25 data
    """
    c25 = pd.read_csv(path, sep = ";", encoding="UTF-8", decimal= ",")
    c25['Date'] = pd.to_datetime(c25['Date']).dt.to_pydatetime()
    c25_price = [StockPrice(time=t, value=v) for t, v in c25[['Date', 'Closingprice']].values]
    c25_returns = stock_price_to_pct_return(c25_price)
    return dict(
        date = [x.time.strftime("%Y-%m-%d") for x in c25_returns],
        values = [x.value for x in c25_returns],
    )

def stock_price_to_pct_return(prices: list[StockPrice]) -> list[StockReturn]:
    """
    Empirical stock prices is transformed into 
    pct. stock returns.
    """
    prices_df = pd.DataFrame(p.dict() for p in prices)
    returns = prices_df.resample(rule='1M', label='left', on='time')\
        ['value']\
        .first()\
        .pct_change()\
        .loc[lambda x: x.notna()]

    return [StockReturn(time=t, value=v) for t, v in returns.iteritems()]

def simulate_path(interest_rates: list[float], periods: int=120) -> list[float]:
    """
    Given a distribution of empirical pct. stock returns, 
    simulate a path of pct. stock returns with an arbitrary 
    length.
    """
    realized_path = (sample(population=interest_rates, k=1) for i in range(periods))
    return list(flatten(realized_path))


if __name__ == '__main__':
    path = pathlib.Path("data/c25.csv")
    returns = generate_returns(path)

    with open(path.parent / 'monthly-returns.json', "w") as file:
        json.dump(returns, file, default=str)
