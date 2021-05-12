import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from Underlying import *
from datetime import *

class Autocall:
    def __init__(self, Index, Curve, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon, Snowball):
        self.Index = Index
        self.Curve = Curve
        self.Maturity = Maturity
        self.Barrier = Barrier
        self.Coupon_Barrier = Coupon_Barrier
        self.KI_Barrier = KI_Barrier
        self.Freq = Freq
        self.Coupon = Coupon
        self.Snowball = Snowball

        self.start_date = datetime(2021,4,7)
        self.end_date = datetime(self.start_date.year + Maturity,self.start_date.month,self.start_date.day)

        self.Observation_Dates =  [self.start_date + timedelta(days = int(i * 365 / self.Freq)) for i in range(Maturity * self.Freq - 1)] + [self.end_date]


    def Payoff(self):
        """Compute the payoff for one simulation"""
        S_t_1 = self.Index.S_0
        Cumulated_Discounted_CF = 0
        Snowballed_CF = 0
        Flag_PDI = False
        # simu
        for i in range(1, len(self.Observation_Dates)):
            # underlying dynamics
            t = self.Observation_Dates[i]
            t_1 = self.Observation_Dates[i - 1]
            dt = (t - t_1).days/365
            r = self.Curve.get_Forward(t_1,t) #TODO what to put in r
            #TODO div à prendre en compte
            S_t = self.Index.Simulate(S_t_1, r, t, self.end_date, dt)
            # update previous value
            S_t_1 = S_t

            #Coupon barrier crossed
            if S_t >= self.Coupon_Barrier * self.Index.S_0:
                Cumulated_Discounted_CF += self.Coupon * self.Curve.get_DF(t)
            else:
                if self.Snowball:
                    Snowballed_CF += self.Coupon



            #Recall barrier touched
            if S_t >= self.Barrier * self.Index.S_0:
                if self.Snowball:
                    return  Cumulated_Discounted_CF + (1 + Snowballed_CF) * self.Curve.get_DF(t)
                else:
                    return Cumulated_Discounted_CF + self.Curve.get_DF(t)

            #Knock in barrier touched
            if S_t <= self.KI_Barrier * self.Index.S_0 and not Flag_PDI:
                Flag_PDI = True

            if t == self.end_date:
                if  Flag_PDI:
                    return Cumulated_Discounted_CF + (S_t / self.Index.S_0) * self.Curve.get_DF(t)
                else:
                    return Cumulated_Discounted_CF + self.Curve.get_DF(t)


    def Compute(self, Nb_Sim):
        Payoff_List = np.zeros(Nb_Sim)
        for k in range(Nb_Sim):
            Payoff_List[k] = self.Payoff()
        return Payoff_List.mean()

