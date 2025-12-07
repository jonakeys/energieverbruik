#!/usr/bin/env python

# Definieer variabelen
graaddagen_vorig = 0
verbruik_vorig = 0
graaddagen_nu = 0
verbruik_nu = 0
ratio_graaddagen = 0
verwacht_verbruik = 0
verschil_verbruik = 0


# Invoer gebruiker voor data
def vraag_invoer():
    global graaddagen_vorig
    graaddagen_vorig = int(input("Graaddagen vorig jaar: "))
    global verbruik_vorig
    verbruik_vorig = int(input("Verbruik vorig jaar (m3): "))
    global graaddagen_nu
    graaddagen_nu = int(input("Graaddagen nu: "))
    global verbruik_nu
    verbruik_nu = int(input("Verbruik nu (m3): "))

# Bereken verhoudingen
def bereken_verhouding():
    global ratio_graaddagen
    global verwacht_verbruik
    global verschil_verbruik
    ratio_graaddagen = graaddagen_vorig / graaddagen_nu
    verwacht_verbruik = verbruik_vorig * ratio_graaddagen
    verschil_verbruik = verbruik_nu / verwacht_verbruik * 100

# Toon de uitvoer
def toon_uitvoer():
    print(f"Verwacht verbruik dit jaar is {verwacht_verbruik:.2f} m3\n"
          f"Werkelijk verbruik was {verbruik_nu} m3\n"
          f"Dus in verhouding {verschil_verbruik:.2f}% ({0-(100-verschil_verbruik):.0f}%)"
          )

def main():
    print("[hint] Bereken graaddagen hier: https://www.mindergas.nl/degree_days_calculation")
    vraag_invoer()
    bereken_verhouding()
    toon_uitvoer()

if __name__ == "__main__":
    main()
