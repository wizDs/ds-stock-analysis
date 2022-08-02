import numpy as np
import pandas as pd
import json
import pathlib
import matplotlib.pyplot as plt
from pandas.core.common import flatten
from random import sample
from compounding import saving_summary, compound

def read_jsonfile(path: pathlib.Path):
    with open(path, "r") as file:
        obj = json.load(file)
    return obj

if __name__=='__main__':
    periods = 120
    saving_rate = 5_000
    path = pathlib.Path(f'data/realized-paths-{periods}.json')
    realized_paths = read_jsonfile(path)
    sampled_returns = list(map(compound, realized_paths.values()))
    mean_returns = np.mean(sampled_returns)
    
    fig, ax = plt.subplots(dpi = 125)
    ax.hist(sampled_returns)

    i=60
    saving = saving_summary(
        interest_rates=realized_paths[str(i)], 
        saving=saving_rate,
    )
    df = pd.DataFrame(saving).set_index('time')
    df

    
    percentiles = [np.quantile(sampled_returns, q) for q in np.arange(0, 1.001, 0.01)]
    fig, ax = plt.subplots(dpi = 125)
    ax.plot(percentiles, range(len(percentiles)))
    ax.set(ylabel = "percentil")
    ax.set(xlabel = f"Opsparing efter {periods // 12} år i millioner dkk")
    ax.set(title  = f"CDF for {periods // 12} års aktieopsparing simuleret på månedlig afkast for c25 (2017-2021)")
    ax.axvline(mean_returns, linestyle = "--", color = "red")
    ax.axvline(periods * saving_rate, linestyle = "--", color = "grey")
    ax.set_xlim(0)
    plt.show()