import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from Underlying import *
from datetime import *

class Autocall:
    def __init__(self, Index, Curve, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon, Snowball, Nb_Sim, type_of_vol = "Historical"):
        self.Index = Index
        self.Curve = Curve
        self.Maturity = Maturity
        self.Barrier = Barrier
        self.Coupon_Barrier = Coupon_Barrier
        self.KI_Barrier = KI_Barrier
        self.Freq = Freq
        self.Coupon = Coupon
        self.Snowball = Snowball

        self.type_of_vol = type_of_vol
        self.Nb_Sim = Nb_Sim

        self.start_date = datetime(2021,4,7)
        self.end_date = datetime(self.start_date.year + Maturity,self.start_date.month,self.start_date.day)

        self.Observation_Dates =  [self.start_date + timedelta(days = int(i * 365 / self.Freq)) for i in range(Maturity * self.Freq - 1)] + [self.end_date]

        self.r_tot = self.Curve.get_Forward(self.start_date,self.end_date)

        self.recall_dates = []


        self.all_dates = []
        for i in range((self.end_date - self.start_date).days):
            tmp_date = self.start_date + timedelta(days = i)
            if tmp_date.weekday() not in [5,6]:
                self.all_dates.append(tmp_date)
        self.all_dates.append(self.end_date)

        S = np.zeros((Nb_Sim , len(self.all_dates)))
        S[:,0] = self.Index.S_0

        U = np.random.normal(size = (Nb_Sim, len(self.all_dates) - 1))
        for i in range(1, len(self.all_dates)):
            # underlying dynamics
            t = self.all_dates[i]
            t_1 = self.all_dates[i - 1]
            dt = (t - t_1).days/252
            r = self.Curve.get_Forward(t_1,t)
            S[:,i] = self.Index.Simulate(S[:,i-1], r, self.end_date, dt, self.type_of_vol, self.r_tot, Nb_Sim, U, i)
        self.S = S






    def Payoff(self, sim):
        """Compute the payoff for one simulation"""
        S_t_1 = self.Index.S_0
        Cumulated_Discounted_CF = 0
        Snowballed_CF = 0
        Flag_PDI = False
        # simu

        for i in range(1, len(self.all_dates)):
            # underlying dynamics
            t = self.all_dates[i]
            S_t = self.S[sim,i]


            # Knock in barrier touched
            if S_t <= self.KI_Barrier * self.Index.S_0 and not Flag_PDI:
                Flag_PDI = True

            if t in self.Observation_Dates:

                #Coupon barrier crossed
                if S_t >= self.Coupon_Barrier * self.Index.S_0:
                    Cumulated_Discounted_CF += self.Coupon * self.Curve.get_DF(t)
                else:
                    if self.Snowball:
                        Snowballed_CF += self.Coupon

                #Recall barrier touched
                if S_t >= self.Barrier * self.Index.S_0:
                    self.recall_dates.append((t - self.start_date).days / 365)
                    if self.Snowball:
                        return  Cumulated_Discounted_CF + (1 + Snowballed_CF) * self.Curve.get_DF(t)
                    else:
                        return Cumulated_Discounted_CF + self.Curve.get_DF(t)

                if t == self.end_date:
                    self.recall_dates.append((t - self.start_date).days / 365)
                    if Flag_PDI:
                        return Cumulated_Discounted_CF + (S_t / self.Index.S_0) * self.Curve.get_DF(t)
                    else:
                        return Cumulated_Discounted_CF + self.Curve.get_DF(t)


    def Compute(self):
        Payoff_List = np.zeros(self.Nb_Sim)
        for sim in range(self.Nb_Sim):
            Payoff_List[sim] = self.Payoff(sim)
        STD = np.std(Payoff_List)
        eps = 1.96 * STD/np.sqrt(self.Nb_Sim)
        return Payoff_List.mean(), eps

    def Expected_Maturity(self):
        return np.mean(self.recall_dates)



