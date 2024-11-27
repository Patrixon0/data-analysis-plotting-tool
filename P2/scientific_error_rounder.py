import numpy as np
import os
from decimal import Decimal, ROUND_HALF_UP, getcontext

def runden_und_speichern(pfad_zur_eingabedatei, suffix='rounded'):
    """
    Rundet die Messwerte und Fehler in der angegebenen Datei und speichert sie in einer neuen Datei.

    Parameter:
    - pfad_zur_eingabedatei (str): Pfad zur Eingabedatei.
    - suffix (str, optional): Suffix für den Namen der Ausgabedatei (Default: 'rounded').

    Die Ausgabedatei wird im gleichen Verzeichnis wie die Eingabedatei gespeichert
    und erhält den Namen 'Dateiname_suffix.txt'.
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

    # Lesen der Daten aus der Eingabedatei
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Überprüfen, ob die erste Zeile eine Kopfzeile ist
    header = ''
    if lines[0].startswith('#'):
        header = lines[0]
        data_lines = lines[1:]
    else:
        data_lines = lines

    # Verarbeitung der Daten
    rounded_data = []
    decimal_places_data = []
    for line in data_lines:
        if line.strip() == '':
            continue  # Überspringe leere Zeilen
        values = line.strip().split()
        # Konvertiere Werte in Decimal-Objekte
        values = [Decimal(val) for val in values]
        # Nehmen wir an, dass die Daten in Paaren von Wert und Fehler organisiert sind
        rounded_line = []
        decimal_places_line = []
        for i in range(0, len(values), 2):
            val = values[i]
            err = values[i+1]
            rounded_vals, rounded_errs, dp_vals, dp_errs = round_measurements([val], [err])
            rounded_line.extend([rounded_vals[0], rounded_errs[0]])
            decimal_places_line.extend([dp_vals[0], dp_errs[0]])
        rounded_data.append(rounded_line)
        decimal_places_data.append(decimal_places_line)

    # Schreiben der gerundeten Daten in die Ausgabedatei
    with open(output_file, 'w') as f:
        if header:
            f.write(header)
        for rounded_line, decimal_places_line in zip(rounded_data, decimal_places_data):
            formatted_numbers = []
            for val, dp in zip(rounded_line, decimal_places_line):
                if dp is None:
                    val_str = str(val)
                else:
                    # Verwende quantize, um die gewünschte Anzahl von Dezimalstellen zu erzwingen
                    format_str = Decimal('1e-{0}'.format(dp))
                    val_quantized = val.quantize(format_str)
                    val_str = format(val_quantized, 'f')
                formatted_numbers.append(val_str)
            rounded_line_str = ' '.join(formatted_numbers)
            f.write(rounded_line_str + '\n')

    print(f'Die gerundeten Daten wurden in der Datei "{output_file}" gespeichert.')
