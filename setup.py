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
        q = (pl.scan_csv(DATA_SOURCE).filter(pl.col("sepal_length") > 5).group_by("species").agg(
            pl.col("sepal_width").mean()))
        df = q.collect()
        cf.infoMsg(LOGGER, str(df), FILE_LOG)
