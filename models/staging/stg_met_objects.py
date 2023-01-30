# imports
import modin.pandas as pd


def model(dbt, session):

    # get dependent data
    df = pd.read_csv("csvs/MetObjects.csv")

    # clean column names
    cols = list(df.columns)
    cols = [c.lower().replace(" ", "_") for c in cols]
    df.columns = cols

    # return model
    return df._to_pandas()
