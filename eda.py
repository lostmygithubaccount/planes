# imports
import duckdb
import requests
import pandas as pd
import numpy as np

# connect to database
con = duckdb.connect("eda.duckdb")

# print tables
print(con.execute("show tables;").df())
