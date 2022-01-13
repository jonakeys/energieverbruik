#
# energieverbruik.py
#
# Jonathan van der Steege
# januari 2022
#
# jonathan@jonakeys.nl
#


// BESCHRIJVING SCRIPT

Pythonscript om het energieverbruik van het vorige en huidige jaar te vergelijken. Ook kun je aan de hand van verbruik van dit jaar een schatting maken van het energieverbruik voor dit jaar.


// INSTALLEREN

Benodigd:
- python 3
- pandas (Python Data Analysis Library) - pandas.pydata.org
- matplotlib

Uitvoeren:
$ python energie_verbruik.py


// DATABESTAND
Voor invoer van data wordt het bestand 'energiedata.csv' gebruikt. Indeling van de velden:
- maand = naam van maand
- grddg_2019, = gegevens graaddagen van de jaren 2019-2021
	grddg_2020,
	grddg_2021
- vrbr_gas_2021	= gasverbruik van 2021
- gem_ele = weging verbruik elektriciteit per maand
- vrbr_ele_2021	= elektriciteitsverbruik 2021
- vrbr_gas_2022	= gasverbruik 2022 [handmatig invoer]
- vrbr_ele_2022	= elektriciteitsverbruik 2022 [handmatige invoer]


// GEBRUIKEN
In het bestand 'energiedata.csv' moet je de kolommen vrbr_gas_2021 en vrbr_ele_2021 invullen met eigen data van het afgelopen jaar.

Tijdens uitvoeren van het script wordt gevraagd om de maand (januari=0, december=11), dag van de maand, aantal dagen van de maand, verbruik gas en elektriciteit (van begin van de maand tot nu).

Het overzicht van de gegevens wordt getoond. Daarnaast wordt het naar het bestand 'energieverbruik_2022.txt' geschreven.

Er worden twee grafieken getoond. Eén met verbruik van gas en de andere van elektriciteit.
