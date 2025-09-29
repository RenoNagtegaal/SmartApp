# Bestandsnamen vast ingesteld
INPUT_FILE = "invoer.txt"
OUTPUT_FILE = "uitvoer.txt"

def fahrenheit(temp_celcius: float) -> float:
    """Bereken temperatuur in Fahrenheit."""
    # Formule: F = 32 + 1.8 * C
    return 32 + 1.8 * temp_celcius


def gevoelstemperatuur(temp_celcius: float, windsnelheid: float, luchtvochtigheid: int) -> float:
    """Bereken gevoelstemperatuur volgens de formule."""
    # Formule: gevoelstemperatuur = temp_celcius - (luchtvochtigheid / 100) * windsnelheid
    return temp_celcius - (luchtvochtigheid / 100) * windsnelheid


def weerrapport(temp_celcius: float, windsnelheid: float, luchtvochtigheid: int) -> str:
    """Genereer een weerrapport op basis van beslisregels."""
    # Eerst de gevoelstemperatuur berekenen
    gevoel = gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid)

    # Beslisregels op basis van gevoelstemperatuur en windsnelheid
    if gevoel < 0 and windsnelheid > 10:
        return "Het is heel koud en het stormt! Verwarming helemaal aan!"
    elif gevoel < 0 and windsnelheid <= 10:
        return "Het is behoorlijk koud! Verwarming mag aan!"
    elif 0 <= gevoel < 10 and windsnelheid > 12:
        return "Het is best koud en het waait; Verwarming aan!"
    elif 0 <= gevoel < 10 and windsnelheid <= 12:
        return "Het is een beetje koud, Verwarming hoeft niet aan!"
    elif 10 <= gevoel < 22:
        return "Heerlijk weer, niet te koud of te warm."
    else:
        return "Warm! AC aan!"


def weerstation():
    """Hoofdprogramma: vraagt input en toont per dag resultaten."""
    # Lijst om alle ingevoerde temperaturen (in Celsius) op te slaan
    temperaturen = []

    # Max 7 dagen invoer
    for dag in range(1, 8):
        # --- Invoer temperatuur ---
        temp_in = input(f"Wat is op dag {dag} de temperatuur[C]: ")
        if temp_in.strip() == "":
            # Stop direct bij lege invoer
            break
        try:
            temp_c = float(temp_in)
        except ValueError:
            print("Ongeldige invoer voor temperatuur, probeer opnieuw.")
            continue

        # --- Invoer windsnelheid ---
        wind_in = input(f"Wat is op dag {dag} de windsnelheid[m/s]: ")
        if wind_in.strip() == "":
            break
        try:
            wind = float(wind_in)
        except ValueError:
            print("Ongeldige invoer voor windsnelheid, probeer opnieuw.")
            continue

        # --- Invoer luchtvochtigheid ---
        vocht_in = input(f"Wat is op dag {dag} de vochtigheid[%]: ")
        if vocht_in.strip() == "":
            break
        try:
            vocht = int(vocht_in)
            # Moet tussen 0 en 100 liggen
            if not (0 <= vocht <= 100):
                raise ValueError
        except ValueError:
            print("Ongeldige invoer voor vochtigheid, geef een geheel getal tussen 0 en 100.")
            continue



        def aantal_dagen(inputFile: str) -> int:
            """Lees het inputbestand en tel het aantal dagen (excl. header)."""
            try:
                with open(inputFile, "r") as f:
                    regels = f.readlines()
                return len(regels) - 1  # Eerste regel is header
            except FileNotFoundError:
                print(f"Bestand {inputFile} niet gevonden.")
                return 0

        def auto_bereken(inputFile: str, outputFile: str) -> None:
            """Lees invoerbestand, bereken actuatorwaarden en schrijf naar uitvoerbestand."""
            try:
                with open(inputFile, "r") as f:
                    regels = f.readlines()
            except FileNotFoundError:
                print(f"Bestand {inputFile} niet gevonden.")
                return

            data_regels = regels[1:]  # sla de header over

            with open(outputFile, "w") as out:
                for regel in data_regels:
                    velden = regel.strip().split(";")
                    if len(velden) != 5:
                        continue
                    datum, personen, setpoint, buiten, neerslag = velden
                    personen = int(personen)
                    setpoint = float(setpoint)
                    buiten = float(buiten)
                    neerslag = float(neerslag)

                    # CV-ketel berekenen
                    verschil = setpoint - buiten
                    if verschil >= 20:
                        cv = 100
                    elif verschil >= 10:
                        cv = 50
                    else:
                        cv = 0

                    # Ventilatie berekenen
                    ventilatie = min(personen + 1, 4)

                    # Bewatering berekenen
                    bewatering = "True" if neerslag < 3 else "False"

                    out.write(f"{datum};{cv};{ventilatie};{bewatering}\n")

            print(f"Uitvoerbestand '{outputFile}' is bijgewerkt.")

        def overwrite_settings(outputFile: str) -> int:
            """Laat gebruiker actuatorwaarde overschrijven voor een bepaalde datum."""

            datum = input("Voer de datum in (dd-mm-jjjj): ").strip()
            systeem = input("Kies systeem (1=CV ketel, 2=Ventilatie, 3=Bewatering): ").strip()
            nieuwe_waarde = input("Nieuwe waarde: ").strip()


            if systeem not in {"1", "2", "3"}:
                print("Ongeldig systeem gekozen.")
                return -3

            with open(outputFile, "r") as f:
                regels = f.readlines()

            aangepast = False
            nieuwe_regels = []
            for regel in regels:
                velden = regel.strip().split(";")
                if len(velden) != 4:
                    nieuwe_regels.append(regel)
                    continue

                r_datum, cv, ventilatie, bewatering = velden
                if r_datum != datum:
                    nieuwe_regels.append(regel)
                    continue



                # Overschrijven per systeem
                if systeem == "1":  # CV-ketel
                    try:
                        waarde = int(nieuwe_waarde)
                        if 0 <= waarde <= 100:
                            cv = str(waarde)
                        else:
                            print("Ongeldige waarde voor CV ketel (0-100).")
                            return -3
                    except ValueError:
                        print("Geen geldig getal voor CV ketel.")
                        return -3

                elif systeem == "2":  # Ventilatie
                    try:
                        waarde = int(nieuwe_waarde)
                        if 0 <= waarde <= 4:
                            ventilatie = str(waarde)
                        else:
                            print("Ongeldige waarde voor ventilatie (0-4).")
                            return -3
                    except ValueError:
                        print("Geen geldig getal voor ventilatie.")
                        return -3

                elif systeem == "3":  # Bewatering
                    if nieuwe_waarde not in {"0", "1"}:
                        print("Ongeldige waarde voor bewatering (0=uit,1=aan).")
                        return -3
                    bewatering = "True" if nieuwe_waarde == "1" else "False"

                nieuwe_regels.append(f"{r_datum};{cv};{ventilatie};{bewatering}\n")
                aangepast = True

            if not aangepast:
                print("Datum niet gevonden.")
                return -1

            with open(outputFile, "w") as f:
                f.writelines(nieuwe_regels)

            print("Waarde succesvol aangepast.")
            return 0

        def smart_app_controller():
            """Menu om de smart app te bedienen."""
            while True:
                print("\n--- SMART APP MENU ---")
                print("1. Aantal dagen weergeven")
                print("2. Autobereken en uitvoerbestand schrijven")
                print("3. Waarde overschrijven in uitvoerbestand")
                print("4. Stoppen")

                keuze = input("Maak een keuze: ").strip()

                if keuze == "1":
                    dagen = aantal_dagen(INPUT_FILE)
                    print(f"Aantal dagen in bestand: {dagen}")

                elif keuze == "2":
                    auto_bereken(INPUT_FILE, OUTPUT_FILE)

                elif keuze == "3":
                    overwrite_settings(OUTPUT_FILE)

                elif keuze == "4":
                    print("Programma gestopt.")
                    break

                else:
                    print("Ongeldige keuze, probeer opnieuw.")

        # Start applicatie
        if __name__ == "__main__":
            smart_app_controller()

        # --- Opslaan en berekenen ---
        temperaturen.append(temp_c)                     # Toevoegen aan lijst
        temp_f = fahrenheit(temp_c)                     # Omrekenen naar Fahrenheit
        rapport = weerrapport(temp_c, wind, vocht)      # Weerrapport genereren
        gemiddelde = sum(temperaturen) / len(temperaturen)  # Gemiddelde temp berekenen
        gevoel = gevoelstemperatuur(temp_c, wind, vocht)  # Gevoels temp berekenen

        # --- Uitvoer per dag ---
        print(f"Het is {temp_c:.1f}C ({temp_f:.1f}F)")
        print(rapport)
        print(f"Gem. temp tot nu toe is {gemiddelde:.1f}")
        print("Gevoelstemperatuur:", gevoel)
        print("=" * 38)  # Scheidingslijn



# Start het programma als dit bestand direct uitgevoerd wordt
if __name__ == "__main__":
    weerstation()
