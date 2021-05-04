from Autocall import *
from Underlying import *
from DataManager import *


DM = DataManager()
Index_Name = "STOXX" #"STOXX or STOXX_DEC (Stoxx 50 with decrement)

Index = Underlying(Index_Name, DM)
Maturity = 5
Barrier = 100
Coupon_Barrier = 90
KI_Barrier = 70
Freq = 1 #in numer of times per year
Coupon = 10

myAutocall = Autocall(Index, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon)