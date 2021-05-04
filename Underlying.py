import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from scipy import optimize


class Underlying:

    def __init__(self, Index_Name, DM):
        self.Index_Name = Index_Name
        self.DM = DM
        self.IV = False

    def Get_Implied_Vol(self):
        return self.IV

    def Compute_Implied_Vol(self,S_0, curr_date, r, K, end_date, isCall):
        T = (end_date - curr_date).days/252
        if isCall:
            p = self.DM.df_call.loc[K,end_date] * S_0
        else:
            p = self.DM.df_put.loc[K,end_date] * S_0
        a, b = 0.000001, 1
        f = lambda x: abs(self.BSClosedForm(S_0, K, r, x, T, isCall) - p)
        sol = optimize.brentq(f, a, b)
        self.IV = sol
        return sol


    @staticmethod
    def BSClosedForm(S_0, K, r, sigma, T, isCall):
        d1 = (np.log(S_0/K) + (r + 0.5 * sigma**2)*T)/(sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if isCall:
            return S_0 * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
        else:
            return -S_0 * norm.cdf(-d1) + np.exp(-r * T) * K * norm.cdf(-d2)