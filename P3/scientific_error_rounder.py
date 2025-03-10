import numpy as np
import os
import csv
from decimal import Decimal, ROUND_HALF_UP, getcontext, InvalidOperation

def runden_und_speichern(pfad_zur_eingabedatei, suffix='rounded'):
    """
    Diese Funktion rundet Messwerte und zugehörige Fehler in einer CSV-Eingabedatei nach wissenschaftlichen 
    Kriterien und speichert die gerundeten Ergebnisse in einer neuen CSV-Datei.

    Parameter:
    - pfad_zur_eingabedatei (str): Pfad zur CSV-Datei mit den Eingabedaten. Die Daten sollten als Paare 
      von Messwert und Fehler organisiert sein.
    - suffix (str, optional): Suffix, das an den Namen der Ausgabedatei angehängt wird. Standard: 'rounded'.

    Beschreibung:
    - Die Funktion liest die CSV-Datei ein und interpretiert die Werte als Paare von 
      Messwerten und Fehlern.
    - Die erste Zeile wird immer als Kopfzeile behandelt.
    - Für jede Paarung wird der Messwert auf dieselbe Dezimalstelle wie der Fehler gerundet, 
      basierend auf den Regeln der wissenschaftlichen Notation.
    - Die gerundeten Daten werden in einer neuen CSV-Datei gespeichert, die im selben Verzeichnis wie 
      die Eingabedatei liegt und das angegebene Suffix enthält.

    Rückgabewert:
    - Speichert die gerundeten Daten in einer neuen CSV-Datei und gibt eine Erfolgsmeldung mit dem 
      Pfad zur Ausgabedatei aus.
    """

    # Erhöhen der Präzision, um Genauigkeitsverluste zu vermeiden
    getcontext().prec = 28

    def round_measurements(values, errors):
        """
        Rundet Messwerte und ihre Fehler wissenschaftlich korrekt.

        Parameter:
        - values (array-like): Liste der Messwerte als Decimal-Objekte.
        - errors (array-like): Liste der zugehörigen Fehler als Decimal-Objekte.

        Rückgabewert:
        - rounded_values: Liste der gerundeten Messwerte als Decimal-Objekte.
        - rounded_errors: Liste der gerundeten Fehler als Decimal-Objekte.
        - decimal_places_values: Anzahl der Dezimalstellen für jeden Wert.
        - decimal_places_errors: Anzahl der Dezimalstellen für jeden Fehler.
        """
        rounded_values = []
        rounded_errors = []
        decimal_places_values = []
        decimal_places_errors = []
        for val, err in zip(values, errors):
            val_dec = Decimal(val)
            err_dec = Decimal(err)
            if err_dec == 0:
                rounded_err = Decimal('0')
                rounded_val = val_dec
                dp_err = None
                dp_val = None
            else:
                # Exponent des Fehlers bestimmen
                exp_e = err_dec.normalize().adjusted()
                m = err_dec.scaleb(-exp_e)
                first_digit = int(m.to_integral_value(rounding=ROUND_HALF_UP))
                if first_digit in [1, 2]:
                    significant_digits = 2
                else:
                    significant_digits = 1
                exponent_LSD = exp_e - (significant_digits - 1)
                # Fehler aufrunden
                factor_err = Decimal('1e{}'.format(exponent_LSD))
                rounded_err = (err_dec / factor_err).to_integral_value(rounding=ROUND_HALF_UP) * factor_err
                # Bestimmen der Anzahl der Dezimalstellen für Fehler
                dp_err = max(-exponent_LSD, 0)
                dp_val = dp_err  # Der Wert wird auf die gleiche Stelle wie der Fehler gerundet
                # Quantisierungswert erstellen
                quantize_exp = Decimal('1e{}'.format(exponent_LSD))
                # Gerundeten Fehler und Wert quantisieren
                rounded_err = rounded_err.quantize(quantize_exp)
                rounded_val = val_dec.quantize(quantize_exp, rounding=ROUND_HALF_UP)
            rounded_values.append(rounded_val)
            rounded_errors.append(rounded_err)
            decimal_places_values.append(dp_val)
            decimal_places_errors.append(dp_err)
        return rounded_values, rounded_errors, decimal_places_values, decimal_places_errors

    # Pfad zur Eingabedatei
    input_file = pfad_zur_eingabedatei

    # Verzeichnis und Dateiname extrahieren
    directory, filename = os.path.split(input_file)
    name, ext = os.path.splitext(filename)

    # Pfad zur Ausgabedatei erstellen
    output_filename = f"{name}_{suffix}{ext}"
    output_file = os.path.join(directory, output_filename)

    # Überprüfen der Dateiendung und bei Bedarf korrigieren
    if ext.lower() != '.csv':
        print(f"Warnung: Die Eingabedatei hat nicht die Endung .csv. Ausgabedatei wird als {name}_{suffix}.csv gespeichert.")
        output_file = os.path.join(directory, f"{name}_{suffix}.csv")

    # CSV-Datei einlesen
    with open(input_file, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        lines = list(csv_reader)

    # Immer die erste Zeile als Kopfzeile behandeln
    if lines:
        header = lines[0]
        data_lines = lines[1:]
    else:
        header = []
        data_lines = []

    # Verarbeitung der Daten
    rounded_data = []
    for line in data_lines:
        if not any(line):  # Überspringe leere Zeilen
            continue
        
        # Bereinige die Werte von speziellen Zeichen wie Sternchen
        cleaned_values = []
        original_values = []
        for val in line:
            original_values.append(val)
            # Entferne Sonderzeichen wie Sternchen (*) und behalte nur numerische Werte
            cleaned_val = val.strip().replace('*', '').strip()
            if cleaned_val:
                cleaned_values.append(cleaned_val)
        
        # Konvertiere die bereinigten Werte in Decimal-Objekte
        decimal_values = []
        try:
            for val in cleaned_values:
                decimal_values.append(Decimal(val))
        except (InvalidOperation, ValueError) as e:
            print(f"Warnung: Konnte einen Wert nicht in Decimal konvertieren: {cleaned_values}. Fehler: {str(e)}")
            continue
        
        # Nehmen wir an, dass die Daten in Paaren von Wert und Fehler organisiert sind
        rounded_line = []
        if len(decimal_values) % 2 == 0:  # Überprüfe, ob die Anzahl der Werte gerade ist
            original_index = 0
            for i in range(0, len(decimal_values), 2):
                val = decimal_values[i]
                err = decimal_values[i+1]
                rounded_vals, rounded_errs, _, _ = round_measurements([val], [err])
                
                # Führe die Zeichen wie Sternchen wieder ein
                val_original = original_values[original_index]
                err_original = original_values[original_index + 1]
                
                val_prefix = ''.join([c for c in val_original if not (c.isdigit() or c == '.' or c == '-' or c == '+' or c == 'e' or c == 'E')])
                err_prefix = ''.join([c for c in err_original if not (c.isdigit() or c == '.' or c == '-' or c == '+' or c == 'e' or c == 'E')])
                
                # Füge die Präfixe zu den gerundeten Werten hinzu
                rounded_line.extend([val_prefix + str(rounded_vals[0]), err_prefix + str(rounded_errs[0])])
                original_index += 2
            
            rounded_data.append(rounded_line)
        else:
            print(f"Warnung: Zeile mit ungerader Anzahl von Werten übersprungen: {cleaned_values}")

    # Schreiben der gerundeten Daten in die Ausgabe-CSV-Datei
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Immer die Kopfzeile schreiben
        csv_writer.writerow(header)
        
        for rounded_line in rounded_data:
            csv_writer.writerow(rounded_line)

    print(f'Die gerundeten Daten wurden in der CSV-Datei "{output_file}" gespeichert.')