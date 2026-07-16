# -*- coding: utf-8 -*-
"""Scratch script to add extra parameters to project configs.

Author: twillia2
Date: Wed Jul 15 10:55:19 MDT 2026
"""
import json

from pathlib import Path

import pandas as pd


HOME = Path(__file__).parent
SRCDIR = Path("~/review_datasets/ncdb_fy26").expanduser()
DST = HOME.joinpath("ncdb_fy26.json")
VDST = SRCDIR.joinpath("variable_options.csv")
MODELS = ["ncdb", "taiesm1", "mpiesm12hr", "gfdlcm4", "ecearth3veg",
          "ecearth3cc", "nsrdb", "wtk", "wtk_hrrr",]
YEARS = ["2000", "2010", "2020", "2030", "2040", "2050"]
TECHS = ["osw", "lbw", "upv"]


def parseit(name):
    """Parse the WTK or NSRDB file names."""
    for model in MODELS:
        if model in name:
            break

    decade = "n/a"
    for decade in YEARS:
        if decade in name:
            break

    for tech in TECHS:
        if tech in name:
            break

    period = "future"
    if decade in ["2000", "2010"]:
        period = "historical"

    entry = {
        "model":  model,
        "tech":  tech,
        "decade":  decade,
        "period": period
    }

    return entry


def main():
    """Build a reView project config."""
    config = {
        "project_name": "NCDB - FY26",
        "directory": str(SRCDIR)
    }

    # Get the files and set variables
    variables = {}
    files = list(SRCDIR.glob("*csv"))
    files = [f for f in files if "variable_options" not in f.name]
    files.sort()
    for file in files:
        name = file.stem
        entry = parseit(name)
        variables[name] = entry

    config["variables"] = variables
    with open(DST, "w") as file:
        file.write(json.dumps(config, indent=4))

    df = pd.DataFrame(variables).T
    df = df.reset_index(names="name")
    df.insert(1, "file", files)
    df.to_csv(VDST, index=False)


if __name__ == "__main__":
    main()
