import sys
import pandas as pd 

from functools import reduce

from utils import get_country_code

def main(marathon_data, marathon_dates, output_file):
    df = pd.read_csv(marathon_data)
    df = df[df['Event'] == 'Marathon']

    record_count = df.groupby('City').size().reset_index(name='Record Count')
    country_count = df.groupby('City')['Country'].nunique().reset_index(name='Country Count')
    people_count = df.groupby('City')['Name'].nunique().reset_index(name='People Count')

    marathon_summary = [record_count, country_count, people_count]
    merged_df = reduce(lambda left, right: pd.merge(left, right, on='City', how='outer'), marathon_summary)

    merged_df['Country'] = merged_df['City'].apply(lambda x: get_country_code(x))
    merged_df['Date'] = merged_df['City'].apply(lambda x: marathon_dates[x])

    merged_df.to_json(
        output_file, 
        orient='records',
        indent=2,
    )

if __name__ == "__main__":
    main(*sys.argv[1:])