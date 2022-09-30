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
# INVOEREN GEGEVENS HUIDIGE JAAR
#
MAAND = Month.sep
DAG_VAN_MAAND = 30
DAGEN_IN_MAAND = 30
VERBRUIK_GAS = 20
VERBRUIK_ELEKTRICITEIT = 89
VERBRUIK_WATER = 4
PRIJS_GAS = 1.63326
PRIJS_ELEKTRICITEIT = 0.53264
PRIJS_WATER = 1.021
VAST_LEVERING_GAS_JAAR = 71.39
VAST_LEVERING_ELE_JAAR = 71.39
VAST_LEVERING_DAG = 0.19559

# Inlezen data graaddagen, verbruik voorgaande jaar en afgeronde maanden
df = pd.read_csv('energiedata.csv')

totVerbrGas2021 = df['vrbr_gas_2021']
totVerbrEle2021 = df['vrbr_ele_2021']
totVerbrWat2021 = df['vrbr_wat_2021']

#
# BEREKENINGEN GAS
#

# Vast verbruik gas per maand. Bepaal aan de hand van zomerverbruik
sumZomerverbruik = 0
for i in range(5, 9):
    sumZomerverbruik += df['vrbr_gas_2021'][i]
vastGasMnd = sumZomerverbruik / 4
vastGasJr = vastGasMnd*12

# Bereken gemiddelde graaddagen per maand voor afgelopen drie jaar
gemGraaddagen = ((df['grddg_2019'] + df['grddg_2020']
                  + df['grddg_2021']) / 3).round(2)

# Bereken percentage verbruik per maand voor graaddagen
sumGraaddagen = 0
for i in gemGraaddagen:
    sumGraaddagen += i
percGraaddagen = (gemGraaddagen / sumGraaddagen).round(2)

# Bereken percentage verbruik per maand voor gasverbruik 2021
sumVerbrGas2021 = 0
for i in totVerbrGas2021:
    sumVerbrGas2021 += i
percVerbrGas2021 = (totVerbrGas2021 / sumVerbrGas2021)

# Correctie verbruik gas 2021
corrVerbrGas2021 = totVerbrGas2021 - vastGasMnd
sumBerbrGas2021_corr = 0
for i in corrVerbrGas2021:
    sumBerbrGas2021_corr += i
percVerbrGas2021_corr = (corrVerbrGas2021 / sumBerbrGas2021_corr)

#
# BEREKENINGEN ELEKTRICITEIT
#

# Gemiddelde verbruik elektriciteit voor een jaar
gemEle = df['gem_ele']

# Bereken percentage verbruik per maand voor elektriciteitsverbruik 2021
sumVerbrEle2021 = 0
for i in totVerbrEle2021:
    sumVerbrEle2021 += i
percVerbrEle2021 = (totVerbrEle2021 / sumVerbrEle2021)

#
# BEREKENINGEN WATER
#
# Gemiddelde verbruik water voor een jaar
gemWat = df['gem_wat']

# Bereken percentage verbruik per maand voor waterverbruik 2021
sumVerbrWat2021 = 0
for i in totVerbrWat2021:
    sumVerbrWat2021 += i
percVerbrWat2021 = (totVerbrWat2021 / sumVerbrWat2021)

#
# BEREKENINGEN SCHATTING VERBRUIK
#

# Combineer graaddagen en verbruik 2021 als basis voor verwachting
# verbruik komende jaar
combiVerbrGas = ((percGraaddagen + percVerbrGas2021_corr) / 2)

# Combineer gemiddeld elektriciteit en verbruik 2021 als basis voor verwachting
combiVerbrEle = ((gemEle + percVerbrEle2021) / 2)

# Combineer gemiddeld waterverbruik 2021 als basis voor verwachting
combiVerbrWat = ((gemWat + percVerbrWat2021) /2)

percMnd = DAG_VAN_MAAND / DAGEN_IN_MAAND
verbrGasMnd = (VERBRUIK_GAS / percMnd) - vastGasMnd
verbrEleMnd = VERBRUIK_ELEKTRICITEIT / percMnd
verbrWatMnd = VERBRUIK_WATER / percMnd
totVerbrGas = 0
totVerbrEle = 0
totVerbrWat = 0

# Bereken schatting verbruik gas en elektriciteit voor 2022
schatVerbrGas2022 = [0] * 12
schatVerbrEle2022 = [0] * 12
schatVerbrWat2022 = [0] * 12
verbrGas2022 = 0
verbrEle2022 = 0
verbrWat2022 = 0

# Als alleen eerste maand bekend is
if MAAND == Month.jan:
    verbrGas2022 = verbrGasMnd / combiVerbrGas[0]
    schatVerbrGas2022 = ((combiVerbrGas * verbrGas2022) + vastGasMnd).round(2)
    verbrEle2022 = (verbrEleMnd / combiVerbrEle[0])
    schatVerbrEle2022 = (combiVerbrEle * verbrEle2022).round(2)
    verbrWat2022 = verbrWatMnd / combiVerbrWat[0]
    schatVerbrWat2022 = (combiVerbrWat * verbrWat2022).round(2)

# Als een of meerdere maanden afgerond zijn
else:
    gasMndnNJr = 0
    for i in range(0, MAAND):
        schatVerbrGas2022[i] = df['vrbr_gas_2022'][i]
        verbrGas2022 += schatVerbrGas2022[i]
        gasMndnNJr += (schatVerbrGas2022[i] / combiVerbrGas[i])
        schatVerbrEle2022[i] = df['vrbr_ele_2022'][i]
        verbrEle2022 += schatVerbrEle2022[i]
        schatVerbrWat2022[i] = df['vrbr_wat_2022'][i]
        verbrWat2022 += schatVerbrWat2022[i]
    gasMndnNJr /= MAAND-1
    for i in range(MAAND, 12):
        if i == MAAND:
            schatVerbrGas2022[i] = ((verbrGasMnd / combiVerbrGas[MAAND])
                                    * combiVerbrGas[i] + vastGasMnd).round(2)
        else:
            schatVerbrGas2022[i] = ((((verbrGasMnd / combiVerbrGas[MAAND])
                                    + gasMndnNJr)/2) * combiVerbrGas[i]
                                    + vastGasMnd).round(2)
        verbrGas2022 += schatVerbrGas2022[i]
        schatVerbrEle2022[i] = ((verbrEleMnd / combiVerbrEle[MAAND])
                                * combiVerbrEle[i]).round(2)
        verbrEle2022 += schatVerbrEle2022[i]
        schatVerbrWat2022[i] = ((verbrWatMnd / combiVerbrWat[MAAND])
                                * combiVerbrWat[i]).round(2)
        verbrWat2022 += schatVerbrWat2022[i]

# Schatting totaal verbruik
schatTotGas = verbrGas2022
schatTotEle = verbrEle2022
schatTotWat = verbrWat2022

# Bereken verschil 2021 - 2022
verschGas = (schatTotGas - sumVerbrGas2021)
verschEle = (schatTotEle - sumVerbrEle2021)
verschWat = (schatTotWat - sumVerbrWat2021)

# Bereken maandbedrag
maandbedrag = int((((schatTotGas * PRIJS_GAS)
                    + (schatTotEle * PRIJS_ELEKTRICITEIT)
                    + VAST_LEVERING_GAS_JAAR
                    + VAST_LEVERING_ELE_JAAR
                    + (2 * (VAST_LEVERING_DAG * 365)))/12))


#
# WEERGEVEN DATA
#
def ToonOverzicht():
    # Toon overzicht, verbruik 2021 en schatting 2022
    schemaG = {"maand": df['maand'],
               "vrbr_g_2021": totVerbrGas2021,
               "vrw_g_2022": schatVerbrGas2022,
               "vrsch_gas": schatVerbrGas2022 - totVerbrGas2021,
               "perc": ((1 - (schatVerbrGas2022 / totVerbrGas2021))
                        * -100).round(1)}
    schemaE = {"maand": df['maand'],
               "vrbr_e_2021": totVerbrEle2021,
               "vrw_e_2022": schatVerbrEle2022,
               "vrsch_ele": (schatVerbrEle2022 - totVerbrEle2021),
               "perc": ((1 - (schatVerbrEle2022 / totVerbrEle2021))
                        * -100).round(1)}
    schemaW = {"maand": df['maand'],
               "vrbr_w_2021": totVerbrWat2021,
               "vrw_w_2022": schatVerbrWat2022,
               "vrsch_wat": (schatVerbrWat2022 - totVerbrWat2021),
               "perc": ((1 - (schatVerbrWat2022 / totVerbrWat2021))
                        * -100).round(1)}
    overzichtG = pd.DataFrame(schemaG)
    overzichtE = pd.DataFrame(schemaE)
    overzichtW = pd.DataFrame(schemaW)
    str_overzicht = ("Gas\n{sch_g}\n\nElektriciteit\n{sch_e}\n\nWater\n{sch_w}\n\n".format(sch_g=overzichtG, sch_e=overzichtE, sch_w=overzichtW))
    # Schrijf overzicht naar bestand
    f = open("energieverbruik_2022_overzicht.txt", "w")
    f.write(str_overzicht)
    f.close()


def PrintOutput():
    strOutput = ("2021\n" +
                 ("\tVerbruik gas: %d m3\n" % sumVerbrGas2021)
                 + ("\tVerbruik elektriciteit: %d kWh\n" % sumVerbrEle2021)
                 + ("\tVerbruik water: %d m3\n" % sumVerbrWat2021)
                 + "2022\n"
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
    f = open("energieverbruik_2022.txt", "w")
    f.write(strOutput)
    f.close()


def SchrijfCsvData():
    strCsvData = ("vrbr_2021,sch_2022,vrsch_vrbr,vrsch_bedr,tar,maandbedr\n"
                  + str("%d" % sumVerbrGas2021)
                  + str(",%d" % (schatTotGas))
                  + str(",%d" % verschGas)
                  + str(",%d" % (verschGas * PRIJS_GAS))
                  + str(",%.2f" % PRIJS_GAS)
                  + str(",0\n")
                  + str("%d" % sumVerbrEle2021)
                  + str(",%d" % schatTotEle)
                  + str(",%d" % verschEle)
                  + str(",%d" % (verschEle * PRIJS_ELEKTRICITEIT))
                  + str(",%.2f" % PRIJS_ELEKTRICITEIT)
                  + str(",0\n")
                  + str("%d" % sumVerbrWat2021)
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
    plotGas.plot(maanden, schatVerbrGas2022, color='tab:orange',
                 label="2022", linewidth=5)
    plotGas.plot(maanden, df['vrbr_gas_2021'], color='tab:blue', label="2021",
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
    plotEle.plot(maanden, schatVerbrEle2022,
                 color='tab:orange', label="2022", linewidth=5)
    plotEle.plot(maanden, df['vrbr_ele_2021'], color='tab:blue', label="2021",
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
    plotWat.plot(maanden, schatVerbrWat2022, color='tab:orange',
                 label="2022", linewidth=5)
    plotWat.plot(maanden, df['vrbr_wat_2021'], color='tab:blue', label="2021",
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
