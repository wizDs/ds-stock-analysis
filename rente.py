import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import symbols, Eq, solve

def monthly_compounding(monthly_return: float, monthly_saving: int, years: int):
    months              = years * 12    
    range_months        = range(1, months + 1)
    compounded_savings  = map(lambda i: monthly_saving * (1 + monthly_return) ** i, range_months)
        
    return sum(compounded_savings)
        

def get_monthly_return(annual_return: float):
    
    r = symbols('r', positive = True)
    lhs_eq = sum((1 + r) ** i for i in range(1, 12 + 1)) / 12
    rhs_eq = 1 + annual_return
    eq = Eq(lhs_eq, rhs_eq)
    solutions = solve(eq, r, dict=True, quick=True, simplify=False,rational=False)
    
    return solutions[0][r]


def get_savings_data(monthly_return: float, monthly_saving: int, years: int):
    range_years = range(1, years + 1)
    
    savings_data = pd.DataFrame({
        'years':              range_years, 
        'savings':            np.cumsum(np.repeat(monthly_saving * 12, years)), 
        'savings_compounded': [monthly_compounding(monthly_return, monthly_saving, t) for t in range_years]
    })
    
    return savings_data.set_index("years")


fig, ax = plt.subplots()
plt.style.use('seaborn-whitegrid')
monthly_return = get_monthly_return(annual_return = 0.074)
savings_df = get_savings_data(monthly_return, 5000, 10)
print(savings_df.savings_compounded.iloc[-1])
ax.plot(savings_df['savings_compounded'].divide(100000))
ax.plot(savings_df['savings'].divide(100000))
ax.set(xlabel = 'Antal år', ylabel = 'Opsparing i hundredtusinder dkk')