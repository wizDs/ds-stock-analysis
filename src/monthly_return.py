from sympy import symbols, Eq, solve

def get_monthly_return(annual_return: float):
    """
    Based on an annual stock return, this function
    calculates the average monthly return based on
    solving r in the following formula:
        (1+r)^1 + (1+r)^2 +...+ (1+r)^12 = 1 + r
    """
    
    r = symbols('r', positive = True)
    lhs_eq = sum((1 + r) ** i for i in range(1, 12 + 1)) / 12
    rhs_eq = 1 + annual_return
    eq = Eq(lhs_eq, rhs_eq)
    solutions = solve(eq, r, dict=True, quick=True, simplify=False,rational=False)
    
    return solutions[0][r]
