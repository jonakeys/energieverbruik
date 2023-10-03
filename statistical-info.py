import pandas as pd
from numpy import *
df = pd.read_csv('energie-stats.csv')

gasHdg = df['g']
gasVrgJr = df['g-1']
gasVrgJr2 = df['g-2']

eleHdg = df['e']
eleVrgJr = df['e-1']
eleVrgJr2 = df['e-2']

watHdg = df['w']
watVrgJr = df['w-1']
watVrgJr2 = df['w-2']

gasHdgStd = round(std(gasHdg), 1)
gasVrgJrStd = round(std(gasVrgJr), 1)
gasVrgJr2Std = round(std(gasVrgJr2), 1)
gasHdgGem = round(gasHdg.mean(), 1)
gasVrgJrGem = round(gasVrgJr.mean(), 1)
gasVrgJr2Gem = round(gasVrgJr2.mean(), 1)
gasHdgMed = round(gasHdg.median(), 1)
gasVrgJrMed = round(gasVrgJr.median(), 1)
gasVrgJr2Med = round(gasVrgJr2.median(), 1)

eleVrgJrStd = round(std(eleVrgJr), 1)
eleHdgStd = round(std(eleHdg), 1)
eleVrgJr2Std = round(std(eleVrgJr2), 1)
eleHdgGem = round(eleHdg.mean(), 1)
eleVrgJrGem = round(eleVrgJr.mean(), 1)
eleVrgJr2Gem = round(eleVrgJr2.mean(), 1)
eleHdgMed = round(eleHdg.median(), 1)
eleVrgJrMed = round(eleVrgJr.median(), 1)
eleVrgJr2Med = round(eleVrgJr2.median(), 1)

watHdgStd = round(std(watHdg), 1)
watVrgJrStd = round(std(watVrgJr), 1)
watVrgJr2Std = round(std(watVrgJr2), 1)
watHdgGem = round(watHdg.mean(), 1)
watVrgJrGem = round(watVrgJr.mean(), 1)
watVrgJr2Gem = round(watVrgJr2.mean(), 1)
watHdgMed = round(watHdg.median(), 1)
watVrgJrMed = round(watVrgJr.median(), 1)
watVrgJr2Med = round(watVrgJr2.median(), 1)

def toonData(soort, dat1, dat2, dat3):
    print("\t", soort, "\t",
          dat1, " (", round(dat1-dat2, 1), ")\t",
          dat2, " (", round(dat2-dat3, 1), ")\t",
          dat3)

def printJaren():
    print("\t\t\t2023\t\t2022\t\t2021")

#printJaren()
print("Gas")
toonData("StdDev", gasHdgStd, gasVrgJrStd, gasVrgJr2Std)
toonData("Gem\t", gasHdgGem, gasVrgJrGem, gasVrgJr2Gem)
toonData("Med\t", gasHdgMed, gasVrgJrMed, gasVrgJr2Med)
print("\nEle")
toonData("StdDev", eleHdgStd, eleVrgJrStd, eleVrgJr2Std)
toonData("Gem\t", eleHdgGem, eleVrgJrGem, eleVrgJr2Gem)
toonData("Med\t", eleHdgMed, eleVrgJrMed, eleVrgJr2Med)
print("\nWat")
toonData("StdDev", watHdgStd, watVrgJrStd, watVrgJr2Std)
toonData("Gem\t", watHdgGem, watVrgJrGem, watVrgJr2Gem)
toonData("Med\t", watHdgMed, watVrgJrMed, watVrgJr2Med)
   
