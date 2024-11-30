import numpy as np

def err_weighted_mean(file_path):
    """
    Berechnet den gewichteten Mittelwert und zugehoerigen Fehler eines Wertearrays unter Berücksichtigung individueller Fehlerwerte.

    Parameter:
    file_path: Der relative Pfad zu der zu Mittelnden Datei

    Rückgabewert:
    - mean_val (float): Der berechnete gewichtete Mittelwert
    - err_mean_val (float): Der Fehler des Mittelwerts
    """

    # Datei einlesen
    data = np.loadtxt(file_path)

    # Werte extrahieren
    val = data[:, 0]  # Die Werte
    err_val = data[:, 1]  # Die Fehler

    return(mean_calc(val, err_val, 'data weighting'), mean_calc(val, err_val, 'error'))


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
    if goal == 'error':
        mean_val = np.sqrt(1 / mean_2)
    return mean_val