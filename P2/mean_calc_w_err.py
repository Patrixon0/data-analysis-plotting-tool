import numpy as np

def err_weighted_mean(file_path, value_col=0, error_col=1, result_length=4):
    """
    Berechnet den gewichteten Mittelwert und den zugehörigen Fehler eines Wertearrays unter Berücksichtigung individueller Fehlerwerte.

    Parameter:
    - file_path (str): Der relative Pfad zu der zu mittelnden Datei.
    - value_col (int, optional): Index der Spalte mit den Werten (Standard: 0).
    - error_col (int, optional): Index der Spalte mit den Fehlern (Standard: 1).
    - result_length (int, optional): Anzahl der Nachkommastellen für die Ergebnisse (Standard: 4).

    Rückgabewert:
    - mean_val (float): Der berechnete gewichtete Mittelwert.
    - err_mean_val (float): Der Fehler des Mittelwerts.
    """
    # Datei einlesen
    data = np.loadtxt(file_path)

    # Werte und Fehler aus den angegebenen Spalten extrahieren
    val = data[:, value_col]  # Die Werte
    err_val = data[:, error_col]  # Die Fehler

    # Berechnung des Mittels und des Fehlers
    mean = mean_calc(val, err_val, 'data weighting')
    err_mean = mean_calc(val, err_val, 'error')

    # Rundung auf result_length Nachkommastellen
    mean_round = round(float(mean), result_length)
    err_mean_round = round(float(err_mean), result_length)
    
    return mean_round, err_mean_round


def mean_calc(z_input, err_input, goal='data weighting'):
    """
    Berechnet den gewichteten Mittelwert eines Wertearrays unter Berücksichtigung individueller Fehlerwerte.

    Parameter:
    - z_input (array_like): Array mit den zu gewichtenden Werten.
    - err_input (array_like): Array mit den Fehlern, die den Werten in z_input zugeordnet sind.
    - goal (str, optional): Bestimmt den Berechnungsmodus.
        - 'data weighting': Berechnet den gewichteten Mittelwert der Daten.
        - 'error': Berechnet den Fehler des Mittelwerts.
        Standardwert: 'data weighting'

    Rückgabewert:
    - mean_val (float): Der berechnete gewichtete Mittelwert oder der Fehler des Mittelwerts.
    """
    mean_1 = mean_2 = i = 0
    while i < len(z_input):
        mean_1 += (z_input[i] / err_input[i] ** 2)
        mean_2 += (1 / (err_input[i] ** 2))
        i += 1
    if goal == 'data weighting':
        mean_val = mean_1 / mean_2
    elif goal == 'error':
        mean_val = np.sqrt(1 / float(mean_2))
    return mean_val