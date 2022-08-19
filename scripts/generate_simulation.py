import sys
import json
import pathlib
import logging
from path_simulation import generate_returns, simulate_path


if __name__ == '__main__':
    logging.basicConfig(stream = sys.stdout, level = logging.INFO)

    path = pathlib.Path("data/c25.csv")
    returns = generate_returns(path)

    periods = 120
    n_paths = 1_000
    interest_rates = returns['values']
    realized_paths = dict(
        (i, simulate_path(interest_rates, periods)) 
        for i in range(n_paths)
    )

    with open(path.parent / 'monthly-returns.json', "w") as file:
        json.dump(returns, file)

    with open(path.parent / f'realized-paths-{periods}.json', "w") as file:
        json.dump(realized_paths, file)

    logging.info(f'{n_paths} paths with {periods} periods simulated from sample distribution')