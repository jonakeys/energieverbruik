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
import matplotlib.pyplot as plot_gas
import matplotlib.pyplot as plot_ele
import matplotlib.pyplot as plot_wat
from matplotlib import rcParams
from multiprocessing import Process


MAAND = 1
DAG_VAN_MAAND = 1
DAGEN_IN_MAAND = 28
VERBRUIK_GAS = 6
VERBRUIK_ELEKTRICITEIT = 5
VERBRUIK_WATER = 0.25
PRIJS_GAS = 1.43
PRIJS_ELEKTRICITEIT = 0.47
PRIJS_WATER = 1.021


# Inlezen data graaddagen, verbruik voorgaande jaar en afgeronde maanden
df = pd.read_csv('energiedata.csv')

totaal_verbruik_gas_2021 = df['vrbr_gas_2021']
totaal_verbruik_ele_2021 = df['vrbr_ele_2021']
totaal_verbruik_wat_2021 = df['vrbr_wat_2021']

#
# BEREKENINGEN GAS
#

# Vast verbruik gas per maand
# Bepaal aan de hand van zomerverbruik
sum_zomerverbruik = 0
for i in range(5, 9):
    sum_zomerverbruik += df['vrbr_gas_2021'][i]
vast_gas_mnd = sum_zomerverbruik / 4
vast_gas_jr = vast_gas_mnd*12

# Bereken gemiddelde graaddagen per maand voor afgelopen drie jaar
gemiddelde_graaddagen = ((df['grddg_2019'] + df['grddg_2020'] +
                          df['grddg_2021']) / 3).round(2)

# Bereken percentage verbruik per maand voor graaddagen
sum_graaddagen = 0
for i in gemiddelde_graaddagen:
    sum_graaddagen += i
percentage_graaddagen = (gemiddelde_graaddagen / sum_graaddagen).round(2)

# Bereken percentage verbruik per maand voor gasverbruik 2021
sum_verbruik_gas_2021 = 0
for i in totaal_verbruik_gas_2021:
    sum_verbruik_gas_2021 += i
percentage_verbruik_gas_2021 = (totaal_verbruik_gas_2021 /
                                sum_verbruik_gas_2021)

# Correctie verbruik gas 2021
correctie_verbruik_gas_2021 = totaal_verbruik_gas_2021 - vast_gas_mnd
sum_verbruik_gas_2021_correctie = 0
for i in correctie_verbruik_gas_2021:
    sum_verbruik_gas_2021_correctie += i
percentage_verbruik_gas_2021_correctie = (correctie_verbruik_gas_2021 /
                                          sum_verbruik_gas_2021_correctie)

#
# BEREKENINGEN ELEKTRICITEIT
#

# Gemiddelde verbruik elektriciteit voor een jaar
gemiddelde_elektriciteit = df['gem_ele']

# Bereken percentage verbruik per maand voor elektriciteitsverbruik 2021
sum_verbruik_elektriciteit_2021 = 0
for i in totaal_verbruik_ele_2021:
    sum_verbruik_elektriciteit_2021 += i
percentage_verbruik_elektriciteit_2021 = (totaal_verbruik_ele_2021 /
                                          sum_verbruik_elektriciteit_2021)

#
# BEREKENINGEN WATER
#
# Gemiddelde verbruik water voor een jaar
gemiddelde_water = df['gem_wat']

# Bereken percentage verbruik per maand voor waterverbruik 2021
sum_verbruik_water_2021 = 0
for i in totaal_verbruik_wat_2021:
    sum_verbruik_water_2021 += i
percentage_verbruik_water_2021 = (totaal_verbruik_wat_2021 /
                                  sum_verbruik_water_2021)

#
# BEREKENINGEN SCHATTING VERBRUIK
#

# Combineer graaddagen en verbruik 2021 als basis voor verwachting
# verbruik komende jaar
combinatie_verbruik_gas = ((percentage_graaddagen +
                            percentage_verbruik_gas_2021_correctie) / 2)

# Combineer gemiddeld elektriciteit en verbruik 2021 als basis voor verwachting
combinatie_verbruik_elektriciteit = ((gemiddelde_elektriciteit +
                                      percentage_verbruik_elektriciteit_2021) / 2)

# Combineer gemiddeld waterverbruik 2021 als basis voor verwachting
combinatie_verbruik_water = ((gemiddelde_water +
                              percentage_verbruik_water_2021) /2)

# Toevoegen nieuwe meetgegevens 2022
# maand 0=jan, 11=dec
#
# INVOEREN GEGEVENS HUIDIGE JAAR
#

print("Energieverbruik 2022")
'''maand = input("Welke maand (jan=0, dec=11)? ")
dag_van_maand = input("Welke dag? ")
dagen_in_maand = input("Hoeveel dagen in de maand? ")
verbruik_gas = input("Gasverbruik? ")
verbruik_elektriciteit = input("Elektriciteitsverbruik? ")
maand = int(maand)
dag_van_maand = int(dag_van_maand)
dagen_in_maand = int(dagen_in_maand)
verbruik_gas = int(verbruik_gas)
verbruik_elektriciteit = int(verbruik_elektriciteit)
maand = 0
dag_van_maand = 19
dagen_in_maand = 31
verbruik_gas = 128
verbruik_elektriciteit = 95'''

percentage_maand = DAG_VAN_MAAND / DAGEN_IN_MAAND
verbruik_gas_maand = (VERBRUIK_GAS / percentage_maand) - vast_gas_mnd
verbruik_elektriciteit_maand = VERBRUIK_ELEKTRICITEIT / percentage_maand
verbruik_water_maand = VERBRUIK_WATER / percentage_maand
totaal_verbruik_gas = 0
totaal_verbruik_elektriciteit = 0
totaal_verbruik_water = 0

# Bereken schatting verbruik gas en elektriciteit voor 2022
schatting_verbruik_gas_2022 = [0] * 12
schatting_verbruik_elektriciteit_2022 = [0] * 12
schatting_verbruik_water_2022 = [0] * 12
verbruik_gas_2022 = 0
verbruik_elektriciteit_2022 = 0
verbruik_water_2022 = 0

# Als alleen eerste maand bekend is
if MAAND == 0:
    verbruik_gas_2022 = verbruik_gas_maand / combinatie_verbruik_gas[0]
    schatting_verbruik_gas_2022 = ((combinatie_verbruik_gas *
                                    verbruik_gas_2022) + vast_gas_mnd).round(2)
    verbruik_elektriciteit_2022 = (verbruik_elektriciteit_maand /
                                   combinatie_verbruik_elektriciteit[0])
    schatting_verbruik_elektriciteit_2022 = (combinatie_verbruik_elektriciteit *
                                             verbruik_elektriciteit_2022).round(2)
    verbruik_water_2022 = verbruik_water_maand / combinatie_verbruik_water[0]
    schatting_verbruik_water_2022 = (combinatie_verbruik_water *
                                      verbruik_water_2022).round(2)

# Als een of meerdere maanden afgerond zijn
else:
    for i in range(0, MAAND):
        schatting_verbruik_gas_2022[i] = df['vrbr_gas_2022'][i]
        verbruik_gas_2022 += schatting_verbruik_gas_2022[i]
        schatting_verbruik_elektriciteit_2022[i] = df['vrbr_ele_2022'][i]
        verbruik_elektriciteit_2022 += schatting_verbruik_elektriciteit_2022[i]
        schatting_verbruik_water_2022[i] = df['vrbr_wat_2022'][i]
        verbruik_water_2022 += schatting_verbruik_water_2022[i]
    for i in range(MAAND, 12):
        schatting_verbruik_gas_2022[i] = ((verbruik_gas_maand /
                                          combinatie_verbruik_gas[MAAND]) *
                                          combinatie_verbruik_gas[i])
        verbruik_gas_2022 += schatting_verbruik_gas_2022[i]
        schatting_verbruik_elektriciteit_2022[i] = ((verbruik_elektriciteit_maand /
                                                     combinatie_verbruik_elektriciteit[MAAND]) *
                                                    combinatie_verbruik_elektriciteit[i])
        verbruik_elektriciteit_2022 += schatting_verbruik_elektriciteit_2022[i]
        schatting_verbruik_water_2022[i] = ((verbruik_water_maand /
                                             combinatie_verbruik_water[MAAND]) *
                                            combinatie_verbruik_water[i])

# Schatting totaal verbruik
schatting_totaal_gas = verbruik_gas_2022
schatting_totaal_elektriciteit = verbruik_elektriciteit_2022
schatting_totaal_water = verbruik_water_2022

# Bereken verschil 2021 - 2022
verschil_gas = (schatting_totaal_gas + vast_gas_jr) - sum_verbruik_gas_2021
verschil_elektriciteit = (schatting_totaal_elektriciteit -
                          sum_verbruik_elektriciteit_2021)
verschil_water = (schatting_totaal_water - sum_verbruik_water_2021)


#
# WEERGEVEN DATA
#
def ToonOverzicht():
    # Toon overzicht, verbruik 2021 en schatting 2022
    schema_g = {"maand": df['maand'],
                "vrbr_g_2021": totaal_verbruik_gas_2021,
                "vrw_g_2022": schatting_verbruik_gas_2022,
                "vrsch_gas": schatting_verbruik_gas_2022 - totaal_verbruik_gas_2021}
    schema_e = {"maand": df['maand'],
                "vrbr_e_2021": totaal_verbruik_ele_2021,
                "vrw_e_2022": schatting_verbruik_elektriciteit_2022,
                "vrsch_ele": (schatting_verbruik_elektriciteit_2022 -
                              totaal_verbruik_ele_2021)}
    schema_w = {"maand": df['maand'],
                "vrbr_w_2021": totaal_verbruik_wat_2021,
                "vrw_w_2022": schatting_verbruik_water_2022,
                "vrsch_wat": (schatting_verbruik_water_2022 -
                              totaal_verbruik_wat_2021)}
    overzicht_g = pd.DataFrame(schema_g)
    overzicht_e = pd.DataFrame(schema_e)
    overzicht_w = pd.DataFrame(schema_w)
    str_overzicht = "Gas\n{sch_g}\n\nElektriciteit\n{sch_e}\n\nWater\n{sch_w}\n\n".format(sch_g=overzicht_g,
                    sch_e=overzicht_e,
                    sch_w=overzicht_w)
    # Schrijf overzicht naar bestand
    f = open("energieverbruik_2022_overzicht.txt", "w")
    f.write(str_overzicht)
    f.close()


def PrintOutput():
    str_output = ("2021\n" +
                  ("\tVerbruik gas: %d m3\n" % sum_verbruik_gas_2021) +
                  ("\tVerbruik elektriciteit: %d kWh\n" % sum_verbruik_elektriciteit_2021) +
                  ("\tVerbruik water: %d m3\n" % sum_verbruik_water_2021) +
                  "2022\n" +
                  ("\tGeschat gas: %d m3\n" % (schatting_totaal_gas + vast_gas_jr)) +
                  ("\tGeschat elektriciteit: %d kWh\n" % schatting_totaal_elektriciteit) +
                  ("\tGeschat water: %d m3\n" % schatting_totaal_water) +
                  "Verschil verbruik\n" +
                  ("\tGas: %d m3 (EUR %d)\n" % (verschil_gas, (verschil_gas * PRIJS_GAS))) +
                  ("\tElektriciteit: %d kWh (EUR %d)\n" %
                   (verschil_elektriciteit, (verschil_elektriciteit * PRIJS_ELEKTRICITEIT))) +
                  ("\tWater: %d m3 (EUR %d)\n" % (verschil_water, (verschil_water * PRIJS_WATER))) +
                  ("\tTarieven: [gas %.2f / m3] [ele %.2f / kWh] [wat %.2f / m3]\n" %
                   (PRIJS_GAS, PRIJS_ELEKTRICITEIT, PRIJS_WATER)))
    # Toon uitvoer overzicht en totalen
    #print(str_overzicht)
    print(str_output)

    # Schrijf uitvoer naar bestand
    f = open("energieverbruik_2022.txt", "w")
    f.write(str_output)
    f.close()


def SchrijfCsvData():
    str_csv_data = ("vrbr_2021,sch_2022,vrsch_vrbr,vrsch_bedr,tar\n" +
                    str("%d" % sum_verbruik_gas_2021) +
                    str(",%d" % (schatting_totaal_gas + vast_gas_jr)) +
                    str(",%d" % verschil_gas) +
                    str(",%d" % (verschil_gas * PRIJS_GAS)) +
                    str(",%.2f\n" % PRIJS_GAS) +
                    str("%d" % sum_verbruik_elektriciteit_2021) +
                    str(",%d" % schatting_totaal_elektriciteit) +
                    str(",%d" % verschil_elektriciteit) +
                    str(",%d" % (verschil_elektriciteit * PRIJS_ELEKTRICITEIT)) +
                    str(",%.2f\n" % PRIJS_ELEKTRICITEIT) +
                    str("%d" % sum_verbruik_water_2021) +
                    str(",%d" % schatting_totaal_water) +
                    str(",%d" % verschil_water) +
                    str(",%d" % (verschil_water * PRIJS_WATER)) +
                    str(",%.2f\n" % PRIJS_WATER))

    # Schrijf csv-data naar bestand
    f = open("energie_hubrpi.csv", "w")
    f.write(str_csv_data)
    f.close()


# Toon grafieken
maanden = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep",
           "okt", "nov", "dec"]
rcParams['axes.edgecolor'] = 'White'
rcParams['figure.figsize'] = [7.8, 4.2]


def GrafiekGas():
    # Grafiek gasverbruik
    plot_gas.figure()
    plot_gas.plot(maanden, schatting_verbruik_gas_2022, color='tab:orange',
                  label="2022", linewidth=5)
    plot_gas.plot(maanden, df['vrbr_gas_2021'], color='tab:blue', label="2021",
                  linewidth=5)
    plot_gas.title("Gas", color='White')
    plot_gas.xlabel("maand", color='White')
    plot_gas.ylabel("verbruik (in m3)", color='White')
    plot_gas.tick_params(colors='White')
    plot_gas.ylim(bottom=0)
    plot_gas.grid()
    plot_gas.legend()
    plot_gas.tight_layout()
    plot_gas.savefig('gasverbruik.png', dpi=100, transparent=True)
    #plot_gas.show()


def GrafiekElektriciteit():
    # Grafiek elektriciteitsverbruik
    plot_ele.figure()
    plot_ele.plot(maanden, schatting_verbruik_elektriciteit_2022,
                  color='tab:orange', label="2022", linewidth=5)
    plot_ele.plot(maanden, df['vrbr_ele_2021'], color='tab:blue', label="2021",
                  linewidth=5)
    plot_ele.title("Elektriciteit", color='White')
    plot_ele.xlabel("maand", color='White')
    plot_ele.ylabel("verbruik (in kWh)", color='White')
    plot_ele.tick_params(colors='White')
    plot_ele.ylim(bottom=0)
    plot_ele.grid()
    plot_ele.legend()
    plot_ele.tight_layout()
    plot_ele.savefig('elektriciteitsverbruik.png', dpi=100, transparent=True)
    #plot_ele.show()


def GrafiekWater():
    # Grafiek waterverbruik
    plot_wat.figure()
    plot_wat.plot(maanden, schatting_verbruik_water_2022, color='tab:orange',
                  label="2022", linewidth=5)
    plot_wat.plot(maanden, df['vrbr_wat_2021'], color='tab:blue', label="2021",
                  linewidth=5)
    plot_wat.title("Water", color='White')
    plot_wat.xlabel("maand", color='White')
    plot_wat.ylabel("verbruik (in m3)", color='White')
    plot_wat.tick_params(colors='White')
    plot_wat.ylim(bottom=0)
    plot_wat.grid()
    plot_wat.legend()
    plot_wat.tight_layout()
    plot_wat.savefig('waterverbruik.png', dpi=100, transparent=True)
    #plot_ele.show()


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
