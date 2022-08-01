import pandas as pd
import json
import pathlib
from pandas.core.common import flatten
from random import sample
from src.compounding import saving_summary

def read_jsonfile(path: pathlib.Path):
    with open(path, "r") as file:
        obj = json.load(file)
    return obj

periods = 120
path = pathlib.Path(f'data/realized-paths-{periods}.json')
realized_paths = read_jsonfile(path)
saving = saving_summary(
    interest_rates=realized_paths['1'], 
    saving=10,
)
df = pd.DataFrame(saving).set_index('time')
