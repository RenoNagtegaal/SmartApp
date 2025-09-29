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
