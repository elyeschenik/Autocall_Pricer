import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from scipy import optimize
from datetime import *


class Underlying:

    def __init__(self, Index_Name, DM):
        self.Index_Name = Index_Name
        self.DM = DM
        self.vol = None
        if Index_Name == "STOXX":
            self.S_0 = 3956.77
            self.q = 0.029
            #self.q = 0
        elif Index_Name == "STOXX_DEC":
            self.S_0 = 750.77
            self.q = 0.05
        else:
            raise Exception("Wrong index name")


    def Compute_Implied_Vol(self,S_t_1, curr_date, r, K, end_date, isCall):
        #TODO compute the implied vol correctly
        T = (end_date - curr_date).days/365
        if isCall:
            p = self.DM.f_call(T,K)[0] * self.S_0
        else:
            p = self.DM.f_put(T,K)[0] * self.S_0
        a, b = 0.000001, 1
        f = lambda sigma: self.BSClosedForm(S_t_1, K, r, 0.029, sigma, T, isCall) - p
        vol = optimize.brentq(f, a, b)
        return vol


    def Get_Implied_Vol(self, r, end_date):
        vol_call = self.Compute_Implied_Vol(3956.77, datetime(2021,4,7), r, 3956.77, end_date, True)
        vol_put = self.Compute_Implied_Vol(3956.77, datetime(2021,4,7), r, 3956.77, end_date, False)
        self.vol = (vol_call + vol_put)/2

    def Compute_Histo_Vol(self):
        if self.Index_Name == "STOXX":
            prices = self.DM.STOXX
        elif self.Index_Name == "STOXX_DEC":
            prices = self.DM.STOXX_DEC
        else:
            raise Exception("Wrong index name")
        returns = prices.pct_change()
        vol = np.sqrt(252) * returns.std()
        self.vol = vol


    def Simulate(self, S_t_1, r, end_date, dt, type_of_vol, r_tot, Nb_Sim = 1, U = None, i=None):
        if self.vol is None:
            if type_of_vol == "Historical":
                self.Compute_Histo_Vol()
            elif type_of_vol == "Implied":
                self.Get_Implied_Vol(r_tot, end_date)
        if U is None:
            S_t = S_t_1 * np.exp((r - self.q - 0.5 * self.vol ** 2) * dt + self.vol * np.random.normal(size = Nb_Sim) * np.sqrt(dt))
        else:
            S_t = S_t_1 * np.exp((r - self.q - 0.5 * self.vol ** 2) * dt + self.vol * U[:,i - 1] * np.sqrt(dt))
        return S_t

    #def Simulate_ND(self, r, end_date, dt, vol_method, r_tot):


    @staticmethod
    def BSClosedForm(S_0, K, r, q, sigma, T, isCall):
        d1 = (np.log(S_0/K) + (r - q + 0.5 * sigma**2)*T)/(sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if isCall:
            return S_0 * norm.cdf(d1) * np.exp(-q * T) - np.exp(-r * T) * K * norm.cdf(d2)
        else:
            return -S_0 * norm.cdf(-d1) * np.exp(-q * T) + np.exp(-r * T) * K * norm.cdf(-d2)