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

            # für Formeloutput
            gaussian_error_propagation(formula, [(var, var_values.get(var, 0), var_errors.get(var, 0)) for var in variables], result_length, output=True, for_file=True)

        
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
    ####################################################################################################
    gaussian_error_propagation(formula, [(var, var_values.get(var, 0), var_errors.get(var, 0)) for var in variables], result_length, output=True, for_file=True)

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


def gaussian_error_propagation(formula, variables, result_lenght=4, output=True, for_file=False):
    """
    Berechnet die Fehlerfortpflanzung nach der Gaußschen Methode und gibt die
    verwendete Formel sowie das Ergebnis aus.
    
    Variablen werden in der Form (Name, Wert, Fehler) notiert bzw. (Name, Wert, 0) falls
    nicht nach ihnen abgeleitet werden soll.
    
    Parameter result_lenght passt die Rundungslänge des Ergebnisses an.
    """
    # create lists of variable names for later usage
    names = [var[0] for var in variables]
    err_names = [sp.symbols(f'del_{var[0]}') for var in variables]
    diff_functions, error_sums_n, error_sums_v =np.empty(0), np.empty(0), np.empty(0)
    val_dict={var[0]: var[1] for var in variables}
    
    # calculate formula value
    formula_value = formula.subs(val_dict).evalf()
    
    # differentiate function by each variable and make the sums both as strings as well as value
    i=0
    while i<len(names):
        diff_functions=np.append(diff_functions,sp.diff(formula, names[i]))
        if variables[i][2]!=0:
            error_sums_n=np.append(error_sums_n,diff_functions[i]*err_names[i])
        error_sums_v=np.append(error_sums_v,(diff_functions[i]*variables[i][2])**2)
        i+=1
    
    # create final formula as a string
    sum_str = [f'({str(sum_n)})**2' for sum_n in error_sums_n]
    result_str = ' + '.join(sum_str)
    error_formula=f'sqrt({result_str})'
    
    # calculate error value
    error_result=sp.sqrt(sum([expr.subs(val_dict).evalf() for expr in error_sums_v]))
    
    if for_file:
        return(error_formula)

    # print output
    if output:
        print(f'Formel: {formula}\nWerte: {variables} \n\nFormelwert: {formula_value}\n')
        print(f'Fehlerformel: {error_formula}')
        print(f'Fehler: {error_result} \nErgebnis: {round(formula_value,result_lenght)}±{round(error_result,result_lenght)}')
        return(None)
    else:
        return(formula_value, error_result)