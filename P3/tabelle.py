import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
from decimal import Decimal, ROUND_HALF_UP, getcontext
from geraden_fit import round_measurement

from tabellen_config import config_1

def tabellen_ersteller(file_n, config=config_1, **kwargs):
    """
    Erstellt eine formatierte Tabelle aus einer CSV-Datei und zeigt diese als Matplotlib-Figur an.
    Die Tabelle kann mit verschiedenen Optionen angepasst werden.
    
    Parameter:
    - file_n (str): Pfad zur CSV-Datei.
    - config (TabellenConfig, optional): Ein Konfigurationsobjekt mit vordefinierten Einstellungen.
    - **kwargs: Individuelle Parametereinstellungen, die die Konfigurationswerte überschreiben.
    
    Mögliche Parameter:
    - title (str, optional): Titel der Tabelle. Standard: 'Tabelle'.
    - header_rows (int, optional): Anzahl der Kopfzeilen. Standard: 1.
    - skip_rows (int, optional): Anzahl der zu überspringenden Zeilen am Anfang. Standard: 0.
    - round_errors (bool, optional): Ob Werte mit Fehlern gerundet werden sollen. Standard: True.
    - error_cols (list, optional): Liste der Spaltenindizes, die Fehler enthalten. Standard: [].
    - value_cols (list, optional): Liste der Spaltenindizes, die zu rundende Werte enthalten. Standard: [].
    - col_labels (list, optional): Benutzerdefinierte Spaltenbeschriftungen. Standard: None.
    - col_widths (list, optional): Benutzerdefinierte Spaltenbreiten. Standard: None.
    - col_colors (list, optional): Benutzerdefinierte Spaltenfarben. Standard: None.
    - header_color (str, optional): Farbe der Kopfzeile. Standard: '#D7E4BC'.
    - row_colors (list, optional): Liste alternierender Zeilenfarben. Standard: ['#FFFFFF', '#F2F2F2'].
    - text_color (str, optional): Textfarbe. Standard: 'black'.
    - font_size (int, optional): Schriftgröße. Standard: 12.
    - cell_height (float, optional): Zellenhöhe. Standard: 0.8.
    - include_index (bool, optional): Ob die Indexspalte angezeigt werden soll. Standard: False.
    - index_label (str, optional): Beschriftung der Indexspalte. Standard: 'Nr.'.
    - decimals (dict, optional): Dictionary mit Spaltenindizes und Anzahl der Dezimalstellen. Standard: {}.
    - scientific_notation (list, optional): Liste der Spaltenindizes für wissenschaftliche Notation. Standard: [].
    - delimiter (str, optional): Trennzeichen für CSV-Dateien. Standard: ','.
    - precision_mode (str, optional): Rundungsmodus ('auto', 'fixed'). Standard: 'auto'.
    - add_plusminus (bool, optional): Ob +/- für Fehler hinzugefügt werden soll. Standard: True.
    - save (bool, optional): Ob die Tabelle als Bild gespeichert werden soll. Standard: False.
    - figsize (tuple, optional): Größe der Figur (Breite, Höhe). Standard: (10, 6).
    - thousands_separator (bool, optional): Ob Tausendertrennzeichen angezeigt werden sollen. Standard: False.
    - cell_alignment (str, optional): Textausrichtung in den Zellen ('left', 'center', 'right'). Standard: 'center'.
    - special_formats (dict, optional): Dictionary mit Spaltenindizes und benutzerdefinierten Formatierungsfunktionen. Standard: {}.
    """
    
    # Parameter aus Konfiguration und kwargs kombinieren
    if config is not None:
        # Dictionary aus Konfigurationsobjekt erstellen
        params = config.__dict__.copy()
        # Mit explizit angegebenen kwargs überschreiben
        params.update(kwargs)
    else:
        # Nur angegebene kwargs mit Funktions-Standardwerten verwenden
        params = kwargs
    
    # CSV-Datei laden
    df = pd.read_csv(file_n, delimiter=params['delimiter'], skiprows=params['skip_rows'])
    
    # Benutzerdefinierte Spaltenbeschriftungen verwenden, falls vorhanden
    if params['col_labels'] is not None:
        # Stellen Sie sicher, dass genug Labels für alle Spalten vorhanden sind
        if len(params['col_labels']) >= len(df.columns):
            df.columns = params['col_labels'][:len(df.columns)]
        else:
            # Ergänzen Sie die bestehenden Labels mit Standardnamen
            existing_labels = params['col_labels'].copy()
            for i in range(len(existing_labels), len(df.columns)):
                existing_labels.append(f'Spalte {i+1}')
            df.columns = existing_labels
    
    # Erstellen Sie eine Kopie, um die formatierten Werte zu speichern
    formatted_df = df.copy()
    
    # Werte mit Fehlerrundung formatieren
    if params['round_errors'] and params['value_cols'] and params['error_cols']:
        for val_idx, err_idx in zip(params['value_cols'], params['error_cols']):
            if val_idx < len(df.columns) and err_idx < len(df.columns):
                val_col = df.columns[val_idx]
                err_col = df.columns[err_idx]
                for idx, row in df.iterrows():
                    val = row[val_col]
                    err = row[err_col]
                    try:
                        val_float = float(val)
                        err_float = float(err)
                        rounded_val, rounded_err = round_measurement(val_float, err_float)
                        
                        if params['add_plusminus']:
                            formatted_df.at[idx, val_col] = f"{rounded_val} ± {rounded_err}"
                        else:
                            formatted_df.at[idx, val_col] = rounded_val
                            formatted_df.at[idx, err_col] = rounded_err
                    except (ValueError, TypeError):
                        # Bei nicht-numerischen Werten unverändert lassen
                        pass
    
    # Dezimalstellen für bestimmte Spalten formatieren
    for col_idx, decimal_places in params['decimals'].items():
        if col_idx < len(df.columns):
            col = df.columns[col_idx]
            for idx, value in enumerate(df[col]):
                try:
                    # Change this line to remove trailing zeros
                    formatted_value = f"{float(value):.{decimal_places}f}".rstrip('0').rstrip('.')
                    if params['thousands_separator']:
                        parts = formatted_value.split('.')
                        parts[0] = "{:,}".format(int(parts[0])).replace(',', '.')
                        if len(parts) > 1:
                            formatted_value = ','.join([parts[0], parts[1]])
                        else:
                            formatted_value = parts[0]
                    formatted_df.at[idx, col] = formatted_value
                except (ValueError, TypeError):
                    # For non-numeric values, leave unchanged
                    pass
    
    # Wissenschaftliche Notation für bestimmte Spalten
    for col_idx in params['scientific_notation']:
        if col_idx < len(df.columns):
            col = df.columns[col_idx]
            for idx, value in enumerate(df[col]):
                try:
                    formatted_df.at[idx, col] = f"{float(value):.2e}"
                except (ValueError, TypeError):
                    # Bei nicht-numerischen Werten unverändert lassen
                    pass
    
    # Spezielle Formatierungen anwenden
    for col_idx, format_func in params['special_formats'].items():
        if col_idx < len(df.columns):
            col = df.columns[col_idx]
            for idx, value in enumerate(df[col]):
                try:
                    formatted_df.at[idx, col] = format_func(value)
                except Exception:
                    # Bei Fehlern unverändert lassen
                    pass
    
    # Matplotlib-Figur erstellen
    fig, ax = plt.subplots(figsize=params['figsize'])
    
    # Achsen ausblenden
    ax.axis('tight')
    ax.axis('off')
    
    # Table erstellen
    data = formatted_df.values
    
    # Index hinzufügen, falls gewünscht
    if params['include_index']:
        # Index-Spalte erstellen
        index_col = np.array([i+1 for i in range(len(formatted_df))]).reshape(-1, 1)
        data = np.hstack((index_col, data))
        
        # Spaltenbeschriftungen aktualisieren
        columns = [params['index_label']] + list(formatted_df.columns)
    else:
        columns = list(formatted_df.columns)
    
    # Spaltenbreiten festlegen
    if params['col_widths'] is None:
        col_widths = [1/len(columns)] * len(columns)
    else:
        # Sicherstellen, dass genug Breiten vorhanden sind
        if len(params['col_widths']) >= len(columns):
            col_widths = params['col_widths'][:len(columns)]
        else:
            # Fehlende Breiten mit Standardwert ergänzen
            col_widths = params['col_widths'] + [1/len(columns)] * (len(columns) - len(params['col_widths']))
    
    # Tabelle erstellen
    table = ax.table(
        cellText=data,
        colLabels=columns,
        loc='center',
        cellLoc=params['cell_alignment'],
        colWidths=col_widths
    )
    
    # Zellenhöhe anpassen
    table.scale(1, params['cell_height'])
    
    # Kopfzeile formatieren
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Kopfzeile
            cell.set_facecolor(params['header_color'])
            cell.set_text_props(weight='bold', color=params['text_color'])
        else:  # Datenzeilen
            # Alternierende Zeilenfarben
            if params['row_colors'] and len(params['row_colors']) > 0:
                cell.set_facecolor(params['row_colors'][(i-1) % len(params['row_colors'])])
            
            # Spaltenfarben anwenden, falls vorhanden
            if params['col_colors'] and j < len(params['col_colors']) and params['col_colors'][j] is not None:
                cell.set_facecolor(params['col_colors'][j])
        
        # Textformatierung für alle Zellen
        cell.set_text_props(fontsize=params['font_size'], color=params['text_color'])
    
    # Titel hinzufügen
    plt.title(params['title'], fontsize=params['font_size']+2, fontweight='bold')
    
    # Anpassen der Figurgröße an die Tabelle
    plt.tight_layout()
    
    # Tabelle speichern, falls gewünscht
    if params['save']:
        plt.savefig(f"{file_n}_tabelle.png", bbox_inches='tight', dpi=300)
    
    # Tabelle anzeigen
    plt.show()
    
    return formatted_df
