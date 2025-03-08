# config file for geraden_fit.py
class config_1:
    file_n = "daten.csv" # Pfad zur Datei mit den zu visualisierenden Daten
    title = "Messwerte mit Fehlerbalken"    # Titel des Plots
    x_label = "Zeit (s)"
    y_label = "Spannung (V)"
    save = True
    linear_fit = True
    focus_point = True
    plot_y_inter = False
    y_inter_label = None
    Ursprungsgerade = None
    plot_errors = True
    x_axis = 0
    y_axis = 0
    x_major_ticks = None
    x_minor_ticks = None
    y_major_ticks = None
    y_minor_ticks = None
    legendlocation = "best"
    y_labels = None
    y_markers = None
    y_colors = None
    x_decimal_places = 2
    y_decimal_places = 2
    scientific_limits = (-3, 3)
    custom_datavol_limiter = 0
    x_shift = 0
    y_shift = 0
    length = 10
    height = 5
    size = 1
    delimiter = ""

    """
    Parameter:
    - file_n: Pfad zur Datei mit den zu visualisierenden Daten.
    - title (str optional): Titel des Plots. Standard: 'unnamed'.
    - x_label (str optional): Beschriftung der X-Achse. Standard: 'X-Achse'.
    - y_label (str optional): Beschriftung der Y-Achse. Standard: 'Y-Achse'.
    - save (bool optional): Ob der Plot gespeichert werden soll. Standard: False.
    - linear_fit (bool optional): Ob eine lineare Regression durchgeführt wird. Standard: False.
    - focus_point (bool optional): Ob der Schwerpunkt mit Fehlerbalken dargestellt wird. Standard: False.
    - plot_y_inter (bool optional): Ob der Y-Achsenabschnitt angezeigt wird. Standard: False.
    - y_inter_label (str optional): Label für den Y-Achsenabschnitt. Standard: None.
    - Ursprungsgerade (float optional): Erstellt Ursprungsgerade mit Steigung Ursprungsgerade. Standard: None.
    - plot_errors (bool optional): Ob Fehler auch geplotted werden. Standard: True.
    - x_axis (float optional): Position der vertikalen Linie bei x=0. Standard: 0.
    - y_axis (float optional): Position der horizontalen Linie bei y=0. Standard: 0.
    - x_major_ticks (float optional): Abstand zwischen den Hauptticks der X-Achse. Standard: None.
    - x_minor_ticks (float optional): Abstand zwischen den Nebenticks der X-Achse. Standard: None.
    - y_major_ticks (float optional): Abstand zwischen den Hauptticks der Y-Achse. Standard: None.
    - y_minor_ticks (float optional): Abstand zwischen den Nebenticks der Y-Achse. Standard: None.
    - legendlocation (str optional): Position der Legende. Standard: 'best'.
    - y_labels (list optional): Bezeichnungen für die Y-Datensätze. Standard: None.
    - y_markers (list optional): Marker für die einzelnen Datensätze. Standard: None.
    - y_colors (list optional): Farben für die einzelnen Datensätze. Standard: None.
    - x_decimal_places (int optional): Anzahl der Dezimalstellen auf der X-Achse. Standard: 1.
    - y_decimal_places (int optional): Anzahl der Dezimalstellen auf der Y-Achse. Standard: 1.
    - scientific_limits (tuple optional): Grenzen für wissenschaftliche Notation. Standard: (-33).
    - custom_datavol_limiter (int optional): Begrenzung der Anzahl der Datenpunkte. Standard: 0 (keine Begrenzung).
    - x_shift (float optional): Horizontaler Offset für die X-Daten. Standard: 0.
    - y_shift (float optional): Vertikaler Offset für die Y-Daten. Standard: 0.
    - length (float optional): Länge der Abbildung in Zoll. Standard: 15.
    - height (float optional): Höhe der Abbildung in Zoll. Standard: 5.
    - size (float optional): Größe der Marker. Standard: 1.
    - delimiter (str optional): Trennzeichen für CSV-Dateien. Standard: ''.
    """
