# tabellen_config.py
from typing import List, Dict, Tuple, Optional, Union, Callable

class TabellenConfig:
    """Konfiguration für die tabellen_ersteller Funktion."""
    
    def __init__(
        self,
        title: str = "Tabelle",
        header_rows: int = 1,
        skip_rows: int = 0,
        round_errors: bool = True,
        error_cols: List[int] = None,
        value_cols: List[int] = None,
        col_labels: Optional[List[str]] = None,
        col_widths: Optional[List[float]] = None,
        col_colors: Optional[List[str]] = None,
        header_color: str = "#D7E4BC",
        row_colors: List[str] = None,
        text_color: str = "black",
        font_size: int = 12,
        cell_height: float = 0.5,
        include_index: bool = False,
        index_label: str = "Nr.",
        decimals: Dict[int, int] = None,
        scientific_notation: List[int] = None,
        delimiter: str = ",",
        precision_mode: str = "auto",
        add_plusminus: bool = True,
        save: bool = False,
        figsize: Tuple[float, float] = (10, 6),
        thousands_separator: bool = False,
        cell_alignment: str = "center",
        special_formats: Dict[int, Callable] = None,
    ):
        """
        Konfigurationsparameter für die tabellen_ersteller Funktion.
        
        Args:
            title: Titel der Tabelle
            header_rows: Anzahl der Kopfzeilen
            skip_rows: Anzahl der zu überspringenden Zeilen am Anfang
            round_errors: Ob Werte mit Fehlern gerundet werden sollen
            error_cols: Liste der Spaltenindizes, die Fehler enthalten
            value_cols: Liste der Spaltenindizes, die zu rundende Werte enthalten
            col_labels: Benutzerdefinierte Spaltenbeschriftungen
            col_widths: Benutzerdefinierte Spaltenbreiten
            col_colors: Benutzerdefinierte Spaltenfarben
            header_color: Farbe der Kopfzeile
            row_colors: Liste alternierender Zeilenfarben
            text_color: Textfarbe
            font_size: Schriftgröße
            cell_height: Zellenhöhe
            include_index: Ob die Indexspalte angezeigt werden soll
            index_label: Beschriftung der Indexspalte
            decimals: Dictionary mit Spaltenindizes und Anzahl der Dezimalstellen
            scientific_notation: Liste der Spaltenindizes für wissenschaftliche Notation
            delimiter: Trennzeichen für CSV-Dateien
            precision_mode: Rundungsmodus ('auto', 'fixed')
            add_plusminus: Ob +/- für Fehler hinzugefügt werden soll
            save: Ob die Tabelle als Bild gespeichert werden soll
            figsize: Größe der Figur (Breite, Höhe)
            thousands_separator: Ob Tausendertrennzeichen angezeigt werden sollen
            cell_alignment: Textausrichtung in den Zellen ('left', 'center', 'right')
            special_formats: Dictionary mit Spaltenindizes und benutzerdefinierten Formatierungsfunktionen
        """
        self.title = title
        self.header_rows = header_rows
        self.skip_rows = skip_rows
        self.round_errors = round_errors
        self.error_cols = [] if error_cols is None else error_cols
        self.value_cols = [] if value_cols is None else value_cols
        self.col_labels = col_labels
        self.col_widths = col_widths
        self.col_colors = col_colors
        self.header_color = header_color
        self.row_colors = ["#FFFFFF", "#F2F2F2"] if row_colors is None else row_colors
        self.text_color = text_color
        self.font_size = font_size
        self.cell_height = cell_height
        self.include_index = include_index
        self.index_label = index_label
        self.decimals = {} if decimals is None else decimals
        self.scientific_notation = [] if scientific_notation is None else scientific_notation
        self.delimiter = delimiter
        self.precision_mode = precision_mode
        self.add_plusminus = add_plusminus
        self.save = save
        self.figsize = figsize
        self.thousands_separator = thousands_separator
        self.cell_alignment = cell_alignment
        self.special_formats = {} if special_formats is None else special_formats

# Standardkonfiguration erstellen
config_1 = TabellenConfig(
    title="Messwerte",
    header_rows=1,
    skip_rows=0,
    round_errors=True,
    error_cols=[],  # Fehler in 0 Spalten
    value_cols=[],  # Werte in 0 Spalten
    col_labels=None,  # Standardmäßig werden die Spaltenüberschriften aus der CSV-Datei verwendet
    col_widths=None,  # Standardmäßig gleiche Breite für alle Spalten
    col_colors=None,  # Keine speziellen Spaltenfarben
    header_color="#D7E4BC",  # Hellgrüner Hintergrund für die Kopfzeile
    row_colors=["#FFFFFF", "#F2F2F2"],  # Abwechselnd weiße und hellgraue Zeilen
    text_color="black",
    font_size=12,
    cell_height=0.8,
    include_index=False,  # Keine separate Indexspalte
    index_label="Nr.",
    decimals={},  # Keine speziellen Dezimalstellen
    scientific_notation=[],  # Keine wissenschaftliche Notation
    delimiter=",",
    precision_mode="auto",  # Automatische Rundung basierend auf dem Fehler
    add_plusminus=True,  # ±-Symbol für Messwerte mit Fehlern anzeigen
    save=False,
    figsize=(10, 6),
    thousands_separator=False,
    cell_alignment="center",
    special_formats={}  # Keine speziellen Formatierungsfunktionen
)

# Eine zweite Beispielkonfiguration für wissenschaftliche Tabellen
config_2 = TabellenConfig(
    title="Wissenschaftliche Messwerte",
    header_rows=1,
    skip_rows=0,
    round_errors=True,
    error_cols=[1, 3, 5],
    value_cols=[0, 2, 4],
    col_labels=["Messreihe", "Δx", "Spannung", "ΔU", "Strom", "ΔI"],  # Spezifische Spaltenüberschriften
    col_widths=[0.15, 0.1, 0.2, 0.1, 0.2, 0.1],  # Angepasste Breiten für jede Spalte
    col_colors=None,
    header_color="#B4C7E7",  # Hellblauer Hintergrund für die Kopfzeile
    row_colors=["#FFFFFF", "#E6E6E6"],  # Abwechselnd weiße und graue Zeilen
    text_color="black",
    font_size=12,
    cell_height=0.6,
    include_index=True,  # Indexspalte anzeigen
    index_label="#",
    decimals={0: 0, 2: 3, 4: 4},  # Spalte 0 mit 0, Spalte 2 mit 3 und Spalte 4 mit 4 Dezimalstellen
    scientific_notation=[4],  # Spalte 4 in wissenschaftlicher Notation
    delimiter=",",
    precision_mode="auto",
    add_plusminus=True,
    save=True,  # Tabelle automatisch speichern
    figsize=(12, 8),
    thousands_separator=True,  # Tausendertrennzeichen anzeigen
    cell_alignment="right",  # Text rechtsbündig ausrichten
    special_formats={}
)