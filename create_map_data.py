import pandas as pd
import mapdatacategories as cat


def process():
    print("Loading CSV data")
    df_all = pd.read_csv(r'la.data.0.CurrentU20-24.txt', sep="\t")

    # Clean up column names
    print("Cleaning raw data")
    df_all = df_all.rename(columns={'series_id                     ': 'series_id',
                                    '       value': 'value'})

    # Engineer new features
    series_seasonally_adjusted = df_all.apply(lambda x: True if str(x['series_id'])[2:3] == "S" else False, axis=1)
    series_area = df_all.apply(lambda x: cat.area[str(x['series_id'])[3:18]] if str(x['series_id'])[3:18] in cat.area else 'NA', axis=1)
    series_measure = df_all.apply(lambda x: cat.measure[str(x['series_id'])[19:20]], axis=1)
    df_all['Seasonally Adjusted'] = series_seasonally_adjusted
    df_all['Measure'] = series_measure
    df_all['Area'] = series_area

    # Drop unused columns
    print("Cleaning processed data")
    df_all.drop('footnote_codes', axis=1, inplace=True)
    df_all.drop(df_all[df_all['Area'] == 'NA'].index, inplace=True)

    # Save the processed data
    df_all.to_csv(r'.\data\map_data.csv', index=False)


if __name__ == '__main__':
    process()
