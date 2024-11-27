import sympy as sp
import numpy as np
import os

def evaluate_gaussian_error(file_path, formulas, variables, result_names, result_length=4, feedback=True, output_file_suffix='results'):
    """
    Funktion zur automatischen Auswertung von Messdaten mit Gaußscher Fehlerfortpflanzung.
    Speichert Ergebnisse als Datei mit dem ursprünglichen Dateinamen plus dem angegebenen Suffix im selben Verzeichnis.
    
    Parameter:
    - file_path: Pfad zur Datei mit den Messdaten.
    - formulas: Liste von sympy-Formeln, auf die die Daten angewendet werden sollen.
    - variables: Liste der sympy-Variablennamen, z.B. [x, y, z].
    - result_names: Liste der Ergebnisvariablen für den Header der Ausgabedatei.
    - result_length: Anzahl der Dezimalstellen zur Rundung der Ergebnisse (default=4).
    - feedback: Wenn True, wird der Output für jede Zeile ausgegeben (default=True).
    - output_file_suffix: Suffix, das an den Dateinamen der Eingabedatei angehängt wird (default='results').
    """
    
    # Überprüfen, ob die Anzahl der Formeln und Ergebnisnamen übereinstimmt
    if len(formulas) != len(result_names):
        raise ValueError("Die Anzahl der Formeln und Ergebnisnamen muss übereinstimmen.")
    
    # Lade die Daten aus der Datei. Gehe davon aus, dass jede Variable eine Spalte für Werte und eine für Fehler hat
    data = np.loadtxt(file_path, usecols=range(len(variables) * 2), ndmin=1)
    
    # Initialisiere Ergebnisliste
    results = []
    
    l = len(data)
    num_formulas = len(formulas)
    
    # Variablen und ihre Fehler symbolisch als sympy Symbole
    err_vars = [sp.symbols(f'del_{var}') for var in variables]
    
    # Berechne die partiellen Ableitungen für alle Formeln vorab
    partial_derivatives_list = []
    for formula in formulas:
        partial_derivatives = [sp.diff(formula, var) for var in variables]
        partial_derivatives_list.append(partial_derivatives)
    
    # Iteriere über jede Zeile der Datei (jeder Zeile entsprechen Werte und Fehler für alle Variablen)
    for i in range(l):
        var_values = {}
        var_errors = {}
        
        # Extrahiere die Werte und Fehler für jede Variable aus der Datei
        for j, var in enumerate(variables):
            value = data[i, 2 * j]        # Wert
            error = data[i, 2 * j + 1]    # Fehler
            var_values[var] = value
            var_errors[var] = error
        
        row_results = []
        
        # Wende die Gaußsche Fehlerfortpflanzung für jede Formel an
        for k in range(num_formulas):
            formula = formulas[k]
            partial_derivatives = partial_derivatives_list[k]
            # Berechne den Funktionswert
            func_value = formula.evalf(subs=var_values)
            # Berechne den Fehler nach der Gaußschen Fehlerfortpflanzung
            squared_errors = []
            for pd, var in zip(partial_derivatives, variables):
                pd_value = pd.evalf(subs=var_values)
                error = var_errors[var]
                squared_errors.append((pd_value * error) ** 2)
            error_value = sp.sqrt(sum(squared_errors)).evalf()
            # Runde das Ergebnis
            func_value = round(float(func_value), result_length)
            error_value = round(float(error_value), result_length)
            # Füge das Ergebnis der Zeile hinzu
            row_results.extend([func_value, error_value])
        
        results.append(row_results)
        
        # Ausgabe für den Nutzer (optional)
        if feedback:
            print(f"Zeile {i+1}: {row_results}")
    
    # Ermittle den Ordner und den Dateinamen ohne die Dateiendung der ursprünglichen Datei
    folder_path = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Erstelle den Ausgabedateinamen durch Anhängen des Suffixes
    output_file_name = f"{base_name}_{output_file_suffix}.txt"
    output_file_path = os.path.join(folder_path, output_file_name)
    
    # Erstelle den Header für die Ausgabedatei
    header_items = []
    for name in result_names:
        header_items.extend([name, f"err_{name}"])
    # Anpassung: Keine Leerzeichen nach '#' und Leerzeichen als Trennzeichen
    header = '#' + ' '.join(header_items)
    
    # Speichere die Ergebnisse in der Datei im gleichen Ordner wie die ursprüngliche Datei
    np.savetxt(output_file_path, results, fmt=f'%.{result_length}f', header=header, delimiter=' ')
    
    # Gib eine Erfolgsnachricht aus
    print(f"Auswertung abgeschlossen. Ergebnisse wurden in '{output_file_path}' gespeichert.")
