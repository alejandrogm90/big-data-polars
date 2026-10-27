#!/usr/bin/env python3
#
#
#       Copyright 2023 Alejandro Gomez
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import logging.config
import os
import sys

import polars as pl

import src.commons.common_functions as cf

# GLOBALS
FILE_LOOGER = os.path.normpath('config/logging.conf')
FILE_LOG = os.path.normpath("log/" + cf.getFiletName(sys.argv[0]) + ".log")
logging.config.fileConfig(FILE_LOOGER)
LOGGER = logging.getLogger('mainLogger')
today = datetime.date.today()
DATA_SOURCE = "data/iris.csv"


def build_example_1_query(data_source=DATA_SOURCE):
    return (
        pl.scan_csv(data_source)
        .filter(pl.col("sepal_length") > 5)
        .group_by("species")
        .agg(pl.col("sepal_width").mean())
    )


def build_example_2_query(data_source=DATA_SOURCE):
    return (
        pl.scan_csv(data_source)
        .select(pl.col("species"), pl.col("sepal_length"))
        .filter(pl.col("sepal_length") > 7)
    )


def build_example_3_query(data_source=DATA_SOURCE):
    return (
        pl.scan_csv(data_source)
        .select(
            pl.col("species"),
            pl.col("species").count().alias("Total"),
        )
        .unique()
    )


def build_example_4_query(data_source=DATA_SOURCE):
    return (
        pl.scan_csv(data_source)
        .group_by("species")
        .agg(
            pl.col("sepal_length").sum(),
            pl.col("sepal_width").sum(),
            pl.col("petal_length").sum(),
            pl.col("petal_width").sum(),
        )
        .sort("species", descending=True)
    )


if __name__ == '__main__':
    # Add Banner
    cf.printMegaBanner(cf.getFiletName(sys.argv[0], True))
    # Show script info
    info = {
        "name": cf.getFiletName(os.path.realpath(__file__), True),
        "location": os.path.dirname(os.path.realpath(__file__)),
        "description": "Big Data example with polars ",
        "Autor": "Alejandro Gómez",
        "calling": sys.argv[0] + " parameters"
    }
    cf.showScriptInfo(info)

    # Load data from file
    if not os.path.exists(DATA_SOURCE):
        cf.errorMsg(LOGGER, 1, "File {0} do not exists.".format(DATA_SOURCE), FILE_LOG)
    else:
        # Example 1
        cf.infoMsg(LOGGER, "Example 1", FILE_LOG)
        q = build_example_1_query()
        df = q.collect()
        cf.infoMsg(LOGGER, str(df), FILE_LOG)
        # Example 2
        cf.infoMsg(LOGGER, "Example 2", FILE_LOG)
        q_2 = build_example_2_query()
        df_2 = q_2.collect()
        cf.infoMsg(LOGGER, str(df_2), FILE_LOG)
        # Example 3
        cf.infoMsg(LOGGER, "Example 3", FILE_LOG)
        q_3 = build_example_3_query()
        df_3 = q_3.collect()
        cf.infoMsg(LOGGER, str(df_3), FILE_LOG)
        # Example 4
        cf.infoMsg(LOGGER, "Example 4", FILE_LOG)
        q4 = build_example_4_query()
        resultado = q4.collect()
        df_4 = q4.collect()
        cf.infoMsg(LOGGER, str(df_4), FILE_LOG)
        # Write the result to a CSV file
        #df_4.write_csv("data/iris_summary.csv")
