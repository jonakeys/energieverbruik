#
# energieverbruik.py
#
# Programma om verbruik van energie (gas + elektriciteit + water) te meten en
# een schatting te maken voor het verdere verloop van het jaar.
# Er wordt gebruikgemaakt van graaddagen van drie voorgaande jaren en van het
# verbruik van het voorgaande jaar voor een zo realistisch mogelijke schatting.
#
# Jonathan van der Steege, januari 2022

from enum import Enum
from multiprocessing import Process
import pandas as pd
import matplotlib.pyplot as plotGas
import matplotlib.pyplot as plotEle
import matplotlib.pyplot as plotWat
from matplotlib import rcParams

class Month(Enum):
    JAN = 0, 31
    FEB = 1, 28
    MRT = 2, 31
    APR = 3, 30
    MEI = 4, 31
    JUN = 5, 30
    JUL = 6, 31
    AUG = 7, 31
    SEP = 8, 30
    OKT = 9, 31
    NOV = 10, 30
    DEC = 11, 31

    def __init__(self, rank, days):
        self.rank = rank
        self.days = days

#
# CONSTANTEN
#
HUIDIG_JAAR = 2025
VORIG_JAAR = HUIDIG_JAAR - 1

#
# INVOEREN GEGEVENS HUIDIGE JAAR
#
MAAND = Month.OKT
DAG_VAN_MAAND = 31
DAGEN_IN_MAAND = MAAND.days
VERBRUIK_GAS = 65
VERBRUIK_ELEKTRICITEIT = 114
VERBRUIK_WATER = 10.4
PRIJS_GAS = 1.20840
PRIJS_ELEKTRICITEIT = 0.28926
PRIJS_WATER = 1.021
VAST_LEVERING_GAS_JAAR = 555.9315
VAST_LEVERING_ELE_JAAR = 350.2942
VERMINDERING_JAAR = 635.19

# Inlezen data graaddagen, verbruik voorgaande jaar en afgeronde maanden
df = pd.read_csv('energiedata.csv')

TOT_VEBR_GAS_VRG_JR = df['vrbr_gas_VrgJr']
TOT_VEBR_GAS_VRG_JR2 = df['vrbr_gas_VrgJr2']
TOT_VEBR_GAS_VRG_JR3 = df['vrbr_gas_VrgJr3']
TOT_VEBR_GAS_VRG_JR4 = df['vrbr_gas_VrgJr4']
TOT_VEBR_ELE_VRG_JR = df['vrbr_ele_VrgJr']
TOT_VEBR_ELE_VRG_JR2 = df['vrbr_ele_VrgJr2']
TOT_VEBR_ELE_VRG_JR3 = df['vrbr_ele_VrgJr3']
TOT_VEBR_ELE_VRG_JR4 = df['vrbr_ele_VrgJr4']
TOT_VEBR_WAT_VRG_JR = df['vrbr_wat_VrgJr']
TOT_VEBR_WAT_VRG_JR2 = df['vrbr_wat_VrgJr2']
TOT_VEBR_WAT_VRG_JR3 = df['vrbr_wat_VrgJr3']
TOT_VEBR_WAT_VRG_JR4 = df['vrbr_wat_VrgJr4']

TOT_VEBR_GAS_VRG_JR2 = (TOT_VEBR_GAS_VRG_JR2 + TOT_VEBR_GAS_VRG_JR3 + TOT_VEBR_GAS_VRG_JR4) / 3
TOT_VEBR_ELE_VRG_JR2 = (TOT_VEBR_ELE_VRG_JR2 + TOT_VEBR_ELE_VRG_JR3 + TOT_VEBR_ELE_VRG_JR4) / 3
TOT_VEBR_WAT_VRG_JR2 = (TOT_VEBR_WAT_VRG_JR2 + TOT_VEBR_WAT_VRG_JR3 + TOT_VEBR_WAT_VRG_JR4) / 3

#
# BEREKENINGEN GAS
#

# Vast verbruik gas per maand. Bepaal aan de hand van zomerverbruik
SUM_ZOMERVERBRUIK = 0
for i in range(6, 9):
    SUM_ZOMERVERBRUIK += df['vrbr_gas_VrgJr'][i]
vastGasMnd = SUM_ZOMERVERBRUIK / 3
vastGasJr = vastGasMnd*12

# Bereken gemiddelde graaddagen per maand voor afgelopen vijf jaar
gemGraaddagen = ((df['grddg_2019'] + df['grddg_2020'] + df['grddg_2021']
                  + df['grddg_2022'] + df['grddg_2023'] + df['grddg_2024']) / 6).round(2)

# Bereken percentage verbruik per maand voor graaddagen
SUM_GRAADDAGEN = 0
for i in gemGraaddagen:
    SUM_GRAADDAGEN += i
percGraaddagen = gemGraaddagen / SUM_GRAADDAGEN

# Bereken percentage verbruik per maand voor gasverbruik vorig jaar
SUM_VERBR_GAS_VRG_JR = 0
for i in TOT_VEBR_GAS_VRG_JR:
    SUM_VERBR_GAS_VRG_JR += i
percVerbrGasVrgJr = TOT_VEBR_GAS_VRG_JR / SUM_VERBR_GAS_VRG_JR

# Correctie verbruik gas vorig jaar
corrVerbrGasVrgJr = TOT_VEBR_GAS_VRG_JR - vastGasMnd
SUM_VERBR_GAS_VRG_JR_CORR = 0
for i in corrVerbrGasVrgJr:
    SUM_VERBR_GAS_VRG_JR_CORR += i
percVerbrGasVrgJr = TOT_VEBR_GAS_VRG_JR / SUM_VERBR_GAS_VRG_JR_CORR

corrVerbrGasVrgJr2 = TOT_VEBR_GAS_VRG_JR2 - vastGasMnd
SUM_VERBR_GAS_VRG_JR2_CORR = 0
for i in corrVerbrGasVrgJr2:
    SUM_VERBR_GAS_VRG_JR2_CORR += i
percVerbrGasVrgJr2 = corrVerbrGasVrgJr2 / SUM_VERBR_GAS_VRG_JR2_CORR

#
# BEREKENINGEN ELEKTRICITEIT
#

# Gemiddelde verbruik elektriciteit voor een jaar
gemEle = df['gem_ele']

# Bereken percentage verbruik per maand voor elektriciteitsverbruik vorig jaar
SUM_VERBR_ELE_VRG_JR = 0
for i in TOT_VEBR_ELE_VRG_JR:
    SUM_VERBR_ELE_VRG_JR += i
percVerbrEleVrgJr = TOT_VEBR_ELE_VRG_JR / SUM_VERBR_ELE_VRG_JR

SUM_VERBR_ELE_VRG_JR2 = 0
for i in TOT_VEBR_ELE_VRG_JR2:
    SUM_VERBR_ELE_VRG_JR2 += i
percVerbrEleVrgJr2 = TOT_VEBR_ELE_VRG_JR2 / SUM_VERBR_ELE_VRG_JR2

#
# BEREKENINGEN WATER
#
# Gemiddelde verbruik water voor een jaar
gemWat = df['gem_wat']

# Bereken percentage verbruik per maand voor waterverbruik vorig jaar
SUM_VERBR_WAT_VRG_JR = 0
for i in TOT_VEBR_WAT_VRG_JR:
    SUM_VERBR_WAT_VRG_JR += i
percVerbrWatVrgJr = TOT_VEBR_WAT_VRG_JR / SUM_VERBR_WAT_VRG_JR

SUM_VERBR_WAT_VRG_JR2 = 0
for i in TOT_VEBR_WAT_VRG_JR2:
    SUM_VERBR_WAT_VRG_JR2 += i
percVerbrWatVrgJr2 = TOT_VEBR_WAT_VRG_JR2 / SUM_VERBR_WAT_VRG_JR2

#
# BEREKENINGEN SCHATTING VERBRUIK
#

# Combineer graaddagen en verbruik vorige jaren als basis voor verwachting
# verbruik komende jaar
combiVerbrGas = (percGraaddagen + (3 * percVerbrGasVrgJr) + (1 * percVerbrGasVrgJr2)) / 5

# Combineer gemiddeld elektriciteit en verbruik vorige jaren als basis voor verwachting
combiVerbrEle = (gemEle + (3 * percVerbrEleVrgJr) + (1 * percVerbrEleVrgJr2)) / 5

# Combineer gemiddeld waterverbruik en verbruik vorige jaren als basis voor verwachting
combiVerbrWat = (gemWat + (3 * percVerbrWatVrgJr) + (1 * percVerbrWatVrgJr2)) / 5

percMnd = DAG_VAN_MAAND / DAGEN_IN_MAAND
VERBR_GASMnd = (VERBRUIK_GAS / percMnd) - vastGasMnd
VERBR_GASMnd = max(VERBR_GASMnd, 0)
VERBR_ELEMnd = VERBRUIK_ELEKTRICITEIT / percMnd
VERBR_WATMnd = VERBRUIK_WATER / percMnd
TOT_VEBR_GAS = 0
TOT_VEBR_ELE = 0
TOT_VEBR_WAT = 0

# Bereken schatting verbruik gas en elektriciteit voor huidig jaar
schatVerbrGas_HDG_JR = [0] * 12
schatVerbrEle_HDG_JR = [0] * 12
schatVerbrWat_HDG_JR = [0] * 12
VERBR_GAS_HDG_JR = 0
VERBR_ELE_HDG_JR = 0
VERBR_WAT_HDG_JR = 0
SUM_SCHAT_GAS = 0
SUM_SCHAT_ELE = 0
SUM_SCHAT_WAT = 0

# Als alleen eerste maand bekend is
if MAAND == Month.JAN:
    VERBR_GAS_HDG_JR = VERBR_GASMnd / combiVerbrGas[0]
    schatVerbrGas_HDG_JR = ((combiVerbrGas * VERBR_GAS_HDG_JR) + vastGasMnd).round(2)
    VERBR_ELE_HDG_JR = VERBR_ELEMnd / combiVerbrEle[0]
    schatVerbrEle_HDG_JR = (combiVerbrEle * VERBR_ELE_HDG_JR).round(2)
    VERBR_WAT_HDG_JR = VERBR_WATMnd / combiVerbrWat[0]
    schatVerbrWat_HDG_JR = (combiVerbrWat * VERBR_WAT_HDG_JR).round(2)
    for i in range (0, 12):
        SUM_SCHAT_GAS += schatVerbrGas_HDG_JR[i]
        SUM_SCHAT_ELE += schatVerbrEle_HDG_JR[i]
        SUM_SCHAT_WAT += schatVerbrWat_HDG_JR[i]

# Als een of meerdere maanden afgerond zijn
else:
    GAS_MNDN_N_JR = 0
    ELE_MNDN_N_JR = 0
    WAWAT_MNDN_N_JR = 0
    PERC_GAS_HDG_JR = 0
    PERC_ELE_HDG_JR = 0
    PERC_WAT_HDG_JR = 0
    for i in range(0, MAAND.rank):
        schatVerbrGas_HDG_JR[i] = df['vrbr_gas_HdgJr'][i]
        SUM_SCHAT_GAS += schatVerbrGas_HDG_JR[i]
        GAS_MNDN_N_JR += (schatVerbrGas_HDG_JR[i] / combiVerbrGas[i])
        PERC_GAS_HDG_JR += schatVerbrGas_HDG_JR[i]/df['vrbr_gas_VrgJr'][i]
        schatVerbrEle_HDG_JR[i] = df['vrbr_ele_HdgJr'][i]
        SUM_SCHAT_ELE += schatVerbrEle_HDG_JR[i]
        ELE_MNDN_N_JR += (schatVerbrEle_HDG_JR[i] / combiVerbrEle[i])
        PERC_ELE_HDG_JR += schatVerbrEle_HDG_JR[i]/df['vrbr_ele_VrgJr'][i]
        schatVerbrWat_HDG_JR[i] = df['vrbr_wat_HdgJr'][i]
        SUM_SCHAT_WAT += schatVerbrWat_HDG_JR[i]
        WAWAT_MNDN_N_JR += (schatVerbrWat_HDG_JR[i] / combiVerbrWat[i])
        PERC_WAT_HDG_JR += schatVerbrWat_HDG_JR[i]/df['vrbr_wat_VrgJr'][i]
    GAS_MNDN_N_JR /= MAAND.rank
    ELE_MNDN_N_JR /= MAAND.rank
    WAWAT_MNDN_N_JR /= MAAND.rank
    PERC_GAS_HDG_JR = PERC_GAS_HDG_JR / MAAND.rank
    PERC_ELE_HDG_JR = PERC_ELE_HDG_JR / MAAND.rank
    PERC_WAT_HDG_JR = PERC_WAT_HDG_JR / MAAND.rank
    for i in range(MAAND.rank, 12):
        if i == MAAND.rank:
            schatVerbrGas_HDG_JR[i] = (((VERBR_GASMnd / combiVerbrGas[MAAND.rank])
                                     * combiVerbrGas[i]) + vastGasMnd).round(2)
            schatVerbrEle_HDG_JR[i] = ((VERBR_ELEMnd / combiVerbrEle[MAAND.rank])
                                     * combiVerbrEle[i]).round(2)
            schatVerbrWat_HDG_JR[i] = ((VERBR_WATMnd / combiVerbrWat[MAAND.rank])
                                     * combiVerbrWat[i]).round(2)
        else:
            schatVerbrGas_HDG_JR[i] = ((((((
                (VERBR_GASMnd / combiVerbrGas[MAAND.rank]) + (2 * GAS_MNDN_N_JR)) / 3)
                    * combiVerbrGas[i]) + vastGasMnd)
                    + (df['vrbr_gas_VrgJr'][i] * PERC_GAS_HDG_JR)) / 2).round(2)
            schatVerbrEle_HDG_JR[i] = ((((((
                (VERBR_ELEMnd / combiVerbrEle[MAAND.rank]) + PERC_ELE_HDG_JR)
                    + (2 * ELE_MNDN_N_JR))/3) * combiVerbrEle[i])
                    + (df['vrbr_ele_VrgJr'][i] * PERC_ELE_HDG_JR))/2).round(2)
            schatVerbrWat_HDG_JR[i] = ((((((
                (VERBR_WATMnd / combiVerbrWat[MAAND.rank]) + PERC_WAT_HDG_JR)
                    + (2 * WAWAT_MNDN_N_JR))/3)* combiVerbrWat[i])
                    + (df['vrbr_wat_VrgJr'][i] * PERC_WAT_HDG_JR)) / 2).round(2)
        SUM_SCHAT_GAS += schatVerbrGas_HDG_JR[i]
        SUM_SCHAT_ELE += schatVerbrEle_HDG_JR[i]
        SUM_SCHAT_WAT += schatVerbrWat_HDG_JR[i]

# Schatting totaal verbruik
schatTotGas = SUM_SCHAT_GAS
schatTotEle = SUM_SCHAT_ELE
schatTotWat = SUM_SCHAT_WAT

# Bereken verschil vorig jaar : huidig jaar
verschGas = schatTotGas - SUM_VERBR_GAS_VRG_JR
verschEle = schatTotEle - SUM_VERBR_ELE_VRG_JR
verschWat = schatTotWat - SUM_VERBR_WAT_VRG_JR

# Bereken MAANDBEDRAG
MAANDBEDRAG = int((((schatTotGas * PRIJS_GAS)
                    + (schatTotEle * PRIJS_ELEKTRICITEIT)
                    + VAST_LEVERING_GAS_JAAR
                    + VAST_LEVERING_ELE_JAAR
                    - VERMINDERING_JAAR)/12))


#
# WEERGEVEN DATA
#
def toon_overzicht():
    # Toon overzicht, verbruik vorig jaar en schatting huidig jaar
    schema_g = {"maand": df['maand'],
               "vrbr_g_VrgJr": TOT_VEBR_GAS_VRG_JR,
               "vrw_g_hdg_jr": schatVerbrGas_HDG_JR,
               "vrsch_gas": schatVerbrGas_HDG_JR - TOT_VEBR_GAS_VRG_JR,
               "perc": ((1 - (schatVerbrGas_HDG_JR / TOT_VEBR_GAS_VRG_JR))
                        * -100).round(1)}
    schema_e = {"maand": df['maand'],
               "vrbr_e_VrgJr": TOT_VEBR_ELE_VRG_JR,
               "vrw_e_hdg_jr": schatVerbrEle_HDG_JR,
               "vrsch_ele": (schatVerbrEle_HDG_JR - TOT_VEBR_ELE_VRG_JR),
               "perc": ((1 - (schatVerbrEle_HDG_JR / TOT_VEBR_ELE_VRG_JR))
                        * -100).round(1)}
    schema_w = {"maand": df['maand'],
               "vrbr_w_VrgJr": TOT_VEBR_WAT_VRG_JR,
               "vrw_w_hdg_jr": schatVerbrWat_HDG_JR,
               "vrsch_wat": (schatVerbrWat_HDG_JR - TOT_VEBR_WAT_VRG_JR),
               "perc": ((1 - (schatVerbrWat_HDG_JR / TOT_VEBR_WAT_VRG_JR))
                        * -100).round(1)}
    overzicht_g = pd.DataFrame(schema_g)
    overzicht_e = pd.DataFrame(schema_e)
    overzicht_w = pd.DataFrame(schema_w)
    str_overzicht = f"Gas\n{overzicht_g}\n\n"\
        f"Elektriciteit\n{overzicht_e}\n\n"\
        f"Water\n{overzicht_w}\n\n"
    # Schrijf overzicht naar bestand
    f = open("energieverbruik_HdgJr_overzicht.txt", "w")
    f.write(str_overzicht)
    f.close()


def print_output():
    strOutput = f"{VORIG_JAAR}\n"\
        f"\tVerbruik gas: {SUM_VERBR_GAS_VRG_JR:.0f} m3\n"\
        f"\tVerbruik elektriciteit: {SUM_VERBR_ELE_VRG_JR:.0f} kWh\n"\
        f"\tVerbruik water: {SUM_VERBR_WAT_VRG_JR:.0f} m3\n"\
        f"{HUIDIG_JAAR}\n"\
        f"\tGeschat gas: {schatTotGas:.0f} m3\n"\
        f"\tGeschat elektriciteit: {schatTotEle:.0f} kWh\n"\
        f"\tGeschat water: {schatTotWat:.0f} m3\n"\
        f"Verschil verbruik\n"\
        f"\tGas: {verschGas:.0f} m3"\
        f" (EUR {(verschGas * PRIJS_GAS):.0f})\n"\
        f"\tElektriciteit: {verschEle:.0f} kWh"\
        f" (EUR {(verschEle * PRIJS_ELEKTRICITEIT):.0f})\n"\
        f"\tWater: {verschWat:.0f} m3"\
        f" (EUR {(verschWat * PRIJS_WATER):.0f})\n"\
        f"Bedragen\n"\
        f"\tTarieven: [gas {PRIJS_GAS:.2f} / m3]"\
        f" [ele {PRIJS_ELEKTRICITEIT:.2f} / kWh]"\
        f" [wat {PRIJS_WATER:.2f} / m3]\n"\
        f"\tMaandbedrag: EUR {MAANDBEDRAG:.0f}\n"
    # Toon uitvoer overzicht en totalen
    print(strOutput)

    # Schrijf uitvoer naar bestand
    f = open("energieverbruik_HdgJr.txt", "w")
    f.write(strOutput)
    f.close()


def schrijf_csv_data():
    string_csv_data = f"vrbr_VrgJr,sch_HdgJr,vrsch_vrbr,vrsch_bedr,tar,maandbedr\n"\
        f"{SUM_VERBR_GAS_VRG_JR:.0f},{schatTotGas:.0f},{verschGas:.0f}"\
        f",{(verschGas * PRIJS_GAS):.0f},{PRIJS_GAS:.2f},0\n"\
        f"{SUM_VERBR_ELE_VRG_JR:.0f},{schatTotEle:.0f},{verschEle:.0f},"\
        f"{(verschEle * PRIJS_ELEKTRICITEIT):.0f},{PRIJS_ELEKTRICITEIT:.2f},0\n"\
        f"{SUM_VERBR_WAT_VRG_JR:.0f},{schatTotWat:.0f},{verschWat:.0f}"\
        f",{(verschWat * PRIJS_WATER):.0f},{PRIJS_WATER:.2f},0\n"\
        f"0,0,0,0,0,{MAANDBEDRAG:.0f}"

    # Schrijf csv-data naar bestand
    f = open("energie_hubrpi.csv", "w")
    f.write(string_csv_data)
    f.close()

rcParams['backend'] = 'Agg'
# Toon grafieken
maanden = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep",
           "okt", "nov", "dec"]
rcParams['axes.edgecolor'] = 'White'
rcParams['figure.figsize'] = [7.8, 3.8]
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['Nokia Sans']

def grafiek_gas():
    # Grafiek gasverbruik
    plotGas.figure()
    plotGas.plot(maanden, df['vrbr_gas_VrgJr2'], color='tab:cyan', label="Eerder",
                 linewidth=5, alpha=0.2, marker='o', ms=10)
    plotGas.plot(maanden, df['vrbr_gas_VrgJr'], color='tab:blue', label="2024",
                 linewidth=5, alpha=0.7, marker='o', ms=10)
    plotGas.plot(maanden, schatVerbrGas_HDG_JR, color='tab:orange',
                 label="2025", linewidth=5, marker='o', ms=10)
    plotGas.ylabel("verbruik (m3)", color='Black')
    plotGas.tick_params(colors='Black')
    plotGas.grid(color='Gray')
    plotGas.legend()
    plotGas.tight_layout()
    plotGas.savefig('gasverbruik.png', dpi=100, transparent=True)


def grafiek_elektriciteit():
    # Grafiek elektriciteitsverbruik
    plotEle.figure()
    plotEle.plot(maanden, df['vrbr_ele_VrgJr2'], color='tab:cyan', label="Eerder",
                 linewidth=5, alpha=0.2, marker='o', ms=10)
    plotEle.plot(maanden, df['vrbr_ele_VrgJr'], color='tab:blue', label="2024",
                 linewidth=5, alpha=0.7, marker='o', ms=10)
    plotEle.plot(maanden, schatVerbrEle_HDG_JR,
                 color='tab:orange', label="2025", linewidth=5, marker='o', ms=10)
    plotEle.ylabel("verbruik (kWh)", color='Black')
    plotEle.tick_params(colors='Black')
    plotEle.grid(color='Gray')
    plotEle.legend()
    plotEle.tight_layout()
    plotEle.savefig('elektriciteitsverbruik.png', dpi=100, transparent=True)


def grafiek_water():
    # Grafiek waterverbruik
    plotWat.figure()
    plotWat.plot(maanden, df['vrbr_wat_VrgJr2'], color='tab:cyan', label="Eerder",
                 linewidth=5, alpha=0.2, marker='o', ms=10)
    plotWat.plot(maanden, df['vrbr_wat_VrgJr'], color='tab:blue', label="2024",
                 linewidth=5, alpha=0.7, marker='o', ms=10)
    plotWat.plot(maanden, schatVerbrWat_HDG_JR, color='tab:orange',
                 label="2025", linewidth=5, marker='o', ms=10)
    plotWat.ylabel("verbruik (m3)", color='Black')
    plotWat.tick_params(colors='Black')
    plotWat.grid(color='Gray')
    plotWat.legend()
    plotWat.tight_layout()
    plotWat.savefig('waterverbruik.png', dpi=100, transparent=True)


p1 = Process(target=toon_overzicht)
p2 = Process(target=print_output)
p3 = Process(target=schrijf_csv_data)
p4 = Process(target=grafiek_gas)
p5 = Process(target=grafiek_elektriciteit)
p6 = Process(target=grafiek_water)
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

def schrijfCsvStats():
    uitvoer = "g,g-1,g-2,e,e-1,e-2,w,w-1,w-2\n"
    for i in range (0, 12):
        uitvoer += f"{schatVerbrGas_HDG_JR[i]:.0f},{TOT_VEBR_GAS_VRG_JR[i]:.0f},"\
                    f"{TOT_VEBR_GAS_VRG_JR2[i]:.0f},{schatVerbrEle_HDG_JR[i]:.0f},"\
                    f"{TOT_VEBR_ELE_VRG_JR[i]:.0f},{TOT_VEBR_ELE_VRG_JR2[i]:.0f},"\
                    f"{schatVerbrWat_HDG_JR[i]:.0f},{TOT_VEBR_WAT_VRG_JR[i]:.0f},"\
                    f"{TOT_VEBR_WAT_VRG_JR2[i]:.0f}\n"
        f = open("energie-stats.csv", "w")
        f.write(uitvoer)
        f.close()

schrijfCsvStats()
