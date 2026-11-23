# WA EV Charging Gap

**DATA 5310 Final Project** · Anushka, Sravya, Hemanth, Hamada

Shared data and chart theme for our project. Everyone loads from here so we all use the same numbers.

## How to load

```python
import pandas as pd

BASE = "https://raw.githubusercontent.com/anushkanaidu/wa-ev-charging-gap/main/"
df = pd.read_csv(BASE + "clean/ev_county_panel.csv")
```

Chart theme:

```python
import urllib.request
urllib.request.urlretrieve(BASE + "ev_theme.py", "ev_theme.py")
import ev_theme as ev
```

## Files

| File | What it is |
|---|---|
| `clean/ev_county_panel.csv` | Main table: one row per county per year (2017–2025). Start here. |
| `data/` | The Homework 8 EDA files the main table is built from, plus the county map and current EV list |
| `ev_theme.py` | Shared colors and chart style |

## Notes

- EVs = passenger EVs registered on Dec 31 each year (no trucks).
- Ports = public Level 2 + DC fast ports.
- Data comes from our Final_EDA notebook, so it matches what we submitted.
