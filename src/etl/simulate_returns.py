import pathlib
import json
from pandas.core.common import flatten
from random import sample

def simulate_path(interest_rates: list[float], periods: int=120) -> list[float]:
    realized_path = (sample(population=interest_rates, k=1) for i in range(periods))
    return list(flatten(realized_path))
