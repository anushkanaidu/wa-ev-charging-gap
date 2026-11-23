"""Shared chart theme for the WA EV Charging Gap project (DATA 5310).

Use it with `import ev_theme as ev`. Importing it turns the theme on.
Same colors and styles as the team theme, so all our plots look like one set.
"""
import os
import altair as alt

# ---- colors ----
BLUE = "#2a78d6"
HIGHLIGHT = "#eb6834"
GRAY = "#8a8983"
TEXT = "#0b0b0b"
MUTED = "#52514e"

CATEGORY = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQUENTIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
DIVERGING = ["#184f95", "#3987e5", "#9ec5f4", "#f0efec", "#f4b4b3", "#e34948", "#a32726"]

# ---- shared scales, so the same group gets the same color in every chart ----
METRO_SCALE = alt.Scale(domain=["Metro", "Nonmetro"], range=["#2a78d6", "#eb6834"])
QUARTILE_SCALE = alt.Scale(domain=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"],
                           range=["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
EV_TYPE_SCALE = alt.Scale(domain=["BEV", "PHEV"], range=["#1baf7a", "#6250d6"])


def seq_scale():
    return alt.Scale(range=SEQUENTIAL)


def diverging_scale(mid):
    return alt.Scale(range=DIVERGING, domainMid=mid)


# ---- sizes and number formats ----
SIZE = {"width": 560, "height": 340}
MAP = {"width": 560, "height": 360}
ONE_DP = ".1f"
DOLLARS = "$,.0f"


def title(text, subtitle=None):
    """Takeaway as the title, what is plotted as the subtitle."""
    return alt.Title(text, subtitle=subtitle) if subtitle else alt.Title(text)


def save(chart, name, folder="figures", scale=3):
    """Save a high-resolution PNG (needs vl-convert-python)."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.png")
    chart.save(path, scale_factor=scale)
    return path


# ---- the theme itself ----
def _theme():
    font = "Helvetica Neue, Helvetica, Arial, Liberation Sans, sans-serif"
    return {"config": {
        "background": "#ffffff",
        "padding": 12,
        "font": font,
        "view": {"stroke": None, "continuousWidth": 560, "continuousHeight": 340},
        "title": {"anchor": "start", "fontSize": 18, "fontWeight": 600, "color": TEXT,
                  "subtitleFontSize": 13, "subtitleColor": MUTED, "subtitlePadding": 4, "offset": 14},
        "axis": {"labelFontSize": 12, "labelColor": MUTED, "titleFontSize": 13, "titleFontWeight": "normal",
                 "titleColor": MUTED, "titlePadding": 8, "gridColor": "#e8e7e3", "domainColor": "#bdbcb6",
                 "tickColor": "#bdbcb6", "labelPadding": 4},
        "axisX": {"grid": False},
        "axisY": {"domain": False, "ticks": False},
        "axisBand": {"grid": False},
        "legend": {"labelFontSize": 12, "labelColor": MUTED, "titleFontSize": 12, "titleColor": MUTED,
                   "titleFontWeight": "normal", "symbolSize": 90, "orient": "top", "direction": "horizontal"},
        "header": {"labelFontSize": 13, "labelColor": TEXT, "titleFontSize": 13},
        "range": {"category": CATEGORY, "ordinal": ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"],
                  "ramp": SEQUENTIAL, "heatmap": SEQUENTIAL, "diverging": DIVERGING},
        "line": {"strokeWidth": 2.5},
        "point": {"size": 70, "filled": True},
        "circle": {"size": 70, "opacity": 0.9},
        "bar": {"cornerRadiusEnd": 3, "color": BLUE},
        "area": {"color": BLUE, "opacity": 0.8},
        "rule": {"color": "#bdbcb6"},
        "text": {"fontSize": 12, "color": MUTED},
        "geoshape": {"stroke": "white", "strokeWidth": 0.8},
        "mark": {"color": BLUE},
    }}


if hasattr(alt, "theme") and hasattr(alt.theme, "register"):   # Altair 5.5+
    alt.theme.register("ev", enable=True)(_theme)
else:                                                          # older Altair
    alt.themes.register("ev", _theme)
    alt.themes.enable("ev")
