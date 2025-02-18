import sys
import json

import pandas as pd 

from functools import reduce
from datetime import datetime, timedelta

from utils import get_country_code

TIME_CUTOFF_DAYS = 2 * 365
RECORD_LIMIT_CUTOFF = 20

def format_date(dates):
    return dates.dt.strftime("%Y-%m-%d")

def filter_df(df, dfs):
    # Only get marathons with enough records
    record_count = df.groupby("City").size().reset_index(name="Record Count")
    record_count = record_count[record_count["Record Count"] >= RECORD_LIMIT_CUTOFF]

    # Make sure we get marathons that are still happening
    date_cutoff = datetime.today() - timedelta(days=TIME_CUTOFF_DAYS)
    last_record = df.groupby("City")["Date"].max().reset_index(name="Last Record")
    last_record = last_record[last_record["Last Record"] >= date_cutoff]   

    dfs = dfs + [record_count, last_record]    
    merged_df = reduce(lambda left, right: pd.merge(left, right, on="City", how="inner"), dfs)
    
    merged_df.drop("Last Record", axis=1, inplace=True)
    
    return merged_df

def get_metadata(df, metadata_output_file):
    count_by_gender = df.groupby(['City', 'Gender'])\
        .agg(unique_count=('Name', 'nunique'))\
        .reset_index()\
        .rename(columns={'unique_count': 'People Count By Gender'})

    gender_count = count_by_gender.pivot(
        index='City', 
        columns='Gender', 
        values='People Count By Gender'
    ).reset_index()
    gender_count.columns.name = None
    
    country_count = df.groupby("City")["Country"].nunique().reset_index(name="Country Count")
    people_count = df.groupby("City")["Name"].nunique().reset_index(name="People Count")

    df = filter_df(df, [people_count, country_count, gender_count])
    
    with open(r"data/marathon_dates.json", "r") as f:
        marathon_dates = json.load(f)
        
    df["Date"] = df["City"].map(marathon_dates)
    df["Country"] = df["City"].apply(lambda x: get_country_code(x))

    df.to_json(
        metadata_output_file, 
        orient="records",
        indent=2,
    )

def get_latest_times(df, latest_times_output):
    idx = df.groupby(["City", "Gender"])["Date"].idxmax()
    
    latest_times = df.loc[idx][["Time", "Name", "Country", "City", "Date", "Year", "Gender"]]
    latest_times["Date"] = format_date(df["Date"])
    
    latest_times = filter_df(df, [latest_times])
    
    latest_times.to_json(
        latest_times_output, 
        orient="records",
        indent=2,
    )

def get_best_times(df, best_times_output):
    df["Running Time"] = df["Time"].apply(pd.to_datetime, errors="coerce")
    idx = df.groupby(["City", "Gender"])["Running Time"].idxmin()
    
    best_times = df.loc[idx][["Time", "Name", "Country", "City", "Date", "Year", "Gender"]]
    best_times["Date"] = format_date(df["Date"])
    
    best_times = filter_df(df, [best_times])
    
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