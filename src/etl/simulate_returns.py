import pathlib
import json
from pandas.core.common import flatten
from random import sample

def read_jsonfile(path: pathlib.Path):
    with open(path, "r") as file:
        obj = json.load(file)
    return obj

def simulate_path(interest_rates: list[float], periods: int=120) -> list[float]:
    realized_path = (sample(population=interest_rates, k=1) for i in range(periods))
    return list(flatten(realized_path))

if __name__ == '__main__':
    periods = 120
    n_paths = 1_000
    path = pathlib.Path('data/monthly-returns.json')
    returns = read_jsonfile(path)
    interest_rates = returns['values']
    realized_paths = dict(
        (i, simulate_path(interest_rates, periods)) 
        for i in range(n_paths)
    )

    with open(path.parent / f'realized-paths-{periods}.json', "w") as file:
        json.dump(realized_paths, file)
