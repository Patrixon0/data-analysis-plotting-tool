import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, ScalarFormatter, FuncFormatter
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP, getcontext

def round_measurement(value, error):
    """
    Rundet einen Messwert und seinen Fehler wissenschaftlich korrekt.

    Parameter:
    - value (float): Messwert.
    - error (float): Fehler des Messwerts.

    Rückgabewert:
    - rounded_value_str (str): Gerundeter Messwert als String.
    - rounded_error_str (str): Gerundeter Fehler als String.
    """
    getcontext().prec = 28
    val_dec = Decimal(str(value))
    err_dec = Decimal(str(error))

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

    # Formatierung, um nachgestellte Nullen zu erhalten
    if dp_val is not None:
        rounded_value_str = f"{rounded_val:.{dp_val}f}"
    else:
        rounded_value_str = str(rounded_val)

    if dp_err is not None:
        rounded_error_str = f"{rounded_err:.{dp_err}f}"

    else:
        rounded_error_str = str(rounded_err)

    return rounded_value_str, rounded_error_str


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

    weights = np.square(1 / err_input)
    
    if goal == 'data weighting':
        return np.sum(z_input * weights) / np.sum(weights)
        # Anhang A1.26
    elif goal == 'error': 
        return np.sqrt(len(weights) / np.sum(weights))
        # Der Return-Wert ist eine approximierte Unsicherheit, die so nicht direkt so in der 
        # Formel steht, aber in der Praxis gut funktioniert. Anhang A1.27
    else:
        raise ValueError("Ungültiges Ziel für mean_calc. Nutze 'data weighting' oder 'error'.")

from geraden_fit_config import config_1
def geraden_fit(file_n, config=config_1, **kwargs):
    """
    Diese Funktion ermöglicht die Darstellung von Messdaten mit Fehlerbalken und optionaler linearer Regression.
    Sie unterstützt mehrere Datensätze und bietet vielfältige Anpassungsmöglichkeiten für die Visualisierung.
    
    Rückgabewert:
    - Ein Plot der Messdaten mit Fehlerbalken, optionalen Regressionslinien und weiteren Visualisierungen.
    - Relevante Daten und Ergebnisse werden auch in der Konsole ausgegeben.

    Args:
        file_n: Path to the data file
        config: A GeradeConfig object containing all parameter settings
        **kwargs: Individual parameter settings that override config values

    Possible parameters:
    - title (str, optional): Titel des Plots. Standard: 'unnamed'.
    - x_label (str, optional): Beschriftung der X-Achse. Standard: 'X-Achse'.
    - y_label (str, optional): Beschriftung der Y-Achse. Standard: 'Y-Achse'.
    - save (bool, optional): Ob der Plot gespeichert werden soll. Standard: False.
    - linear_fit (bool, optional): Ob eine lineare Regression durchgeführt wird. Standard: False.
    - focus_point (bool, optional): Ob der Schwerpunkt mit Fehlerbalken dargestellt wird. Standard: False.
    - plot_y_inter (bool, optional): Ob der Y-Achsenabschnitt angezeigt wird. Standard: False.
    - plot_x_inter (bool, optional): Ob der X-Achsenabschnitt angezeigt wird. Standard: False.
    - y_inter_label (str, optional): Label für den Y-Achsenabschnitt. Standard: None.
    - x_inter_label (str, optional): Label für den X-Achsenabschnitt. Standard: None.
    - Ursprungsgerade (float, optional): Erstellt Ursprungsgerade mit Steigung Ursprungsgerade. Standard: None.
    - Ursprungsgerade_title (str,optional): Bennenug der Ursprungsgeraden in der Legende. Standart: Ursprungsgerade
    - plot_errors (bool, optional): Ob Fehler auch geplotted werden. Standard: True.
    - x_axis (float, optional): Position der horizontalen Linie bei y=0. Standard: 0.
    - y_axis (float, optional): Position der vertikalen Linie bei x=0. Standard: 0.
    - x_major_ticks (float, optional): Abstand zwischen den Hauptticks der X-Achse. Standard: None.
    - x_minor_ticks (float, optional): Abstand zwischen den Nebenticks der X-Achse. Standard: None.
    - y_major_ticks (float, optional): Abstand zwischen den Hauptticks der Y-Achse. Standard: None.
    - y_minor_ticks (float, optional): Abstand zwischen den Nebenticks der Y-Achse. Standard: None.
    - legendlocation (str, optional): Position der Legende. Standard: 'best'.
    - y_labels (list, optional): Bezeichnungen für die Y-Datensätze. Standard: None.
    - y_markers (list, optional): Marker für die einzelnen Datensätze. Standard: None.
    - y_colors (list, optional): Farben für die einzelnen Datensätze. Standard: None.
    - x_decimal_places (int, optional): Anzahl der Dezimalstellen auf der X-Achse. Standard: 1.
    - y_decimal_places (int, optional): Anzahl der Dezimalstellen auf der Y-Achse. Standard: 1.
    - scientific_limits (tuple, optional): Grenzen für wissenschaftliche Notation. Standard: (-3,3).
    - custom_datavol_limiter (int, optional): Begrenzung der Anzahl der Datenpunkte. Standard: 0 (keine Begrenzung).
    - x_shift (float, optional): Horizontaler Offset für die X-Daten. Standard: 0.
    - y_shift (float, optional): Vertikaler Offset für die Y-Daten. Standard: 0.
    - length (float, optional): Länge der Abbildung in Zoll. Standard: 15.
    - height (float, optional): Höhe der Abbildung in Zoll. Standard: 5.
    - size (float, optional): Größe der Marker. Standard: 1.
    - delimiter (str, optional): Trennzeichen für CSV-Dateien. Standard: ','.
    - y_max (float, optional): Obere Begrenzung der Y-Achse. Standard: None (keine Begrenzung).
    - y_min (float, optional): Untere Begrenzung der Y-Achse. Standard: None (keine Begrenzung).
    - x_max (float, optional): Obere Begrenzung der X-Achse. Standard: None (keine Begrenzung).
    - x_min (float, optional): Untere Begrenzung der X-Achse. Standard: None (keine Begrenzung).
    """

    # If config provided, use its values as defaults
    if config is not None:
        # Create a dictionary from config object attributes
        params = config.__dict__.copy()
        # Override with any explicitly provided kwargs
        params.update(kwargs)
    else:
        # Use provided kwargs with function defaults
        params = kwargs

    # Daten laden
    # Überprüfen der Dateiendung und Laden der Daten entsprechend
    if file_n.endswith('.csv'):
        # CSV-Datei mit Pandas laden
        df = pd.read_csv(file_n, delimiter=params['delimiter'], header=0)
        
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
        data = np.loadtxt(file_n, ndmin=1)
    
    x_val, x_err = data[:, 0] + params['x_shift'], data[:, 1]
    y_data = data[:, 2:]
    
    # Überprüfen, ob die Anzahl der y-Spalten gerade ist
    if y_data.shape[1] % 2 != 0:
        raise ValueError("Die Anzahl der y-Spalten muss gerade sein (Paare von y und y_err).")
    
    n_datasets = y_data.shape[1] // 2  # Anzahl der y-Datensätze
    
    # Labels, Marker und Farben vorbereiten
    if params['y_labels'] is None:
        params['y_labels'] = [f'{i+1}' for i in range(n_datasets)]
    if params['y_markers'] is None:
        params['y_markers'] = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', '+', 'x', 'd']
    if params['y_colors'] is None:
        cmap = plt.cm.get_cmap('tab10')
        params['y_colors'] = [cmap(i) for i in range(n_datasets)]
    
    fig, ax = plt.subplots(figsize=(params['length'], params['height']))
    
    # Achsen bei x=0 und y=0 hinzufügen
    ax.axhline(params['x_axis'], color='black', linewidth=1.5)
    ax.axvline(params['y_axis'], color='black', linewidth=1.5)
    
    # Begrenzter Wertebereich für die Ursprungsgerade initialisieren
    overall_min_x = np.inf
    overall_max_x = -np.inf
    
    # Jeden Datensatz plotten
    for i in range(n_datasets):
        y_val = y_data[:, 2*i] + params['y_shift']
        y_err = y_data[:, 2*i + 1]
    
        # Begrenzen der Daten, falls custom_datavol_limiter gesetzt ist
        limit = params['custom_datavol_limiter'] if params['custom_datavol_limiter'] > 0 else len(x_val)
        x_val_limited = x_val[:limit]
        x_err_limited = x_err[:limit]
        y_val_limited = y_val[:limit]
        y_err_limited = y_err[:limit]
        
        n = len(x_val_limited)
    
        if params['y_labels'] != '':
            label = params['y_labels'][i] if i < len(params['y_labels']) else f'Datensatz {i+1}'
        marker = params['y_markers'][i % len(params['y_markers'])]
        color = params['y_colors'][i % len(params['y_colors'])]

        labellegend = label
        if params['linear_fit']: # If linear Fit is enabled, we disable the legend because of double structures.
            labellegend="_nolegend_"
        if params['plot_errors'] == True:
            ax.errorbar(x_val_limited, y_val_limited, xerr=x_err_limited, yerr=y_err_limited,
                marker=marker, capsize=3, linestyle='none', label=labellegend, color=color, markersize=params['size'])
        else:
            ax.plot(x_val_limited, y_val_limited, marker=marker, linestyle='none', label=labellegend, color=color, markersize=params['size'])
    
        if params['linear_fit']:
            # Berechnungen der Ausgleichsgeraden -unsicherheit und des Mittelwerts 
            
            '''
            ------> This is the old version of the calculation, which is not working correctly <------

            
            #This is an attempt at considering the errors of both x and y values in various calculations. This broke me, it is not working correctly as you have to consider the errors relative to the values and shit
            #xy_err_mean = mean_calc(None, 0.5*np.sqrt(np.square(y_err_limited)+np.square(x_err_limited * ((y_val_limited + 0.5*y_err_limited)/(x_val_limited + 0.5*x_err_limited))))
            #                        + 0.5*np.sqrt(np.square(x_err_limited)+np.square(y_err_limited * ((x_val_limited + 0.5*x_err_limited)/(y_val_limited + 0.5*y_err_limited)))), 'error')
            #x_mean = mean_calc(x_val_limited, y_err_limited)
            #y_mean = mean_calc(y_val_limited, y_err_limited)
            #xy_mean = mean_calc(x_val_limited * y_val_limited, y_err_limited)
            #xs_mean = mean_calc(np.square(x_val_limited), y_err_limited)
            #y_err_mean = mean_calc(None, y_err_limited, 'error')
            #
            #root_x_mean = mean_calc(x_val_limited, x_err_limited)
            #root_y_mean = mean_calc(y_val_limited, x_err_limited)
            #root_xy_mean = mean_calc(x_val_limited * y_val_limited, x_err_limited)
            #root_ys_mean = mean_calc(np.square(y_val_limited), x_err_limited)
            ## Anhang A1.26
            #denominator = xs_mean - np.square(x_mean)
            #grad = (xy_mean - x_mean * y_mean) / denominator
            #y_inter = (xs_mean * y_mean - x_mean * xy_mean) / denominator
            #x_inter = (root_ys_mean * root_x_mean - root_y_mean * root_xy_mean) / (root_ys_mean - np.square(root_y_mean))
            # Anhang A1.21, A1.22
            # Beruecksichtigung des X-Fehlers für folgende Fehlerberechnung der Geradensteigung
            '''
            
            # We calculate a temporary gradient by the means of the linear fit formulas of A1. As we have to consider the errors of both x and y values, 
            # we use the temporary gradient to calibrate the x_err values to the y_err values. Then we calculate the length of the joint x_err and y_err vector.
            # This is then used in the calculation instead of the y_err values solely. This gives results that regard the errors of both x and y values.
            # The generall procedure is calles minimization of the squares. You can read more about it on this website: https://www.sherrytowers.com/cowan_statistical_data_analysis.pdf


            #Theo ist ein k

            tempo_grad_y = (mean_calc(x_val_limited * y_val_limited, y_err_limited) - mean_calc(x_val_limited, y_err_limited) * mean_calc(y_val_limited, y_err_limited)) /(mean_calc(np.square(x_val_limited), y_err_limited) - np.square(mean_calc(x_val_limited, y_err_limited)))
            tempo_grad_x = (mean_calc(x_val_limited * y_val_limited, x_err_limited) - mean_calc(x_val_limited, x_err_limited) * mean_calc(y_val_limited, x_err_limited)) /(mean_calc(np.square(x_val_limited), x_err_limited) - np.square(mean_calc(x_val_limited, x_err_limited)))
            print(tempo_grad_y, tempo_grad_x)
            mean_tempo_grad = (tempo_grad_y + tempo_grad_x) / 2
            xwy_err_limited = np.sqrt(np.square(x_err_limited * mean_tempo_grad) + np.square(y_err_limited))
            xy_err_mean = mean_calc(None, xwy_err_limited, 'error')
            x_mean = mean_calc(x_val_limited, xwy_err_limited)
            y_mean = mean_calc(y_val_limited, xwy_err_limited)
            xy_mean = mean_calc(x_val_limited * y_val_limited, xwy_err_limited)
            xs_mean = mean_calc(np.square(x_val_limited), xwy_err_limited)
            ys_mean = mean_calc(np.square(y_val_limited), xwy_err_limited)

            denominator = xs_mean - np.square(x_mean)
            grad = (xy_mean - x_mean * y_mean) / denominator
            y_inter = (xs_mean * y_mean - x_mean * xy_mean) / denominator
            x_inter = (mean_calc(np.square(y_val_limited), xwy_err_limited) * mean_calc(x_val_limited, xwy_err_limited) - mean_calc(y_val_limited, xwy_err_limited) * mean_calc(x_val_limited * y_val_limited, xwy_err_limited)) / (mean_calc(np.square(y_val_limited), xwy_err_limited) - np.square(mean_calc(y_val_limited, xwy_err_limited)))

            #xy_err_mean = mean_calc(None, np.sqrt(np.square(x_err_limited*grad) + np.square(y_err_limited)), 'error')
            # legacy function: np.mean((y_err * np.sqrt(((x_err / x_val)/(y_err / (y_val-y_inter)))**2 + 1))) 
            # Fehleranfällig, da x_err/x_val bei x_val=0 nicht definiert ist (only god knows how this works)
            var_grad = np.square(xy_err_mean) / (n * (xs_mean - np.square(x_mean)))
            var_y_inter = np.square(xy_err_mean) * xs_mean / (n * (xs_mean - np.square(x_mean)))
            var_x_inter = np.square(xy_err_mean) * ys_mean / (n * (ys_mean - np.square(y_mean)))
            # Anhang A1.23, A1.24
    
            grad_err = np.sqrt(var_grad)
            y_inter_err = np.sqrt(var_y_inter)
            x_inter_err = np.sqrt(var_x_inter)
    
            x_mean_err = mean_calc(None, x_err_limited, 'error')
            #x_mean_err = np.sqrt(np.sum(x_err_limited**2)) / n  # Fehler des x-Mittelwerts
            y_mean_err = mean_calc(None, y_err_limited, 'error')
            #y_mean_err = np.sqrt(np.sum(y_err_limited**2)) / n  # Fehler des y-Mittelwerts
    
            # Gerundete Werte erhalten
            grad_str, grad_err_str = round_measurement(grad, grad_err)
            y_inter_str, y_inter_err_str = round_measurement(y_inter, y_inter_err)
            x_inter_str, x_inter_err_str = round_measurement(x_inter, x_inter_err)
            x_mean_str, x_mean_err_str = round_measurement(x_mean, x_mean_err)
            y_mean_str, y_mean_err_str = round_measurement(y_mean, y_mean_err)

            # Schwerpunkt plotten
            if params['focus_point']:
                if params['plot_errors'] == True:
                    ax.errorbar(x_mean, y_mean, yerr=y_mean_err, xerr=x_mean_err, marker='x', color='red', capsize=3,
                            label=f'Schwerpunkt {label}\n({x_mean_str}±{x_mean_err_str}, {y_mean_str}±{y_mean_err_str})')  
                else:
                    ax.plot(x_mean, y_mean, marker='x', color='red',
                            label=f'Schwerpunkt {label}\n({x_mean_str}±{x_mean_err_str}, {y_mean_str}±{y_mean_err_str})')    
  
                
            # Berechnung der Regressionsgeraden
            
            overall_min_x = min(overall_min_x, min(x_val_limited)) 
            if params['plot_y_inter'] == True and overall_min_x > 0: 
                overall_min_x = 0
            #if params['plot_x_inter'] == True and overall_min_x > x_inter:
            #    overall_min_y = x_inter 
            
            overall_max_x = max(overall_max_x, max(x_val_limited))
            x_line = np.linspace(overall_min_x, overall_max_x, 100)
            best_fit = grad * x_line + y_inter
            stan_dev_1 = (grad + grad_err) * (x_line - x_mean) + y_mean
            stan_dev_2 = (grad - grad_err) * (x_line - x_mean) + y_mean
    
            # Regressionsgerade plotten
            ax.plot(x_line, best_fit, color=color, label=f'{label}: m={grad_str}±{grad_err_str}')

            # Unsicherheitsgeraden plotten
            if params['plot_errors'] == True:
                ax.plot(x_line, stan_dev_1, color=color, linestyle=':', label="_nolegend_")
                ax.plot(x_line, stan_dev_2, color=color, linestyle=':')
    
            # Y-Achsenabschnitt plotten
            if params['y_inter_label'] != None:
                labellegend = params['y_inter_label'] # Makes custom labels possible
            if params['plot_y_inter']:
                if params['y_inter_label'] == None:
                    if params['plot_errors'] == True:
                        ax.errorbar(0, y_inter, yerr=y_inter_err, marker='x', color=color, capsize=3,
                                label=f'Y-Achenabschnitt {label}\n({y_inter_str}±{y_inter_err_str})')  
                    else:
                        ax.plot(0, y_inter, marker='x', color=color,
                                label=f'Y-Achenabschnitt {label}\n({y_inter_str}±{y_inter_err_str})')  
                
            # X-Achsenabschnitt plotten
            if params['x_inter_label'] != None:
                labellegend = params['x_inter_label'] # Makes custom labels possible
            if params['plot_x_inter']:
                if params['x_inter_label'] == None:
                    if params['plot_errors'] == True:
                        ax.errorbar(x_inter, 0, xerr=x_inter_err, marker='x', color=color, capsize=3,
                                label=f'X-Achenabschnitt {label}\n({x_inter_str}±{x_inter_err_str})')  
                    else:
                        ax.plot(x_inter, 0, marker='x', color=color,
                                label=f'X-Achenabschnitt {label}\n({x_inter_str}±{x_inter_err_str})')  

            # Fit-Ergebnisse ausgeben
            print(f"Fit-Ergebnisse für {label}:")
            print(f"Schwerpunkt: ({x_mean_str} ± {x_mean_err_str}, {y_mean_str} ± {y_mean_err_str})")
            print(f"Steigung: {grad_str} ± {grad_err_str}")
            print(f"Y-Achsenabschnitt: {y_inter_str} ± {y_inter_err_str}\n")
    
    # Ursprungsgerade (auf begrenzte Werte angepasst)
    if params['Ursprungsgerade'] != None:
        line_range = np.linspace(0, overall_max_x, 100)
        plt.plot(line_range, params['Ursprungsgerade'] * line_range, color="black", linestyle="-", label=f"{params['Ursprungsgerade_title']} (m={params['Ursprungsgerade']})")

    # Formeln plotten, falls vorhanden und aktiviert
    if params.get('plot_formula', False) and params.get('formula') is not None and params.get('var_names') is not None and params.get('formula_values') is not None:
        formula = params['formula']
        var_names = params['var_names']
        values = params['formula_values']
        x_range = params.get('formula_x_range', (-10, 10))
        points = params.get('formula_points', 1000)
        
        # Extrahiere die unabhängige Variable (normalerweise die letzte in var_names)
        ind_var = var_names[-1]
        
        # Erstelle ein Wörterbuch mit den Werten für alle Variablen außer der unabhängigen
        var_values = {var: val for var, val in zip(var_names[:-1], values)}
        
        # Erstelle x-Werte für den Plot
        x_vals = np.linspace(x_range[0], x_range[1], points)
        
        # Plotte jede Formel in der Liste
        for i, expr in enumerate(formula):
            # Ersetze die Variablen durch ihre Werte
            expr_with_values = expr.subs(var_values)
            
            # Konvertiere den SymPy-Ausdruck in eine NumPy-Funktion
            f = sp.lambdify(ind_var, expr_with_values, "numpy")
            
            # Berechne die y-Werte
            y_vals = f(x_vals)
            
            # Plotte die Funktion
            ax.plot(x_vals, y_vals, label=f"Formel: {expr_with_values}")
 
    # Beschränkt den Graphen auf y_max bzw. y_min
    if 'y_max' in params and params['y_max'] is not None:
        ax.set_ylim(top=params['y_max'])
    if 'y_min' in params and params['y_min'] is not None:
        ax.set_ylim(bottom=params['y_min'])
    
    # Beschränkt den Graphen auf x_max bzw. x_min
    if 'x_max' in params and params['x_max'] is not None:
        ax.set_xlim(right=params['x_max'])
    if 'x_min' in params and params['x_min'] is not None:
        ax.set_xlim(left=params['x_min'])

    # Anzahl der Dezimalstellen für die Achsenlabels festlegen
    x_format_string = f'%.{params["x_decimal_places"]}f'
    y_format_string = f'%.{params["y_decimal_places"]}f'
    ax.xaxis.set_major_formatter(FormatStrFormatter(x_format_string))
    ax.yaxis.set_major_formatter(FormatStrFormatter(y_format_string))
    
    # Haupt- und Nebenticks setzen
    if params['x_major_ticks'] != None:
        ax.xaxis.set_major_locator(MultipleLocator(params['x_major_ticks']))
    if params['x_minor_ticks'] != None:
        ax.xaxis.set_minor_locator(MultipleLocator(params['x_minor_ticks']))
    if params['y_major_ticks'] != None:
        ax.yaxis.set_major_locator(MultipleLocator(params['y_major_ticks']))
    if params['y_minor_ticks'] != None:
        ax.yaxis.set_minor_locator(MultipleLocator(params['y_minor_ticks']))

    # Rasterlinien anpassen
    if params['x_major_ticks'] != None or params['y_major_ticks'] != None:
        ax.grid(which='major', color='grey', linestyle='-', linewidth=0.75)
    if params['x_minor_ticks'] != None or params['y_minor_ticks'] != None:
        ax.grid(which='minor', color='lightgrey', linestyle=':', linewidth=0.5)

    def scientific_formatter(x, pos):
        if abs(x) < 1e-3 or abs(x) >= 1e4:  # Customize these thresholds
            return f'{x:.1e}'
        else:
            return f'{x:.1f}'  # Regular formatting for numbers in the middle range

    ax.xaxis.set_major_formatter(FuncFormatter(scientific_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))
    
    # Achsenbeschriftungen und Titel
    ax.set_xlabel(params['x_label'])
    ax.set_ylabel(params['y_label'])
    ax.set_title(params['title'])
    
    # Legende anzeigen
    if params['legendlocation'] == 'outside right':
        ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    elif params['legendlocation'] != None:
        ax.legend(loc=params['legendlocation'])
    
    if params['save']:
        plt.savefig(f'{file_n}.png', bbox_inches='tight')
    
    plt.show()