import sys
import json

import pandas as pd 

from functools import reduce
from utils import get_country_code, get_athlete_country

def format_date(dates):
    try:
        return dates.dt.strftime("%Y-%m-%d")
    except:
        return None

def get_metadata(df, metadata_output_file):
    count_by_gender = df.groupby(["City", "Gender"])\
        .agg(unique_count=("Name", "nunique"))\
        .reset_index()\
        .rename(columns={"unique_count": "People Count By Gender"})

    gender_count = count_by_gender.pivot(
        index="City", 
        columns="Gender", 
        values="People Count By Gender"
    ).reset_index()
    gender_count.columns.name = None
    
    country_count = df.groupby("City")["Country"].nunique().reset_index(name="Country Count")
    people_count = df.groupby("City")["Name"].nunique().reset_index(name="People Count")

    dfs = [people_count, country_count, gender_count]
    df = reduce(lambda left, right: pd.merge(left, right, on='City', how='inner'), dfs)
    
    df["Country"] = df["City"].apply(lambda x: get_country_code(x))

    df.to_json(
        metadata_output_file, 
        orient="records",
        indent=2,
    )

def get_latest_times(df, latest_times_output):
    idx = df.groupby(["City", "Gender"])["Date"].idxmax()
    
    latest_times = df.loc[idx][["Time", "Name", "Country", "City", "Date", "Year", "Gender"]]
    
    latest_times["Date"] = format_date(latest_times["Date"])
    latest_times["Country"] = latest_times["Country"].apply(get_athlete_country)
    
    latest_times.to_json(
        latest_times_output, 
        orient="records",
        indent=2,
    )

def get_best_times(df, best_times_output):
    df["Running Time"] = df["Time"].apply(pd.to_datetime, errors="coerce")
    idx = df.groupby(["City", "Gender"])["Running Time"].idxmin()
    
    best_times = df.loc[idx][["Time", "Name", "Country", "City", "Date", "Year", "Gender"]]
    
    best_times["Date"] = format_date(best_times["Date"])
    best_times["Country"] = best_times["Country"].apply(get_athlete_country)
    
    best_times.to_json(
        best_times_output, 
        orient="records",
        indent=2
    )
    
def main(marathon_data, metadata_output_file, best_times_output, latest_times_output):
    df = pd.read_csv(marathon_data)
    
    df = df[df["Event"] == "Marathon"]
    
    df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
    df["Year"] = df["Date"].dt.year
    
    get_metadata(df, metadata_output_file)
    get_best_times(df, best_times_output)
    get_latest_times(df, latest_times_output)

if __name__ == "__main__":
    main(*sys.argv[1:])