#
# energie_verbruik.py
#
# Programma om verbruik van energie (gas + elektriciteit + water) te meten en
# een schatting te maken voor het verdere verloop van het jaar.
# Er wordt gebruikgemaakt van graaddagen van drie voorgaande jaren en van het
# verbruik van het voorgaande jaar voor een zo realistisch mogelijke schatting.
#
# Jonathan van der Steege, januari 2022

import pandas as pd
import matplotlib.pyplot as plotGas
import matplotlib.pyplot as plotEle
import matplotlib.pyplot as plotWat
from enum import IntEnum
from matplotlib import rcParams
from multiprocessing import Process


class Month(IntEnum):
    jan = 0
    feb = 1
    mrt = 2
    apr = 3
    mei = 4
    jun = 5
    jul = 6
    aug = 7
    sep = 8
    okt = 9
    nov = 10
    dec = 11

#
# CONSTANTEN
#
HUIDIG_JAAR = 2023
VORIG_JAAR = HUIDIG_JAAR - 1

#
# INVOEREN GEGEVENS HUIDIGE JAAR
#
MAAND = Month.apr
DAG_VAN_MAAND = 23
DAGEN_IN_MAAND = 30
VERBRUIK_GAS = 72
VERBRUIK_ELEKTRICITEIT = 92
VERBRUIK_WATER = 4
PRIJS_GAS = 1.39006
PRIJS_ELEKTRICITEIT = 0.39802
PRIJS_WATER = 1.021
VAST_LEVERING_GAS_JAAR = 83.49
VAST_LEVERING_ELE_JAAR = 83.49

# Inlezen data graaddagen, verbruik voorgaande jaar en afgeronde maanden
df = pd.read_csv('energiedata.csv')

totVerbrGasVrgJr = df['vrbr_gas_VrgJr']
totVerbrEleVrgJr = df['vrbr_ele_VrgJr']
totVerbrEleVrgJr2 = df['vrbr_ele_VrgJr2']
totVerbrWatVrgJr = df['vrbr_wat_VrgJr']
totVerbrWatVrgJr2 = df['vrbr_wat_VrgJr2']

#
# BEREKENINGEN GAS
#

# Vast verbruik gas per maand. Bepaal aan de hand van zomerverbruik
sumZomerverbruik = 0
for i in range(5, 9):
    sumZomerverbruik += df['vrbr_gas_VrgJr'][i]
vastGasMnd = sumZomerverbruik / 4
vastGasJr = vastGasMnd*12

# Bereken gemiddelde graaddagen per maand voor afgelopen vier jaar
gemGraaddagen = ((df['grddg_2019'] + df['grddg_2020']
                  + df['grddg_2021'] + df['grddg_2022']) / 4).round(2)

# Bereken percentage verbruik per maand voor graaddagen
sumGraaddagen = 0
for i in gemGraaddagen:
    sumGraaddagen += i
percGraaddagen = (gemGraaddagen / sumGraaddagen).round(2)

# Bereken percentage verbruik per maand voor gasverbruik vorig jaar
sumVerbrGasVrgJr = 0
for i in totVerbrGasVrgJr:
    sumVerbrGasVrgJr += i
percVerbrGasVrgJr = (totVerbrGasVrgJr / sumVerbrGasVrgJr)

# Correctie verbruik gas vorig jaar
corrVerbrGasVrgJr = totVerbrGasVrgJr - vastGasMnd
sumBerbrGasVrgJr_corr = 0
for i in corrVerbrGasVrgJr:
    sumBerbrGasVrgJr_corr += i
percVerbrGasVrgJr_corr = (corrVerbrGasVrgJr / sumBerbrGasVrgJr_corr)

#
# BEREKENINGEN ELEKTRICITEIT
#

# Gemiddelde verbruik elektriciteit voor een jaar
gemEle = df['gem_ele']

# Bereken percentage verbruik per maand voor elektriciteitsverbruik vorig jaar
sumVerbrEleVrgJr = 0
for i in totVerbrEleVrgJr:
    sumVerbrEleVrgJr += i
percVerbrEleVrgJr = (totVerbrEleVrgJr / sumVerbrEleVrgJr)
sumVerbrEleVrgJr2 = 0
for i in totVerbrEleVrgJr2:
    sumVerbrEleVrgJr2 += i
percVerbrEleVrgJr2 = (totVerbrEleVrgJr2 / sumVerbrEleVrgJr)

#
# BEREKENINGEN WATER
#
# Gemiddelde verbruik water voor een jaar
gemWat = df['gem_wat']

# Bereken percentage verbruik per maand voor waterverbruik vorig jaar
sumVerbrWatVrgJr = 0
for i in totVerbrWatVrgJr:
    sumVerbrWatVrgJr += i
percVerbrWatVrgJr = (totVerbrWatVrgJr / sumVerbrWatVrgJr)
sumVerbrWatVrgJr2 = 0
for i in totVerbrWatVrgJr2:
    sumVerbrWatVrgJr2 += i
percVerbrWatVrgJr2 = (totVerbrWatVrgJr2 / sumVerbrWatVrgJr2)

#
# BEREKENINGEN SCHATTING VERBRUIK
#

# Combineer graaddagen en verbruik vorig jaar als basis voor verwachting
# verbruik komende jaar
combiVerbrGas = ((percGraaddagen + percVerbrGasVrgJr_corr) / 2)

# Combineer gemiddeld elektriciteit en verbruik VrgJr als basis voor verwachting
combiVerbrEle = ((gemEle + percVerbrEleVrgJr + percVerbrEleVrgJr2) / 3)

# Combineer gemiddeld waterverbruik VrgJr als basis voor verwachting
combiVerbrWat = ((gemWat + percVerbrWatVrgJr + percVerbrWatVrgJr2) / 3)

percMnd = DAG_VAN_MAAND / DAGEN_IN_MAAND
verbrGasMnd = (VERBRUIK_GAS / percMnd) - vastGasMnd
verbrEleMnd = VERBRUIK_ELEKTRICITEIT / percMnd
verbrWatMnd = VERBRUIK_WATER / percMnd
totVerbrGas = 0
totVerbrEle = 0
totVerbrWat = 0

# Bereken schatting verbruik gas en elektriciteit voor huidig jaar
schatVerbrGasHdgJr = [0] * 12
schatVerbrEleHdgJr = [0] * 12
schatVerbrWatHdgJr = [0] * 12
verbrGasHdgJr = 0
verbrEleHdgJr = 0
verbrWatHdgJr = 0

# Als alleen eerste maand bekend is
if MAAND == Month.jan:
    verbrGasHdgJr = verbrGasMnd / combiVerbrGas[0]
    schatVerbrGasHdgJr = ((combiVerbrGas * verbrGasHdgJr) + vastGasMnd).round(2)
    verbrEleHdgJr = (verbrEleMnd / combiVerbrEle[0])
    schatVerbrEleHdgJr = (combiVerbrEle * verbrEleHdgJr).round(2)
    verbrWatHdgJr = verbrWatMnd / combiVerbrWat[0]
    schatVerbrWatHdgJr = (combiVerbrWat * verbrWatHdgJr).round(2)

# Als een of meerdere maanden afgerond zijn
else:
    gasMndnNJr = 0
    for i in range(0, MAAND):
        schatVerbrGasHdgJr[i] = df['vrbr_gas_HdgJr'][i]
        verbrGasHdgJr += schatVerbrGasHdgJr[i]
        gasMndnNJr += (schatVerbrGasHdgJr[i] / combiVerbrGas[i])
        schatVerbrEleHdgJr[i] = df['vrbr_ele_HdgJr'][i]
        verbrEleHdgJr += schatVerbrEleHdgJr[i]
        schatVerbrWatHdgJr[i] = df['vrbr_wat_HdgJr'][i]
        verbrWatHdgJr += schatVerbrWatHdgJr[i]
    gasMndnNJr /= (MAAND-1 + 1)
    for i in range(MAAND, 12):
        if i == MAAND:
            schatVerbrGasHdgJr[i] = ((verbrGasMnd / combiVerbrGas[MAAND])
                                    * combiVerbrGas[i] + vastGasMnd).round(2)
        else:
            schatVerbrGasHdgJr[i] = ((((verbrGasMnd / combiVerbrGas[MAAND])
                                    + gasMndnNJr)/2) * combiVerbrGas[i]
                                    + vastGasMnd).round(2)
        verbrGasHdgJr += schatVerbrGasHdgJr[i]
        schatVerbrEleHdgJr[i] = ((verbrEleMnd / combiVerbrEle[MAAND])
                                * combiVerbrEle[i]).round(2)
        verbrEleHdgJr += schatVerbrEleHdgJr[i]
        schatVerbrWatHdgJr[i] = ((verbrWatMnd / combiVerbrWat[MAAND])
                                * combiVerbrWat[i]).round(2)
        verbrWatHdgJr += schatVerbrWatHdgJr[i]

# Schatting totaal verbruik
schatTotGas = verbrGasHdgJr
schatTotEle = verbrEleHdgJr
schatTotWat = verbrWatHdgJr

# Bereken verschil vorig jaar : huidig jaar
verschGas = (schatTotGas - sumVerbrGasVrgJr)
verschEle = (schatTotEle - sumVerbrEleVrgJr)
verschWat = (schatTotWat - sumVerbrWatVrgJr)

# Bereken maandbedrag
maandbedrag = int((((schatTotGas * PRIJS_GAS)
                    + (schatTotEle * PRIJS_ELEKTRICITEIT)
                    + VAST_LEVERING_GAS_JAAR
                    + VAST_LEVERING_ELE_JAAR)/12))


#
# WEERGEVEN DATA
#
def ToonOverzicht():
    # Toon overzicht, verbruik vorig jaar en schatting huidig jaar
    schemaG = {"maand": df['maand'],
               "vrbr_g_VrgJr": totVerbrGasVrgJr,
               "vrw_g_HdgJr": schatVerbrGasHdgJr,
               "vrsch_gas": schatVerbrGasHdgJr - totVerbrGasVrgJr,
               "perc": ((1 - (schatVerbrGasHdgJr / totVerbrGasVrgJr))
                        * -100).round(1)}
    schemaE = {"maand": df['maand'],
               "vrbr_e_VrgJr": totVerbrEleVrgJr,
               "vrw_e_HdgJr": schatVerbrEleHdgJr,
               "vrsch_ele": (schatVerbrEleHdgJr - totVerbrEleVrgJr),
               "perc": ((1 - (schatVerbrEleHdgJr / totVerbrEleVrgJr))
                        * -100).round(1)}
    schemaW = {"maand": df['maand'],
               "vrbr_w_VrgJr": totVerbrWatVrgJr,
               "vrw_w_HdgJr": schatVerbrWatHdgJr,
               "vrsch_wat": (schatVerbrWatHdgJr - totVerbrWatVrgJr),
               "perc": ((1 - (schatVerbrWatHdgJr / totVerbrWatVrgJr))
                        * -100).round(1)}
    overzichtG = pd.DataFrame(schemaG)
    overzichtE = pd.DataFrame(schemaE)
    overzichtW = pd.DataFrame(schemaW)
    str_overzicht = ("Gas\n{sch_g}\n\nElektriciteit\n{sch_e}\n\nWater\n{sch_w}\n\n".format(sch_g=overzichtG, sch_e=overzichtE, sch_w=overzichtW))
    # Schrijf overzicht naar bestand
    f = open("energieverbruik_HdgJr_overzicht.txt", "w")
    f.write(str_overzicht)
    f.close()


def PrintOutput():
    strOutput = (f"{VORIG_JAAR}\n" +
                 ("\tVerbruik gas: %d m3\n" % sumVerbrGasVrgJr)
                 + ("\tVerbruik elektriciteit: %d kWh\n" % sumVerbrEleVrgJr)
                 + ("\tVerbruik water: %d m3\n" % sumVerbrWatVrgJr)
                 + f"{HUIDIG_JAAR}\n"
                 + ("\tGeschat gas: %d m3\n" % (schatTotGas))
                 + ("\tGeschat elektriciteit: %d kWh\n" % schatTotEle)
                 + ("\tGeschat water: %d m3\n" % schatTotWat)
                 + "Verschil verbruik\n"
                 + ("\tGas: %d m3 (EUR %d)\n" % (verschGas, (verschGas * PRIJS_GAS)))
                 + ("\tElektriciteit: %d kWh (EUR %d)\n" %
                    (verschEle, (verschEle * PRIJS_ELEKTRICITEIT)))
                 + ("\tWater: %d m3 (EUR %d)\n" % (verschWat, (verschWat * PRIJS_WATER)))
                 + ("Bedragen\n")
                 + ("\tTarieven: [gas %.2f / m3] [ele %.2f / kWh] [wat %.2f / m3]\n"
                   % (PRIJS_GAS, PRIJS_ELEKTRICITEIT, PRIJS_WATER))
                 + ("\tMaandbedrag: EUR %d\n") % maandbedrag)
    # Toon uitvoer overzicht en totalen
    #print(str_overzicht)
    print(strOutput)

    # Schrijf uitvoer naar bestand
    f = open("energieverbruik_HdgJr.txt", "w")
    f.write(strOutput)
    f.close()


def SchrijfCsvData():
    strCsvData = ("vrbr_VrgJr,sch_HdgJr,vrsch_vrbr,vrsch_bedr,tar,maandbedr\n"
                  + str("%d" % sumVerbrGasVrgJr)
                  + str(",%d" % (schatTotGas))
                  + str(",%d" % verschGas)
                  + str(",%d" % (verschGas * PRIJS_GAS))
                  + str(",%.2f" % PRIJS_GAS)
                  + str(",0\n")
                  + str("%d" % sumVerbrEleVrgJr)
                  + str(",%d" % schatTotEle)
                  + str(",%d" % verschEle)
                  + str(",%d" % (verschEle * PRIJS_ELEKTRICITEIT))
                  + str(",%.2f" % PRIJS_ELEKTRICITEIT)
                  + str(",0\n")
                  + str("%d" % sumVerbrWatVrgJr)
                  + str(",%d" % schatTotWat)
                  + str(",%d" % verschWat)
                  + str(",%d" % (verschWat * PRIJS_WATER))
                  + str(",%.2f" % PRIJS_WATER)
                  + str(",0\n")
                  + str("0,0,0,0,0,%d\n" % maandbedrag))

    # Schrijf csv-data naar bestand
    f = open("energie_hubrpi.csv", "w")
    f.write(strCsvData)
    f.close()


# Toon grafieken
maanden = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep",
           "okt", "nov", "dec"]
rcParams['axes.edgecolor'] = 'White'
rcParams['figure.figsize'] = [7.8, 3.8]


def GrafiekGas():
    # Grafiek gasverbruik
    plotGas.figure()
    plotGas.plot(maanden, schatVerbrGasHdgJr, color='tab:orange',
                 label="2023", linewidth=5)
    plotGas.plot(maanden, df['vrbr_gas_VrgJr'], color='tab:blue', label="2022",
                 linewidth=5)
    #plotGas.title("Gas", color='White')
    #plotGas.xlabel("maand", color='White')
    plotGas.ylabel("verbruik (m3)", color='White')
    plotGas.tick_params(colors='White')
    plotGas.ylim(bottom=0)
    plotGas.grid()
    plotGas.legend()
    plotGas.tight_layout()
    plotGas.savefig('gasverbruik.png', dpi=100, transparent=True)
    #plotGas.show()


def GrafiekElektriciteit():
    # Grafiek elektriciteitsverbruik
    plotEle.figure()
    plotEle.plot(maanden, schatVerbrEleHdgJr,
                 color='tab:orange', label="2023", linewidth=5)
    plotEle.plot(maanden, df['vrbr_ele_VrgJr'], color='tab:blue', label="2022",
                 linewidth=5)
    #plotEle.title("Elektriciteit", color='White')
    #plotEle.xlabel("maand", color='White')
    plotEle.ylabel("verbruik (kWh)", color='White')
    plotEle.tick_params(colors='White')
    plotEle.ylim(bottom=0)
    plotEle.grid()
    plotEle.legend()
    plotEle.tight_layout()
    plotEle.savefig('elektriciteitsverbruik.png', dpi=100, transparent=True)
    #plotEle.show()


def GrafiekWater():
    # Grafiek waterverbruik
    plotWat.figure()
    plotWat.plot(maanden, schatVerbrWatHdgJr, color='tab:orange',
                 label="2023", linewidth=5)
    plotWat.plot(maanden, df['vrbr_wat_VrgJr'], color='tab:blue', label="2022",
                 linewidth=5)
    #plotWat.title("Water", color='White')
    #plotWat.xlabel("maand", color='White')
    plotWat.ylabel("verbruik (m3)", color='White')
    plotWat.tick_params(colors='White')
    plotWat.ylim(bottom=0)
    plotWat.grid()
    plotWat.legend()
    plotWat.tight_layout()
    plotWat.savefig('waterverbruik.png', dpi=100, transparent=True)
    #plotEle.show()


p1 = Process(target=ToonOverzicht)
p2 = Process(target=PrintOutput)
p3 = Process(target=SchrijfCsvData)
p4 = Process(target=GrafiekGas)
p5 = Process(target=GrafiekElektriciteit)
p6 = Process(target=GrafiekWater)
p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()
p1.join()
p2.join()
p3.join()
p4.join()
p5.join()
p6.join()
