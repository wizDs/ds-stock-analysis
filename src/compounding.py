import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from itertools import accumulate, starmap
from functools import reduce, partial
from collections.abc import Sequence

@dataclass
class Saving:
    time: int
    total: float
    
def compound_formula(saldo: float, interest: float, saving: float) -> float:
    return (saldo + saving) * (1 + interest)

def compound(interest_rates: list[float], saving: int=5_000, initial_saving: float=0) -> float:
    return reduce(
        partial(compound_formula, saving=saving), 
        interest_rates, 
        initial_saving
    )

def saving_summary(interest_rates: list[float], saving: int=5_000, initial_saving: float=0) -> Sequence[Saving]:
    saving_over_time = accumulate(
        interest_rates, 
        partial(compound_formula, saving=saving), 
        initial=initial_saving
    )
    return starmap(Saving, enumerate(saving_over_time))

if __name__ == '__main__':
    saving_rate = 3000
    savings = saving_summary(np.repeat(0.01, 120), saving=saving_rate)
    savings_df = pd.DataFrame(savings)
    print(savings_df)

    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    ax.plot(savings_df['total'].divide(100000))
    ax.plot(savings_df['time'].multiply(saving_rate).divide(100000))
    ax.set(xlabel = 'Antal år', ylabel = 'Opsparing i hundredtusinder dkk')
    plt.show()