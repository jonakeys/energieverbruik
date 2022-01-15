#
# energie_verbruik.py
#
# Programma om verbruik van energie (gas + elektriciteit) te meten en een
# schatting te maken voor het verdere verloop van het jaar.
# Er wordt gebruikgemaakt van graaddagen van drie voorgaande jaren en van het
# verbruik van het voorgaande jaar voor een zo realistisch mogelijke schatting.
#
# Jonathan van der Steege, januari 2022

import pandas as pd
import matplotlib.pyplot as plot_gas
import matplotlib.pyplot as plot_ele
from matplotlib import rcParams

# Inlezen data graaddagen, verbruik voorgaande jaar en afgeronde maanden
df = pd.read_csv('energiedata.csv')

totaal_verbruik_gas_2021 = df['vrbr_gas_2021']
totaal_verbruik_ele_2021 = df['vrbr_ele_2021']

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
# BEREKENINGEN SCHATTING VERBRUIK
#

# Combineer graaddagen en verbruik 2021 als basis voor verwachting
# verbruik komende jaar
combinatie_verbruik_gas = ((percentage_graaddagen +
                            percentage_verbruik_gas_2021_correctie) / 2)

# Combineer gemiddeld elektriciteit en verbruik 2021 als basis voor verwachting
combinatie_verbruik_elektriciteit = ((gemiddelde_elektriciteit +
                                      percentage_verbruik_elektriciteit_2021) / 2)

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
verbruik_elektriciteit = int(verbruik_elektriciteit)'''
maand = 0
dag_van_maand = 15
dagen_in_maand = 31
verbruik_gas = 102
verbruik_elektriciteit = 73

percentage_maand = dag_van_maand / dagen_in_maand
verbruik_gas_maand = (verbruik_gas / percentage_maand) - vast_gas_mnd
verbruik_elektriciteit_maand = verbruik_elektriciteit / percentage_maand
totaal_verbruik_gas = 0
totaal_verbruik_elektriciteit = 0

# Bereken schatting verbruik gas en elektriciteit voor 2022
schatting_verbruik_gas_2022 = [0] * 12
schatting_verbruik_elektriciteit_2022 = [0] * 12
verbruik_gas_2022 = 0
verbruik_elektriciteit_2022 = 0
# Als alleen eerste maand bekend is
if maand == 0:
    verbruik_gas_2022 = verbruik_gas_maand / combinatie_verbruik_gas[0]
    schatting_verbruik_gas_2022 = ((combinatie_verbruik_gas *
                                    verbruik_gas_2022) + vast_gas_mnd).round(2)
    verbruik_elektriciteit_2022 = (verbruik_elektriciteit_maand /
                                   combinatie_verbruik_elektriciteit[0])
    schatting_verbruik_elektriciteit_2022 = (combinatie_verbruik_elektriciteit *
                                             verbruik_elektriciteit_2022).round(2)
# Als een of meerdere maanden afgerond zijn
else:
    for i in range(0,maand):
        schatting_verbruik_gas_2022[i] = df['vrbr_gas_2022'][i]
        verbruik_gas_2022 += schatting_verbruik_gas_2022[i]
        schatting_verbruik_elektriciteit_2022[i] = df['vrbr_ele_2022'][i]
        verbruik_elektriciteit_2022 += schatting_verbruik_elektriciteit_2022[i]
    for i in range(maand, 12):
        schatting_verbruik_gas_2022[i] = ((verbruik_gas_maand /
                                          combinatie_verbruik_gas[maand]) *
                                          combinatie_verbruik_gas[i])
        verbruik_gas_2022 += schatting_verbruik_gas_2022[i]
        schatting_verbruik_elektriciteit_2022[i] = ((verbruik_elektriciteit_maand /
                                                     combinatie_verbruik_elektriciteit[maand]) *
                                                    combinatie_verbruik_elektriciteit[i])
        verbruik_elektriciteit_2022 += schatting_verbruik_elektriciteit_2022[i]

# Schatting totaal verbruik
schatting_totaal_gas = verbruik_gas_2022
schatting_totaal_elektriciteit = verbruik_elektriciteit_2022

# Bereken verschil 2021 - 2022
verschil_gas = (schatting_totaal_gas + vast_gas_jr) - sum_verbruik_gas_2021
verschil_elektriciteit = (schatting_totaal_elektriciteit -
                          sum_verbruik_elektriciteit_2021)

#
# WEERGEVEN DATA
#

prijs_gas = 1.43
prijs_elektriciteit = 0.47

# Toon overzicht, verbruik 2021 en schatting 2022
schema = {"maand": df['maand'],
          "vrbr_g_2021": totaal_verbruik_gas_2021,
          "vrw_g_2022": schatting_verbruik_gas_2022,
          "vrsch_gas": schatting_verbruik_gas_2022 - totaal_verbruik_gas_2021,
          "vrbr_e_2021": totaal_verbruik_ele_2021,
          "vrw_e_2022": schatting_verbruik_elektriciteit_2022,
          "vrsch_ele": (schatting_verbruik_elektriciteit_2022 -
                        totaal_verbruik_ele_2021)}
overzicht = pd.DataFrame(schema)
str_output = (str(overzicht) + "\n\n" + "2021\n" +
              ("\tVerbruik gas: %d m3\n" % sum_verbruik_gas_2021) +
              ("\tVerbruik elektriciteit: %d kWh\n\n" % sum_verbruik_elektriciteit_2021) +
              "2022\n" +
              ("\tGeschat gas: %d m3\n" % (schatting_totaal_gas + vast_gas_jr)) +
              ("\tGeschat elektriciteit: %d kWh\n\n" % schatting_totaal_elektriciteit) +
              "Verschil verbruik\n" +
              ("\tGas: %d m3 (EUR %d)\n" % (verschil_gas, (verschil_gas * prijs_gas))) +
              ("\tElektriciteit: %d kWh (EUR %d)\n" %
               (verschil_elektriciteit, (verschil_elektriciteit * prijs_elektriciteit))) +
              ("\tTarieven: [gas %.2f / m3] [elektriciteit %.2f / kWh]\n" %
               (prijs_gas, prijs_elektriciteit)))

# Toon uitvoer overzicht en totalen
print(str_output)

# Schrijf uitvoer naar bestand
f = open("energieverbruik_2022.txt", "w")
f.write(str_output)
f.close()

# Toon grafieken
maanden = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep",
           "okt", "nov", "dec"]
#plt.figure(facecolor="white")
rcParams['axes.edgecolor'] = 'White'
rcParams['figure.figsize'] = [7.9, 3.8]
#plot_gas = plt.subplot2grid((2, 1), (0, 0))
plot_gas.plot(maanden, schatting_verbruik_gas_2022, color='tab:orange', label="2022", linewidth=5)
plot_gas.plot(maanden, df['vrbr_gas_2021'], color='tab:blue', label="2021", linewidth=5)
#plot_gas.set_title("Gas", color='White')
#plot_gas.set_xlabel("maand", color='White')
#plot_gas.set_ylabel("verbruik (in m3)", color='White')
plot_gas.title("Gas", color='White')
plot_gas.xlabel("maand", color='White')
plot_gas.ylabel("verbruik (in m3)", color='White')
plot_gas.tick_params(colors='White')
plot_gas.grid()
plot_gas.legend()
#plot_gas.set_facecolor("grey")
plot_gas.tight_layout()
plot_gas.savefig('gasverbruik.png', dpi=100, transparent=True)
plot_gas.show()

#plot_ele = plt.subplot2grid((2, 1), (1, 0))
plot_ele.plot(maanden, schatting_verbruik_elektriciteit_2022, color='tab:orange', label="2022", linewidth=5)
plot_ele.plot(maanden, df['vrbr_ele_2021'], color='tab:blue', label="2021", linewidth=5)
#plot_ele.set_title("Elektriciteit", color='White')
#plot_ele.set_xlabel("maand", color='White')
#plot_ele.set_ylabel("verbruik (in kWh)", color='White')
plot_ele.title("Elektriciteit", color='White')
plot_ele.xlabel("maand", color='White')
plot_ele.ylabel("verbruik (in kWh)", color='White')
plot_ele.tick_params(colors='White')
plot_ele.grid()
plot_ele.legend()
#plot_ele.set_facecolor("grey")
plot_ele.tight_layout()
plot_ele.savefig('elektriciteitsverbruik.png', dpi=100, transparent=True)
plot_ele.show()
