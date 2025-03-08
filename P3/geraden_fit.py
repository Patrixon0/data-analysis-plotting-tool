import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, ScalarFormatter
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

    weights = 1 / np.square(err_input)
    
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
    - y_inter_label (str, optional): Label für den Y-Achsenabschnitt. Standard: None.
    - Ursprungsgerade (float, optional): Erstellt Ursprungsgerade mit Steigung Ursprungsgerade. Standard: None.
    - plot_errors (bool, optional): Ob Fehler auch geplotted werden. Standard: True.
    - x_axis (float, optional): Position der vertikalen Linie bei x=0. Standard: 0.
    - y_axis (float, optional): Position der horizontalen Linie bei y=0. Standard: 0.
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
        df = pd.read_csv(file_n, delimiter=config.delimiter)
        # Umwandlung in NumPy-Array für weitere Verarbeitung
        data = df.values
    else:
        # Bestehender Code für Leerzeichen-getrennte Dateien
        data = np.loadtxt(file_n, ndmin=1)
    
    x_val, x_err = data[:, 0] + config.x_shift, data[:, 1]
    y_data = data[:, 2:]
    
    # Überprüfen, ob die Anzahl der y-Spalten gerade ist
    if y_data.shape[1] % 2 != 0:
        raise ValueError("Die Anzahl der y-Spalten muss gerade sein (Paare von y und y_err).")
    
    n_datasets = y_data.shape[1] // 2  # Anzahl der y-Datensätze
    
    # Labels, Marker und Farben vorbereiten
    if config.y_labels is None:
        config.y_labels = [f'{i+1}' for i in range(n_datasets)]
    if config.y_markers is None:
        config.y_markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', '+', 'x', 'd']
    if config.y_colors is None:
        cmap = plt.cm.get_cmap('tab10')
        config.y_colors = [cmap(i) for i in range(n_datasets)]
    
    fig, ax = plt.subplots(figsize=(config.length, config.height))
    
    # Achsen bei x=0 und y=0 hinzufügen
    ax.axhline(config.y_axis, color='black', linewidth=1.5)
    ax.axvline(config.x_axis, color='black', linewidth=1.5)
    
    # Begrenzter Wertebereich für die Ursprungsgerade initialisieren
    overall_min_x = np.inf
    overall_max_x = -np.inf
    
    # Jeden Datensatz plotten
    for i in range(n_datasets):
        y_val = y_data[:, 2*i] + config.y_shift
        y_err = y_data[:, 2*i + 1]
    
        # Begrenzen der Daten, falls custom_datavol_limiter gesetzt ist
        limit = config.custom_datavol_limiter if config.custom_datavol_limiter > 0 else len(x_val)
        x_val_limited = x_val[:limit]
        x_err_limited = x_err[:limit]
        y_val_limited = y_val[:limit]
        y_err_limited = y_err[:limit]
    
        n = len(x_val_limited)
    
        if config.y_labels != '':
            label = config.y_labels[i] if i < len(config.y_labels) else f'Datensatz {i+1}'
        marker = config.y_markers[i % len(config.y_markers)]
        color = config.y_colors[i % len(config.y_colors)]
        if config.plot_errors == True:
            ax.errorbar(x_val_limited, y_val_limited, xerr=x_err_limited, yerr=y_err_limited,
                marker=marker, capsize=3, linestyle='none', label=label, color=color, markersize=config.size)
        else:
            ax.plot(x_val_limited, y_val_limited, marker=marker, linestyle='none', label=label, color=color, markersize=size)
    
        if config.linear_fit:
            # Berechnungen der Ausgleichsgeraden -unsicherheit und des Mittelwerts 
            x_mean = mean_calc(x_val_limited, y_err_limited)
            y_mean = mean_calc(y_val_limited, y_err_limited)
            xty_mean = mean_calc(x_val_limited * y_val_limited, y_err_limited)
            xs_mean = mean_calc(x_val_limited ** 2, y_err_limited)
            y_err_mean = mean_calc(y_val_limited, y_err_limited, 'error')
            # Anhang A1.26

            denominator = xs_mean - x_mean ** 2
            grad = (xty_mean - x_mean * y_mean) / denominator
            y_inter = (xs_mean * y_mean - x_mean * xty_mean) / denominator
            # Anhang A1.21, A1.22

            xy_err_mean = mean_calc(None, np.sqrt(x_err_limited**2 + y_err_limited**2), 'error')
            # Beruecksichtigung des X-Fehlers für folgende Fehlerberechnung der Geradensteigung

            # legacy function: np.mean((y_err * np.sqrt(((x_err / x_val)/(y_err / (y_val-y_inter)))**2 + 1))) 
            # Fehleranfällig, da x_err/x_val bei x_val=0 nicht definiert ist (only god knows how this works)
            var_grad = xy_err_mean ** 2 / (n * (xs_mean - x_mean ** 2))
            var_inter = xy_err_mean ** 2 * xs_mean / (n * (xs_mean - x_mean ** 2))
            # Anhang A1.23, A1.24

            grad_err = np.sqrt(var_grad)
            y_inter_err = np.sqrt(var_inter)
    
            x_mean_err = np.sqrt(np.sum(x_err_limited**2)) / n  # Fehler des Mittelwerts
    
            # Gerundete Werte erhalten
            grad_str, grad_err_str = round_measurement(grad, grad_err)
            y_inter_str, y_inter_err_str = round_measurement(y_inter, y_inter_err)
            x_mean_str, x_mean_err_str = round_measurement(x_mean, x_mean_err)
            y_mean_str, y_mean_err_str = round_measurement(y_mean, y_err_mean)

            # Schwerpunkt plotten
            if config.focus_point:
                if config.plot_errors == True:
                    ax.errorbar(x_mean, y_mean, yerr=y_err_mean, xerr=x_mean_err, marker='x', color='red', capsize=3,
                            label=f'Schwerpunkt {label}\n({x_mean_str}±{x_mean_err_str}, {y_mean_str}±{y_mean_err_str})')  
                else:
                    ax.plot(x_mean, y_mean, marker='x', color='red',
                            label=f'Schwerpunkt {label}\n({x_mean_str}±{x_mean_err_str}, {y_mean_str}±{y_mean_err_str})')    
  
                
            # Berechnung der Regressionsgeraden
            if config.plot_y_inter == False: 
                overall_min_x = min(overall_min_x, min(x_val_limited)) 
            else: 
                overall_min_x = 0
            
            overall_max_x = max(overall_max_x, max(x_val_limited))
            x_line = np.linspace(overall_min_x, overall_max_x, 100)
            best_fit = grad * x_line + y_inter
            stan_dev_1 = (grad + grad_err) * (x_line - x_mean) + y_mean
            stan_dev_2 = (grad - grad_err) * (x_line - x_mean) + y_mean
    
            # Regressionsgerade plotten
            ax.plot(x_line, best_fit, color=color, label=f'Fit {label}: m={grad_str}±{grad_err_str}')

            # Unsicherheitsgeraden plotten
            if config.plot_errors == True:
                ax.plot(x_line, stan_dev_1, color=color, linestyle=':', label=f'Unsicherheit {label}')
                ax.plot(x_line, stan_dev_2, color=color, linestyle=':')
    
            # Y-Achsenabschnitt plotten
            if config.plot_y_inter:
                if config.y_inter_label == None:
                    if config.plot_errors == True:
                        ax.errorbar(0, y_inter, yerr=y_inter_err, marker='x', color='#ffc130', capsize=3,
                                label=f'Y-Achenabschnitt {label}\n({y_inter_str}±{y_inter_err_str})')  
                    else:
                        ax.plot(0, y_inter, marker='x', color='#ffc130',
                                label=f'Y-Achenabschnitt {label}\n({y_inter_str}±{y_inter_err_str})')  
                else:  
                    if config.plot_errors == True:
                        ax.errorbar(0, y_inter, yerr=y_inter_err, marker='x', color='#ffc130', capsize=3,
                                label=f'Y-Achenabschnitt {config.y_inter_label}\n({y_inter_str}±{y_inter_err_str})') 
                    else:
                        ax.plot(0, y_inter, marker='x', color='#ffc130', 
                                label=f'Y-Achenabschnitt {config.y_inter_label}\n({y_inter_str}±{y_inter_err_str})') 
                
            # Fit-Ergebnisse ausgeben
            print(f"Fit-Ergebnisse für {label}:")
            print(f"Schwerpunkt: ({x_mean_str} ± {x_mean_err_str}, {y_mean_str} ± {y_mean_err_str})")
            print(f"Steigung: {grad_str} ± {grad_err_str}")
            print(f"Y-Achsenabschnitt: {y_inter_str} ± {y_inter_err_str}\n")
    
    # Ursprungsgerade (auf begrenzte Werte angepasst)
    if config.Ursprungsgerade != None:
        line_range = np.linspace(0, overall_max_x, 100)
        plt.plot(line_range, config.Ursprungsgerade * line_range, color="red", linestyle="--", label=f"Ursprungsgerade (y={Ursprungsgerade}*x)")

    # Anzahl der Dezimalstellen für die Achsenlabels festlegen
    x_format_string = f'%.{config.x_decimal_places}f'
    y_format_string = f'%.{config.y_decimal_places}f'
    ax.xaxis.set_major_formatter(FormatStrFormatter(x_format_string))
    ax.yaxis.set_major_formatter(FormatStrFormatter(y_format_string))
    
    # Haupt- und Nebenticks setzen
    if config.x_major_ticks != None:
        ax.xaxis.set_major_locator(MultipleLocator(config.x_major_ticks))
    if config.x_minor_ticks != None:
        ax.xaxis.set_minor_locator(MultipleLocator(config.x_minor_ticks))
    if config.y_major_ticks != None:
        ax.yaxis.set_major_locator(MultipleLocator(config.y_major_ticks))
    if config.y_minor_ticks != None:
        ax.yaxis.set_minor_locator(MultipleLocator(config.y_minor_ticks))

    # Rasterlinien anpassen
    if config.x_major_ticks != None or config.y_major_ticks != None:
        ax.grid(which='major', color='grey', linestyle='-', linewidth=0.75)
    if config.x_minor_ticks != None or config.y_minor_ticks != None:
        ax.grid(which='minor', color='lightgrey', linestyle=':', linewidth=0.5)

    # Wissenschaftliche Notation für Ticks aktivieren
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits(config.scientific_limits)

    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    
    # Achsenbeschriftungen und Titel
    ax.set_xlabel(config.x_label)
    ax.set_ylabel(config.y_label)
    ax.set_title(config.title)
    
    # Legende anzeigen
    ax.legend(loc=config.legendlocation)
    
    if config.save:
        plt.savefig(f'{file_n}.png', bbox_inches='tight')
    
    plt.show()