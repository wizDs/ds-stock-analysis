import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
from random import sample
from datetime import datetime
from math import ceil
from sympy import symbols, Eq, solve

class Config:
    monthly_saving = 5000 / 1000000
    years = 15
    

# =============================================================================
# teoretisk
# =============================================================================
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


fig, ax = plt.subplots(dpi = 125)
plt.style.use('seaborn-whitegrid')
monthly_return = get_monthly_return(annual_return = 0.074)
savings_df = get_savings_data(monthly_return, Config.monthly_saving, Config.years)
mean_returns    = savings_df.savings_compounded.iloc[-1]
ax.plot(savings_df['savings_compounded'])
ax.plot(savings_df['savings'])
ax.set(xlabel = 'Antal år', ylabel = 'Opsparing i millioner dkk')

# =============================================================================
# praktisk med usikkerhed
# =============================================================================
c25 = pd.read_csv("data/c25.csv", sep = ";", encoding="UTF-8", decimal= ",")
c25["Date"]  = pd.to_datetime(c25.Date)
c25["Day"]   = c25["Date"].dt.day
c25["Month"] = c25["Date"].dt.month
c25["Year"]  = c25["Date"].dt.year

first_day_in_month  = c25.groupby(["Year", "Month"]).Day.min().reset_index()
c25_monthly         = c25.merge(first_day_in_month, on = ["Year", "Month", "Day"])
c25_monthly.set_index("Date", inplace = True)
c25_monthly.sort_index(ascending = True, inplace = True)

prices = c25_monthly['Closingprice']

returns = prices.pct_change()
returns = returns[returns.notna()]
returns_dict = returns.to_dict()


return_binned_pct = pd.cut(returns.multiply(100), bins = [ -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])
fig, ax = plt.subplots(dpi = 125)
sns.countplot(x = return_binned_pct, ax = ax, color = "blue")
plt.xticks(rotation=55)

class StochasticCompounding:
    
    def __init__(self):
        self.time = list()
        self.stock_return = list()
        self.total_savings = list()
        self.sampled_date = list()
        
    def add_point(self, time: int, stock_return: float, total_savings: float, sampled_date: datetime):
        self.time.append(time)
        self.stock_return.append(stock_return)
        self.total_savings.append(total_savings)
        self.sampled_date.append(sampled_date)
        self.cum_savings = total_savings
        
    def to_frame(self):
        df = pd.DataFrame({
                "time" :        self.time,
                "stock_return": self.stock_return,
                'total_savings':self.total_savings,
                "sampled_date": self.sampled_date,
        })
        
        return df.set_index("time")
    
    def annual_returns(self):
        df = self.to_frame()
        df["stock_return"]  = df.stock_return.add(1)
        df["year"]          = (df.index / 12).map(ceil)
        returns_year        = df.groupby("year").agg({"stock_return":list})
        returns_year        = [sum(np.prod(lst[i:]) for i in range(len(lst))) / 12 - 1 for lst in returns_year.stock_return]
        
        return returns_year
    
    def annual_savings(self):
        df = self.to_frame()
        savings_year = df[df.index % 12 == 0]
        savings_year.index = savings_year.index // 12
        
        return savings_year.total_savings
        
    
  
    
def monthly_compounding_stoc(monthly_return_sample_space: Dict[datetime, float], monthly_saving: int, years: int):
    months          = years * 12
    total_savings   = 0
    stoc_compounding= StochasticCompounding()
    
    for i in range(1, months + 1):
        sampled_date = sample(monthly_return_sample_space.keys(), 1)[0]
        monthly_return = monthly_return_sample_space[sampled_date]
        total_savings  = (total_savings + monthly_saving) * (1 + monthly_return)
        
        stoc_compounding.add_point(i, monthly_return, total_savings, sampled_date)
        
    return stoc_compounding
        

def get_savings_data_stoc(monthly_return_sample_space: Dict[datetime, float], monthly_saving: int, years: int):
    range_years = range(1, years + 1)
    sc = monthly_compounding_stoc(monthly_return_sample_space, monthly_saving, years)
        
    savings_data  = pd.DataFrame({
         'years':                range_years, 
         'savings':              np.cumsum(np.repeat(monthly_saving * 12, years)), 
         'savings_compounded':   sc.annual_savings(), 
         'annual_returns':       sc.annual_returns()
    })
    
    return savings_data.set_index("years")




sampled_paths   = [monthly_compounding_stoc(returns_dict, Config.monthly_saving, Config.years) for i in range(1000)]

max_y = ceil(max(path.cum_savings for path in sampled_paths[:20])) + 1

fig, ax = plt.subplots(dpi = 150)
for path in sampled_paths[:10]:
    ax.plot(path.annual_savings())
ax.set_ylim(0,max_y)
    

fig, ax = plt.subplots(dpi = 150)
for path in sampled_paths[:20]:
    ax.plot(path.annual_savings())
ax.set_ylim(0,max_y)


sampled_returns = [path.cum_savings for path in sampled_paths]
fig, ax = plt.subplots(dpi = 125)
ax.hist(sampled_returns)

percentiles = [np.quantile(sampled_returns, q) for q in np.arange(0, 1.001, 0.01)]
fig, ax = plt.subplots(dpi = 125)
ax.plot(percentiles, range(len(percentiles)))
ax.set(ylabel = "percentil")
ax.set(xlabel = f"Opsparing efter {Config.years} år i millioner dkk")
ax.set(title  = f"CDF for {Config.years} års aktieopsparing simuleret på månedlig afkast for c25 (2017-2021)")
ax.axvline(mean_returns, linestyle = "--", color = "red")
ax.axvline(Config.years * 12 * Config.monthly_saving, linestyle = "--", color = "grey")


df = get_savings_data_stoc(returns_dict, Config.monthly_saving, Config.years)
print(df)
df.annual_returns.mean()