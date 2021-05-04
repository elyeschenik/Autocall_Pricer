import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from scipy import optimize


class DataManager:

    def __init__(self):

        # Historical value of underlying asset
        df_underlyings = pd.read_excel("Exam Data.xlsx", index_col=0, sheet_name="Histo underlying")
        STOXX_DEC = df_underlyings.iloc[1:, 0]
        STOXX_DEC.index.name = "Date"
        STOXX = df_underlyings.iloc[1:, 3].dropna()
        STOXX.index.name = "Date"
        self.STOXX = STOXX
        self.STOXX_DEC = STOXX_DEC
        # Implied vol from call put prices
        df_call_put = pd.read_excel("Exam Data.xlsx", index_col=1, sheet_name="Call-Put Price").drop("CALL",
                                                                                                     axis=1).dropna()
        self.df_call = df_call_put.iloc[:9]
        self.df_put = df_call_put.iloc[10:]
