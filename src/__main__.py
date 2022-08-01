import pandas as pd
import json
import pathlib
import matplotlib.pyplot as plt
from pandas.core.common import flatten
from random import sample
from src.compounding import saving_summary, compound

def read_jsonfile(path: pathlib.Path):
    with open(path, "r") as file:
        obj = json.load(file)
    return obj


if __name__=='__main__':
    periods = 120
    path = pathlib.Path(f'data/realized-paths-{periods}.json')
    realized_paths = read_jsonfile(path)
    sampled_returns = list(map(compound, realized_paths.values()))
    
    fig, ax = plt.subplots(dpi = 125)
    ax.hist(sampled_returns)
    plt.show()

    i=60
    saving = saving_summary(
        interest_rates=realized_paths[str(i)], 
        saving=0.005,
    )
    df = pd.DataFrame(saving).set_index('time')
    df