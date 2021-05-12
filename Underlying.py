import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from scipy import optimize


class Underlying:

    def __init__(self, Index_Name, DM):
        self.Index_Name = Index_Name
        self.DM = DM
        self.IV = 0
        if Index_Name == "STOXX":
            self.S_0 = 3956.77
            self.q = 0.029
        elif Index_Name == "STOXX_DEC":
            self.S_0 = 750.77
            self.q = 0.05
        else:
            raise Exception("Wrong index name")


    def Compute_Implied_Vol(self,S_t_1, curr_date, r, K, end_date, isCall):
        #TODO compute the implied vol correctly
        T = (end_date - curr_date).days/365
        if isCall:
            p = self.DM.f_call(K,T)[0] * self.S_0
        else:
            p = self.DM.f_put(K,T)[0] * self.S_0
        a, b = 0.000001, 1
        f = lambda sigma: self.BSClosedForm(S_t_1, K, r, 0.029, sigma, T, isCall) - p
        try:
            out = optimize.brentq(f, a, b)
        except:
            print("aasba")
        self.IV = out
        return out

    def Simulate(self, S_t_1, r, curr_date, end_date, dt):
        #self.Compute_Implied_Vol(S_t_1, curr_date, r, S_t_1, end_date, True)
        #S_t = S_t_1 * np.exp((r - self.q - 0.5 * self.IV ** 2) * dt + self.IV * np.random.normal() * np.sqrt(dt))
        S_t = S_t_1 * np.exp((r - self.q - 0.5 * 0.2 ** 2) * dt + 0.2 * np.random.normal() * np.sqrt(dt))
        return S_t


    @staticmethod
    def BSClosedForm(S_0, K, r, q, sigma, T, isCall):
        d1 = (np.log(S_0/K) + (r - q + 0.5 * sigma**2)*T)/(sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if isCall:
            return S_0 * norm.cdf(d1) * np.exp(-q * T) - np.exp(-r * T) * K * norm.cdf(d2)
        else:
            return -S_0 * norm.cdf(-d1) * np.exp(-q * T) + np.exp(-r * T) * K * norm.cdf(-d2)