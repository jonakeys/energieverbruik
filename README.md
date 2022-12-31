
energieverbruik.py

Jonathan van der Steege
januari 2022


## BESCHRIJVING SCRIPT

Pythonscript om het energieverbruik van het vorige en huidige jaar te vergelijken. Ook kun je aan de hand van verbruik van dit jaar een schatting maken van het energieverbruik voor dit jaar.


## INSTALLEREN

Benodigd:
- python 3
- pandas (Python Data Analysis Library) - pandas.pydata.org
- matplotlib

Uitvoeren:
$ python energie_verbruik.py


## DATABESTAND 'ENERGIEDATA.CSV'
Voor invoer van data wordt het bestand 'energiedata.csv' gebruikt. Indeling van de velden:
- maand = naam van maand
- grddg_2019, grddg_2020, grddg_2021, grddg_2022 = gegevens graaddagen van de jaren 2019-2022	
- vrbr_gas_VrgJr	= gasverbruik van vorig jaar
- gem_ele = weging verbruik elektriciteit per maand
- vrbr_ele_VrgJr	= elektriciteitsverbruik vorig jaar
- vrbr_gas_HdgJr	= gasverbruik huidig jaar [handmatig invoer]
- vrbr_ele_HdgJr	= elektriciteitsverbruik huidig jaar [handmatige invoer]
- gem_wat = percentage waterverbruik per maand
- vrbr_wat_VrgJr = waterverbruik vorig jaar
- vrbr_wat_HdgJr = waterverbruik huidig jaar [handmatig invoer]


## UITVOER 'ENERGIE_HUBRPI.CSV'
Uitvoer van data naar dit bestand voor gebruik in het hub-programma voor de RPi.
De rijen bevatten respectievelijk data voor gas, elektriciteit en water.
- vrbr_VrgJr = totaalverbruik vorig jaar
- sch_HdgJr = schatting verbruik huidig jaar
- vrsch_vrbr = verschil verbruik vorig jaar - huidig jaar
- vrsch_bedr = verschil bedrag vorig jaar - huidig jaar
- tar = tarieven (per m3 of kWh)


## GEBRUIKEN
In het bestand 'energiedata.csv' moet je de kolommen vrbr_gas_VrgJr, vrbr_ele_VrgJr en vrbr_wat_VrgJr invullen met eigen data van het afgelopen jaar.

Tijdens uitvoeren van het script wordt gevraagd om de maand (jan tot dec), dag van de maand, aantal dagen van de maand, verbruik gas, elektriciteit en water (van begin van de maand tot nu).

Het overzicht van de gegevens wordt getoond. Daarnaast wordt het naar het bestand 'energieverbruik_HdgJr.txt' geschreven.

Er worden drie grafieken getoond. Eén met verbruik van gas, de tweede van elektriciteit en de derde van water.
