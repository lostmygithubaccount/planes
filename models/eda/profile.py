# imports
import pandas as pd

from pandas_profiling import ProfileReport

OUT = "eda.html"

# define dbt model
def model(dbt, session):

    # get dependent data
    df = dbt.ref("stg_met_objects").df()

    # clean column names
    profile = ProfileReport(df, title="profile", minimal=True)

    profile.to_file(OUT)

    # return model
    return pd.DataFrame([OUT], columns=["file"])
