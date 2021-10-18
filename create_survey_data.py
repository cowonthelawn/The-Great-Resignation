import pandas as pd
import surveydatacategories as cat


def process():
    print("Loading CSV data")
    df_all = pd.read_csv(r'https://download.bls.gov/pub/time.series/jt/jt.data.1.AllItems', sep="\t")

    # Clean up column names
    print("Cleaning data")
    df_all = df_all.rename(columns={'       value': 'value',
                                    'series_id                     ': 'series_id'})

    # Drop unused column
    df_all.drop('footnote_codes', axis=1, inplace=True)

    # Engineer new features
    print("Engineering new features")
    # Parse the series_id column value and break it out into multiple columns
    series_seasonally_adjusted = df_all.apply(lambda x: True if str(x['series_id'])[2:3] == "S" else False, axis=1)
    series_industry = df_all.apply(lambda x: cat.industry[str(x['series_id'])[3:9]], axis=1)
    series_state = df_all.apply(lambda x: cat.state[str(x['series_id'])[9:11]], axis=1)
    series_num_employees = df_all.apply(lambda x: cat.num_employees[str(x['series_id'])[16:18]], axis=1)
    series_activity_type = df_all.apply(lambda x: cat.activity_type[str(x['series_id'])[18:20]], axis=1)
    series_data_type = df_all.apply(lambda x: cat.data_type[str(x['series_id'])[20:21]], axis=1)
    df_all["Seasonally Adjusted"] = series_seasonally_adjusted
    df_all["Industry"] = series_industry
    df_all["State"] = series_state
    df_all["Number Employees"] = series_num_employees
    df_all["Activity Type"] = series_activity_type
    df_all["Data Type"] = series_data_type

    # Categorize if the period is annual or monthly
    series_monthly = df_all.apply(lambda x: True if str(x['period']) != 'M13' else False, axis=1)
    df_all['Is Monthly'] = series_monthly

    # Engineer a datetime column
    series_datetime = df_all.apply(
        lambda x: str(x['year']) + '-' + str(x['period']).replace('M', '') + '-01' if str(x['period']) != 'M13'
        else str(x['year']), axis=1)
    df_all['DateTime'] = pd.to_datetime(series_datetime)

    # Save the processed data
    df_all.to_csv(r'.\data\survey_data.csv')


if __name__ == '__main__':
    process()
