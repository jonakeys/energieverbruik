import pandas as pd
from numpy import *
df = pd.read_csv('energie-stats.csv')

gasDitJaar = df['g']
gasDitJaarMin1 = df['g-1']
gasDitJaarMin2 = df['g-2']

eleDitJaar = df['e']
eleDitJaarMin1 = df['e-1']
eleDitJaarMin2 = df['e-2']

watDitJaar = df['w']
watDitJaarMin1 = df['w-1']
watDitJaarMin2 = df['w-2']

gasDitJaarStd = round(std(gasDitJaar), 1)
gasDitJaarMin1Std = round(std(gasDitJaarMin1), 1)
gasDitJaarMin2Std = round(std(gasDitJaarMin2), 1)
gasDitJaarGem = round(gasDitJaar.mean(), 1)
gasDitJaarMin1Gem = round(gasDitJaarMin1.mean(), 1)
gasDitJaarMin2Gem = round(gasDitJaarMin2.mean(), 1)
gasDitJaarMed = round(gasDitJaar.median(), 1)
gasDitJaarMin1Med = round(gasDitJaarMin1.median(), 1)
gasDitJaarMin2Med = round(gasDitJaarMin2.median(), 1)

eleDitJaarStd = round(std(eleDitJaar), 1)
eleDitJaarMin1Std = round(std(eleDitJaarMin1), 1)
eleDitJaarMin2Std = round(std(eleDitJaarMin2), 1)
eleDitJaarGem = round(eleDitJaar.mean(), 1)
eleDitJaarMin1Gem = round(eleDitJaarMin1.mean(), 1)
eleDitJaarMin2Gem = round(eleDitJaarMin2.mean(), 1)
eleDitJaarMed = round(eleDitJaar.median(), 1)
eleDitJaarMin1Med = round(eleDitJaarMin1.median(), 1)
eleDitJaarMin2Med = round(eleDitJaarMin2.median(), 1)

watDitJaarStd = round(std(watDitJaar), 1)
watDitJaarMin1Std = round(std(watDitJaarMin1), 1)
watDitJaarMin2Std = round(std(watDitJaarMin2), 1)
watDitJaarGem = round(watDitJaar.mean(), 1)
watDitJaarMin1Gem = round(watDitJaarMin1.mean(), 1)
watDitJaarMin2Gem = round(watDitJaarMin2.mean(), 1)
watDitJaarMed = round(watDitJaar.median(), 1)
watDitJaarMin1Med = round(watDitJaarMin1.median(), 1)
watDitJaarMin2Med = round(watDitJaarMin2.median(), 1)

def toon(jrStd, jrmin1Std, jrmin2Std, jrGem, jrmin1Gem, jrmin2Gem,
         jrMed, jrmin1Med, jrmin2Med):
    print("\t   2024\t", jrStd, " (", round(jrStd-jrmin2Std, 1), ")\t",
          jrGem, " (", round(jrGem-jrmin2Gem, 1), ")\t",
          jrMed, " (", round(jrMed-jrmin2Med, 1), ")", sep="")
    print("\t   2023\t", jrmin1Std, " (", round(jrmin1Std-jrmin2Std, 1), ")\t",
          jrmin1Gem, " (", round(jrmin1Gem-jrmin2Gem, 1), ")\t",
          jrmin1Med, " (", round(jrmin1Med-jrmin2Med, 1), ")", sep="")
    print("\t<= 2022\t", jrmin2Std, "\t\t", jrmin2Gem, "\t\t", jrmin2Med, sep="")

print("GAS (m3)\tStdDev\t\tAvg\t\tMed")
toon(gasDitJaarStd, gasDitJaarMin1Std, gasDitJaarMin2Std,
     gasDitJaarGem, gasDitJaarMin1Gem, gasDitJaarMin2Gem,
     gasDitJaarMed, gasDitJaarMin1Med, gasDitJaarMin2Med)
print("ELEKTRICITEIT (kWh)")
toon(eleDitJaarStd, eleDitJaarMin1Std, eleDitJaarMin2Std,
     eleDitJaarGem, eleDitJaarMin1Gem, eleDitJaarMin2Gem,
     eleDitJaarMed, eleDitJaarMin1Med, eleDitJaarMin2Med)
print("WATER (m3)")
toon(watDitJaarStd, watDitJaarMin1Std, watDitJaarMin2Std,
     watDitJaarGem, watDitJaarMin1Gem, watDitJaarMin2Gem,
     watDitJaarMed, watDitJaarMin1Med, watDitJaarMin2Med)

def schrijfCsvData():
    strCsvData = ("gStd,gStdDiff,gGem,gGemDiff,gMed,gMedDiff,"
                  + "eStd,eStdDiff,eGem,eGemDiff,eMed,eMedDiff,"
                  + "wStd,wStdDiff,wGem,wGemDiff,wMed,wMedDiff\n"
                  + str("%.1f," % gasDitJaarStd) + str("%.1f," % round(gasDitJaarStd-gasDitJaarMin2Std, 1))
                  + str("%.1f," % gasDitJaarGem) + str("%.1f," % round(gasDitJaarGem-gasDitJaarMin2Gem, 1))
                  + str("%.1f," % gasDitJaarMed) + str("%.1f," % round(gasDitJaarMed-gasDitJaarMin2Med, 1))
                  + str("%.1f," % eleDitJaarStd) + str("%.1f," % round(eleDitJaarStd-eleDitJaarMin2Std, 1))
                  + str("%.1f," % eleDitJaarGem) + str("%.1f," % round(eleDitJaarGem-eleDitJaarMin2Gem, 1))
                  + str("%.1f," % eleDitJaarMed) + str("%.1f," % round(eleDitJaarMed-eleDitJaarMin2Med, 1))
                  + str("%.1f," % watDitJaarStd) + str("%.1f," % round(watDitJaarStd-watDitJaarMin2Std, 1))
                  + str("%.1f," % watDitJaarGem) + str("%.1f," % round(watDitJaarGem-watDitJaarMin2Gem, 1))
                  + str("%.1f," % watDitJaarMed) + str("%.1f\n" % round(watDitJaarMed-watDitJaarMin2Med, 1))
                  + str("%.1f," % gasDitJaarMin1Std) + str("%.1f," % round(gasDitJaarMin1Std-gasDitJaarMin2Std, 1))
                  + str("%.1f," % gasDitJaarMin1Gem) + str("%.1f," % round(gasDitJaarMin1Gem-gasDitJaarMin2Gem, 1))
                  + str("%.1f," % gasDitJaarMin1Med) + str("%.1f," % round(gasDitJaarMin1Med-gasDitJaarMin2Med, 1))
                  + str("%.1f," % eleDitJaarMin1Std) + str("%.1f," % round(eleDitJaarMin1Std-eleDitJaarMin2Std, 1))
                  + str("%.1f," % eleDitJaarMin1Gem) + str("%.1f," % round(eleDitJaarMin1Gem-eleDitJaarMin2Gem, 1))
                  + str("%.1f," % eleDitJaarMin1Med) + str("%.1f," % round(eleDitJaarMin1Med-eleDitJaarMin2Med, 1))
                  + str("%.1f," % watDitJaarMin1Std) + str("%.1f," % round(watDitJaarMin1Std-watDitJaarMin2Std, 1))
                  + str("%.1f," % watDitJaarMin1Gem) + str("%.1f," % round(watDitJaarMin1Gem-watDitJaarMin2Gem, 1))
                  + str("%.1f," % watDitJaarMin1Med) + str("%.1f\n" % round(watDitJaarMin1Med-watDitJaarMin2Med, 1))
                  + str("%.1f," % gasDitJaarMin2Std) + "0.0,"
                  + str("%.1f," % gasDitJaarMin2Gem) + "0.0,"
                  + str("%.1f," % gasDitJaarMin2Med) + "0.0,"
                  + str("%.1f," % eleDitJaarMin2Std) + "0.0,"
                  + str("%.1f," % eleDitJaarMin2Gem) + "0.0,"
                  + str("%.1f," % eleDitJaarMin2Med) + "0.0,"
                  + str("%.1f," % watDitJaarMin2Std) + "0.0,"
                  + str("%.1f," % watDitJaarMin2Gem) + "0.0,"
                  + str("%.1f," % watDitJaarMin2Med) + "0.0\n")
    f = open("stats-energiedata.csv", "w")
    f.write(strCsvData)
    f.close()

schrijfCsvData()
