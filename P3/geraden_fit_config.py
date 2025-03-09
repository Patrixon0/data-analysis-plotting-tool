# geraden_fit_config.py
from typing import List, Tuple, Optional, Union

class GeradeConfig:
    """Configuration for geraden_fit function."""
    
    def __init__(
        self,
        title: str = "unnamed",
        x_label: str = "X-Achse",
        y_label: str = "Y-Achse",
        save: bool = False,
        linear_fit: bool = False,
        focus_point: bool = False,
        plot_y_inter: bool = False,
        plot_x_inter: bool = False,
        y_inter_label: Optional[str] = None,
        x_inter_label: Optional[str] = None,
        Ursprungsgerade: Optional[float] = None,
        plot_errors: bool = True,
        x_axis: float = 0,
        y_axis: float = 0,
        x_major_ticks: Optional[float] = None,
        x_minor_ticks: Optional[float] = None,
        y_major_ticks: Optional[float] = None,
        y_minor_ticks: Optional[float] = None,
        legendlocation: str = 'best',
        y_labels: Optional[List[str]] = None,
        y_markers: Optional[List[str]] = None,
        y_colors: Optional[List[str]] = None,
        x_decimal_places: int = 1,
        y_decimal_places: int = 1,
        scientific_limits: Tuple[int, int] = (-3, 3),
        custom_datavol_limiter: int = 0,
        x_shift: float = 0,
        y_shift: float = 0,
        length: float = 15,
        height: float = 5,
        size: float = 1,
        delimiter: str = ',',
        y_max: Optional[float] = None,
        y_min: Optional[float] = None,
    ):
        """
        Configuration parameters for the geraden_fit function.
        
        Args:
            title: Title of the plot
            x_label: Label for the X-axis
            y_label: Label for the Y-axis
            save: Whether to save the plot
            linear_fit: Whether to perform linear regression
            focus_point: Whether to display focus point with error bars
            plot_y_inter: Whether to show y-intercept
            plot_x_inter: Whether to show y-intercept
            y_inter_label: Label for the y-intercept
            x_inter_label: Label for the y-intercept
            Ursprungsgerade: Creates line through origin with this slope
            plot_errors: Whether to plot errors
            x_axis: Position of vertical line at x=0
            y_axis: Position of horizontal line at y=0
            x_major_ticks: Spacing between major x-axis ticks
            x_minor_ticks: Spacing between minor x-axis ticks
            y_major_ticks: Spacing between major y-axis ticks
            y_minor_ticks: Spacing between minor y-axis ticks
            legendlocation: Position of the legend
            y_labels: Labels for the Y datasets
            y_markers: Markers for individual datasets
            y_colors: Colors for individual datasets
            x_decimal_places: Number of decimal places on X-axis
            y_decimal_places: Number of decimal places on Y-axis
            scientific_limits: Limits for scientific notation
            custom_datavol_limiter: Limit for number of data points
            x_shift: Horizontal offset for X data
            y_shift: Vertical offset for Y data
            length: Figure length in inches
            height: Figure height in inches
            size: Size of markers
            delimiter: Delimiter for CSV files
            y_max: Upper limit of Y-axis
            y_min: Lower limit of Y-axis
        """
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.save = save
        self.linear_fit = linear_fit
        self.focus_point = focus_point
        self.plot_y_inter = plot_y_inter
        self.plot_x_inter = plot_x_inter
        self.y_inter_label = y_inter_label
        self.x_inter_label = x_inter_label
        self.Ursprungsgerade = Ursprungsgerade
        self.plot_errors = plot_errors
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x_major_ticks = x_major_ticks
        self.x_minor_ticks = x_minor_ticks
        self.y_major_ticks = y_major_ticks
        self.y_minor_ticks = y_minor_ticks
        self.legendlocation = legendlocation
        self.y_labels = y_labels
        self.y_markers = y_markers
        self.y_colors = y_colors
        self.x_decimal_places = x_decimal_places
        self.y_decimal_places = y_decimal_places
        self.scientific_limits = scientific_limits
        self.custom_datavol_limiter = custom_datavol_limiter
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.length = length
        self.height = height
        self.size = size
        self.delimiter = delimiter
        self.y_max = y_max
        self.y_min = y_min

config_1 = GeradeConfig(
    title = "Messwerte mit Fehlerbalken",
    x_label = "Zeit (s)",
    y_label = "Spannung (V)",
    save = True,
    linear_fit = True,
    focus_point = True,
    plot_y_inter = False,
    plot_x_inter = False,
    y_inter_label = None,
    x_inter_label = None,
    Ursprungsgerade = None,
    plot_errors = True,
    x_axis = 0,
    y_axis = 0,
    x_major_ticks = None,
    x_minor_ticks = None,
    y_major_ticks = None,
    y_minor_ticks = None,
    legendlocation = "best",
    y_labels = None,
    y_markers = None,
    y_colors = None,
    x_decimal_places = 2,
    y_decimal_places = 2,
    scientific_limits = (-3, 3),
    custom_datavol_limiter = 0,
    x_shift = 0,
    y_shift = 0,
    length = 10,
    height = 5,
    size = 1,
    delimiter = ",",
    y_max = None,
    y_min = None
)
