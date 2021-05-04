import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from Underlying import *

class Autocall:
    def __init__(self, Index, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon):
        self.Index = Index
        self.Maturity = Maturity
        self.Barrier = Barrier
        self. Coupon_Barrier = Coupon_Barrier
        self.KI_Barrier = KI_Barrier
        self.Freq = Freq
        self.Coupon = Coupon


    def Compute(self):
        pass

