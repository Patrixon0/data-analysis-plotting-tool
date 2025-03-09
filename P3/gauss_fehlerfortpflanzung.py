import sympy as sp
import numpy as np
import os
import csv
import pandas as pd

def gaussian_error_propagation(formula, variables, result_lenght=4, output=True, for_file=False):
    """
    Diese Funktion berechnet die Fehlerfortpflanzung nach der Gaußschen Methode basierend auf einer gegebenen Formel 
    und Variablen. Sie liefert sowohl die berechnete Fehlerformel als auch den numerischen Wert des Fehlers.

    Die Variablen werden als Tupel in der Form (Name, Wert, Fehler) übergeben. Wenn kein Fehler angegeben ist, 
    sollte (Name, Wert, 0) verwendet werden, um die Variable von der Ableitung auszuschließen.

    Parameter:
    - formula (sympy.Expr): Die mathematische Formel, deren Fehler berechnet werden soll.
    - variables (list of tuples): Liste der Variablen als Tupel (Name, Wert, Fehler).
    - result_lenght (int, optional): Anzahl der Dezimalstellen für die Rundung des Ergebnisses. Standard: 4.
    - output (bool, optional): Ob die Ergebnisse ausgegeben werden sollen. Standard: True.
    - for_file (bool, optional): Ob die Fehlerformel als String zurückgegeben werden soll. Standard: False.

    Rückgabewerte:
    - Bei `output=True`: Gibt die Formel, Werte, Fehlerformel und das Ergebnis (Wert ± Fehler) in der Konsole aus.
    - Bei `for_file=True`: Gibt die Fehlerformel als String zurück.
    - Bei `output=False` und `for_file=False`: Gibt das Ergebnis und den Fehler als Tuple (Wert, Fehler) zurück.
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



def evaluate_gaussian_error(file_path, formulas, variables, result_names, result_length=4, feedback=True, output_file_suffix='results'):
    """
    Diese Funktion automatisiert die Auswertung von Messdaten mit Gaußscher Fehlerfortpflanzung. 
    Sie berechnet für eine Liste von Formeln die entsprechenden Werte und Fehler für jeden Datenpunkt 
    in einer Datei und speichert die Ergebnisse in einer neuen Datei.

    Parameter:
    - file_path (str): Pfad zur Eingabedatei mit den Messdaten. Jede Variable sollte durch eine 
      Spalte für Werte und eine für Fehler repräsentiert werden.
    - formulas (list of sympy.Expr): Liste der Formeln, für die die Werte und Fehler berechnet werden sollen.
    - variables (list of sympy.Symbol): Liste der Variablen, die in den Formeln verwendet werden.
    - result_names (list of str): Liste der Namen der Ergebnisse für die Spaltenüberschriften der Ausgabedatei.
    - result_length (int, optional): Anzahl der Dezimalstellen für die Rundung der Ergebnisse. Standard: 4.
    - feedback (bool, optional): Wenn True, wird für jede Datenzeile der Fortschritt und die Ergebnisse in der Konsole ausgegeben. Standard: True.
    - output_file_suffix (str, optional): Suffix, das an den Namen der Ausgabedatei angehängt wird. Standard: 'results'.

    Rückgabewert:
    - Die Ergebnisse werden in einer neuen Datei im selben Verzeichnis wie die Eingabedatei gespeichert. 
      Die Datei enthält die berechneten Werte und Fehler für jede Formel und jeden Datenpunkt.

    Hinweise:
    - Die Funktion überprüft, ob die Anzahl der Formeln mit der Anzahl der Ergebnisnamen übereinstimmt.
    - Die Variablenwerte und ihre Fehler werden für jede Zeile der Eingabedatei extrahiert und für 
      die Berechnung der Fehlerfortpflanzung verwendet.
    - Die Ausgabedatei enthält einen Header mit den Namen der Ergebnisse und ihrer zugehörigen Fehler.
    """
    import pandas as pd


    if len(formulas) != len(result_names):
        raise ValueError("Die Anzahl der Formeln und Ergebnisnamen muss übereinstimmen.")
    
    if file_path.endswith('.csv'):
        # CSV-Datei mit Pandas laden
        df = pd.read_csv(file_path, delimiter=',', header=0)
        
        # Clean column names by removing asterisks if present
        df.columns = [col.replace('*', '') for col in df.columns]
        
        # Convert the dataframe to the format expected by the rest of the function
        # Create an array with [x, x_err, y1, y1_err, y2, y2_err, ...] structure
        x_col = df.columns[0]  # First column as x values
        x_err_col = df.columns[1]  # Second column as x error
        
        # Initialize with x and x_err columns
        data_array = np.column_stack((df[x_col].values, df[x_err_col].values))
        
        # Add each y and y_err column pair
        for i in range(2, len(df.columns), 2):
            if i+1 < len(df.columns):  # Ensure both y and y_err columns exist
                y_col = df.columns[i]
                y_err_col = df.columns[i+1]
                data_array = np.column_stack((data_array, df[y_col].values, df[y_err_col].values))
        
        data = data_array
    else:
        # Original code for space-separated files
        data = np.loadtxt(file_path, ndmin=1)
    
    # Initialisiere Ergebnisliste
    results = []
    
    l = len(data)
    num_formulas = len(formulas)
    
    # Variablen und ihre Fehler symbolisch als sympy Symbole
    err_vars = [sp.symbols(f'del_{var}') for var in variables]
    
    # Vor der ersten Schleife definieren
    var_values = {var: var for var in variables}
    var_errors = {var: sp.Symbol(f'del_{var}') for var in variables}

    # Berechne die partiellen Ableitungen für alle Formeln vorab
    partial_derivatives_list = []
    for formula in formulas:
        partial_derivatives = [sp.diff(formula, var) for var in variables]
        partial_derivatives_list.append(partial_derivatives)
        
        # für Formeloutput
        print(gaussian_error_propagation(
            formula,
            [(var, var_values[var], var_errors[var]) for var in variables],
            result_length,
            output=False,
            for_file=True
        ))


    
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
    output_file_name = f"{base_name}_{output_file_suffix}.csv"
    output_file_path = os.path.join(folder_path, output_file_name)
    
    # Erstelle den Header für die Ausgabedatei
    header = []
    for name in result_names:
        header.append(name)
        header.append(f"err_{name}")
    
    ## Schreibe den Header und die Ergebnisse in die Datei
    #with open(output_file_path, 'w') as f:
    #    # Schreibe den Header
    #    f.write(f"{header}\n")
    #    # Schreibe die Ergebnisse
    #    np.savetxt(f, results, fmt=f'%.{result_length}f', delimiter=' ')

    with open(output_file_path, 'w', newline='') as f:
        # Schreibe den Header
        csv.writer(f).writerow(header)
        # Schreibe die Ergebnisse
        csv.writer(f).writerows(results)


    # Gib eine Erfolgsnachricht aus
    print(f"Auswertung abgeschlossen. Ergebnisse wurden in '{output_file_path}' gespeichert.")
