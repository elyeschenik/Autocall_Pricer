from datetime import *
import numpy as np

class Curve:
    def __init__(self, DM):
        self.DM = DM

    def get_Spread(self, date):
        if date in self.DM.spread_curve.index:
            rate = self.DM.spread_curve.loc[date].values[0]
        else:
            d_bottom = self.DM.spread_curve.loc[self.DM.spread_curve.index < date].index[-1]
            d_up = self.DM.spread_curve.loc[self.DM.spread_curve.index > date].index[0]

            self.DM.spread_curve.loc[date] = None
            rate = self.DM.spread_curve.sort_index().loc[[d_bottom, date, d_up]].interpolate(method='time').loc[date].values[0]
            self.DM.spread_curve.drop(date, axis=0, inplace=True)
        return rate

    def get_Rate(self, date):
        if date in self.DM.curve.index:
            rate = self.DM.curve.loc[date].values[0]
        else:
            d_bottom = self.DM.curve.loc[self.DM.curve.index < date].index[-1]
            d_up = self.DM.curve.loc[self.DM.curve.index > date].index[0]

            self.DM.curve.loc[date] = None
            rate = self.DM.curve.sort_index().loc[[d_bottom, date, d_up]].interpolate(method='time').loc[date].values[0]
            self.DM.curve.drop(date, axis=0, inplace=True)
        return rate

    def get_DF(self, date, addSpread = True):
        rate = self.get_Rate(date)
        if addSpread:
            rate = rate + self.get_Spread(date)
        delta = (date - datetime(2021,4,7)).days/365
        DF = np.exp(-rate * delta)
        return DF

    def get_Forward(self, date_1, date_2):
        delta = (date_1 - date_2).days/365
        B_1 = self.get_DF(date_1, addSpread=False)
        B_2 = self.get_DF(date_2, addSpread=False)
        return (1/delta) * ((B_1/B_2) - 1)


