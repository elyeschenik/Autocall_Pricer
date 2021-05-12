from xlwings import Book, Range
from Autocall import *
from Underlying import *
from DataManager import *
from Curve import *


import os

wb = Book('Exam Data.xlsm')  # Creates a reference to the calling Excel file
sht = wb.sheets['Excel Connect']

os.chdir(wb.fullname[:-15])

def convert_to_bool(txt):
    if txt == "True":
        return True
    elif txt == "False":
        return False

dict_names = {"Eurostoxx 50 Price Index" : "STOXX",
                "Eurostoxx 50 Equal Weight decrement 5% Price Index ( 5% dividend)": "STOXX_DEC"}

Nb_Sim = int(sht.range("C13").value)
DM = DataManager()

Index_Name = dict_names[sht.range("C11").value] #"STOXX" or "STOXX_DEC" (Stoxx 50 with decrement)

discount_curve = Curve(DM)
Index = Underlying(Index_Name, DM)
Maturity = int(sht.range("C3").value)
Barrier = sht.range("C4").value
Coupon_Barrier = sht.range("C5").value
KI_Barrier = sht.range("C6").value
Freq = int(sht.range("C7").value) #in numer of times per year
Coupon = sht.range("C9").value
Snowball = convert_to_bool(sht.range("C8").value)

def Read_Data():
    global Nb_Sim, Index_Name, Index, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon, Snowball
    Nb_Sim = int(sht.range("C13").value)

    Index_Name = dict_names[sht.range("C11").value]  # "STOXX" or "STOXX_DEC" (Stoxx 50 with decrement)

    Index = Underlying(Index_Name, DM)
    Maturity = int(sht.range("C3").value)
    Barrier = sht.range("C4").value
    Coupon_Barrier = sht.range("C5").value
    KI_Barrier = sht.range("C6").value
    Freq = int(sht.range("C7").value)  # in numer of times per year
    Coupon = sht.range("C9").value
    Snowball = convert_to_bool(sht.range("C8").value)


def Compute_Price():
    Read_Data()
    myAutocall = Autocall(Index, discount_curve, Maturity, Barrier, Coupon_Barrier, KI_Barrier, Freq, Coupon, Snowball)
    price = myAutocall.Compute(Nb_Sim)
    sht.range("C15").value = price