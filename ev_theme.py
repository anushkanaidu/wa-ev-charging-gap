"""
ev_theme.py - shared Altair chart theme for the WA EV final project
====================================================================

Use it at the top of every notebook:

    import altair as alt
    import ev_theme as ev          # registers + turns on the theme

Every Altair chart made after that picks up the same fonts, sizes, axes and
colors automatically. For the colors that MEAN something (metro vs nonmetro,
BEV vs PHEV, income quartiles, maps), use the shared scales below so the same
thing is the same color on every slide:

    color=alt.Color("area_type:N", scale=ev.METRO_SCALE)
    color=alt.Color("income_quartile:N", scale=ev.QUARTILE_SCALE)
    color=alt.Color("ev_type:N", scale=ev.EV_TYPE_SCALE)
    color=alt.Color("evs_per_1000:Q", scale=ev.seq_scale())          # maps
    color=alt.Color("gap_vs_state:Q", scale=ev.diverging_scale(0))    # gap map

Save a high-res PNG for the report and slides (3x = sharp on a projector):

    ev.save(chart, "income_vs_evs")        # -> figures/income_vs_evs.png

Conventions everyone follows
----------------------------
* Title = the takeaway ("Richer counties have more EVs per resident"),
  subtitle = what is plotted + units + year ("EVs per 1,000 residents, Dec 2025").
* Per-resident rates, never raw counts, when comparing counties.
* Direct-label lines (<= 4 series) instead of relying on the legend alone.
* Use ev.SIZE (notebook/report) or ev.SLIDE (16:9 slide) for width/height.
* No dual y-axes. Two measures with different units -> two charts.
* Combining charts with |, &, alt.hconcat or alt.vconcat? Add .resolve_scale(color="independent")
  to EVERY concat (inner rows too), or Altair merges their color scales and mixes up the colors.
"""

import os
import altair as alt

# ----------------------------------------------------------------- fonts & ink
FONT = "Helvetica Neue, Helvetica, Arial, Liberation Sans, sans-serif"
INK = "#0b0b0b"          # titles
INK_2 = "#52514e"        # subtitles, axis labels, annotations
INK_3 = "#8a8983"        # very quiet notes
GRID = "#e8e7e3"
DOMAIN = "#bdbcb6"
BACKGROUND = "#ffffff"
GRAY = "#b4b3ad"         # "everything else" / de-emphasised marks
HIGHLIGHT = "#eb6834"    # one thing you want the eye to land on (use sparingly)

# --------------------------------------------------------- categorical colors
# Fixed order, never cycled. Checked for color-blind safety.
BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
CATEGORICAL = [BLUE, ORANGE, AQUA, "#eda100", "#e87ba4", "#008300", VIOLET, "#e34948"]

# Meaningful colors - the same on every chart in the project
METRO_COLORS = {"Metro": BLUE, "Nonmetro": ORANGE}
EV_TYPE_COLORS = {"BEV": AQUA, "PHEV": VIOLET}      # aqua is light: always direct-label it
METRO_SCALE = alt.Scale(domain=list(METRO_COLORS), range=list(METRO_COLORS.values()))
EV_TYPE_SCALE = alt.Scale(domain=list(EV_TYPE_COLORS), range=list(EV_TYPE_COLORS.values()))

# ----------------------------------------------------- sequential (one hue)
BLUES = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
ORANGES = ["#fde3d6", "#f9c3a8", "#f39e78", "#eb6834", "#c9501f", "#9c3d17", "#6e2a10"]

# Income quartiles: ordered light -> dark (lightest still visible on white)
QUARTILES = ["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
QUARTILE_COLORS = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
QUARTILE_SCALE = alt.Scale(domain=QUARTILES, range=QUARTILE_COLORS)

# ------------------------------------------------- diverging (two hues + gray)
# blue = better than the state (fewer EVs per port), red = worse (more crowded)
DIVERGING = ["#184f95", "#3987e5", "#9ec5f4", "#f0efec", "#f4b4b3", "#e34948", "#a32726"]

# ------------------------------------------------------------- sizes & formats
SIZE = dict(width=560, height=340)      # notebook / report figure
SLIDE = dict(width=760, height=380)     # fills a 16:9 slide with room for a title
MAP = dict(width=560, height=360)       # Washington is wide and short

DOLLARS = "$,.0f"
THOUSANDS = ",.0f"
PCT = ".0%"
ONE_DP = ".1f"


def seq_scale(colors=BLUES, **kw):
    """Sequential color scale for magnitudes (choropleths, heatmaps)."""
    return alt.Scale(range=colors, **kw)


def diverging_scale(midpoint=0, **kw):
    """Diverging scale centred on `midpoint` (e.g. the state average or 0)."""
    return alt.Scale(range=DIVERGING, domainMid=midpoint, **kw)


def title(text, subtitle=None):
    """Takeaway title + quiet subtitle, left-aligned."""
    return alt.Title(text, subtitle=subtitle) if subtitle else alt.Title(text)


# ------------------------------------------------------------------ the theme
def _theme():
    return {
        "config": {
            "background": BACKGROUND,
            "padding": 12,
            "font": FONT,
            "view": {"stroke": None, "continuousWidth": SIZE["width"], "continuousHeight": SIZE["height"]},
            "title": {
                "anchor": "start", "fontSize": 18, "fontWeight": 600, "color": INK,
                "subtitleFontSize": 13, "subtitleColor": INK_2, "subtitlePadding": 4, "offset": 14,
            },
            "axis": {
                "labelFontSize": 12, "labelColor": INK_2, "titleFontSize": 13, "titleFontWeight": "normal",
                "titleColor": INK_2, "titlePadding": 8, "gridColor": GRID, "domainColor": DOMAIN,
                "tickColor": DOMAIN, "labelPadding": 4,
            },
            "axisX": {"grid": False},
            "axisY": {"domain": False, "ticks": False},
            "axisBand": {"grid": False},
            "legend": {
                "labelFontSize": 12, "labelColor": INK_2, "titleFontSize": 12, "titleColor": INK_2,
                "titleFontWeight": "normal", "symbolSize": 90, "orient": "top", "direction": "horizontal",
            },
            "header": {"labelFontSize": 13, "labelColor": INK, "titleFontSize": 13},
            "range": {
                "category": CATEGORICAL,
                "ordinal": QUARTILE_COLORS,
                "ramp": BLUES,
                "heatmap": BLUES,
                "diverging": DIVERGING,
            },
            "line": {"strokeWidth": 2.5},
            "point": {"size": 70, "filled": True},
            "circle": {"size": 70, "opacity": 0.9},
            "bar": {"cornerRadiusEnd": 3, "color": BLUE},
            "area": {"color": BLUE, "opacity": 0.8},
            "rule": {"color": DOMAIN},
            "text": {"fontSize": 12, "color": INK_2},
            "geoshape": {"stroke": "white", "strokeWidth": 0.8},
            "mark": {"color": BLUE},
        }
    }


# Works on Altair 5.5+ / 6 (alt.theme) and older 5.x (alt.themes)
if hasattr(alt, "theme") and hasattr(alt.theme, "register"):
    alt.theme.register("ev_project", enable=True)(_theme)
else:
    alt.themes.register("ev_project", _theme)
    alt.themes.enable("ev_project")


# ------------------------------------------------------------------- export
def save(chart, name, folder="figures", scale=3):
    """Save a high-res PNG (needs: pip install vl-convert-python). Returns the path."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.png")
    chart.save(path, scale_factor=scale)
    return path
