from Autocall import *
from Underlying import *
from DataManager import *
from Curve import *

Nb_Sim = 1000
DM = DataManager()
Index_Name = "STOXX" #"STOXX" or "STOXX_DEC" (Stoxx 50 with decrement)

discount_curve = Curve(DM)
Index = Underlying(Index_Name, DM)
Maturity = 5
Barrier = 1
Coupon_Barrier = 0.9
KI_Barrier = 0.7
Freq = 1 #in numer of times per year
Coupon = 0.05
Snowball = True


myAutocall = Autocall(Index, discount_curve, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon, Snowball, Nb_Sim)
print(myAutocall.Compute())