import sys
import json

import pandas as pd 

from functools import reduce
from utils import get_country_code

RECORD_LIMIT_CUTOFF = 20

def main(marathon_data, marathon_dates, cities_file, output_file):
    df = pd.read_csv(marathon_data)
    
    df = df[df['Event'] == 'Marathon']
    
    record_count = df.groupby('City').size().reset_index(name='Record Count')
    country_count = df.groupby('City')['Country'].nunique().reset_index(name='Country Count')
    people_count = df.groupby('City')['Name'].nunique().reset_index(name='People Count')

    marathon_summary = [record_count, country_count, people_count]
    merged_df = reduce(lambda left, right: pd.merge(left, right, on='City', how='outer'), marathon_summary)

    # merged_df['Country'] = merged_df['City'].apply(lambda x: get_country_code(x))
    
    merged_df = merged_df[merged_df['Record Count'] >= RECORD_LIMIT_CUTOFF]
    merged_df['City'].to_csv(cities_file, index=False) 
    
    with open(marathon_dates, "r") as f:
        marathon_dates = json.load(f)
        
    merged_df['Date'] = merged_df['City'].map(marathon_dates)

    merged_df.to_json(
        output_file, 
        orient='records',
        indent=2,
    )

if __name__ == "__main__":
    main(*sys.argv[1:])