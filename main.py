from os.path import exists
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import surveydatacategories as cat
import numpy as np
import datetime
import create_survey_data
import create_map_data

if __name__ == '__main__':
    # Load processed survey data
    if exists(r'.\data\survey_data.csv'):
        df_survey = pd.read_csv(r'.\data\survey_data.csv')
    else:
        create_survey_data.process()
        df_survey = pd.read_csv(r'.\data\survey_data.csv')

    # Convert the DateTime column to a datetime
    df_survey['DateTime'] = pd.to_datetime(df_survey['DateTime'])

    # Load processed choropleth map data
    if exists(r'.\data\map_data.csv'):
        df_map = pd.read_csv(r'.\data\map_data.csv')
    else:
        create_map_data.process()
        df_map = pd.read_csv(r'.\data\map_data.csv')

    # Plot the figures
    # Plot the employment activities by year
    print('Creating Employment Activity by Year Chart')
    # Create the axis data points
    data_times = df_survey['DateTime'][(df_survey['Seasonally Adjusted']) &
                                       (df_survey['Industry'] == 'Total Non-Farm') &
                                       (df_survey['State'] == 'Total US') &
                                       (df_survey['Number Employees'] == 'All') &
                                       (df_survey['Activity Type'] == 'Quits') &
                                       (df_survey['Data Type'] == 'Level') &
                                       (df_survey['Is Monthly']) &
                                       (df_survey['year'] >= 2019)]
    data_quits = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                    (df_survey['Industry'] == 'Total Non-Farm') &
                                    (df_survey['State'] == 'Total US') &
                                    (df_survey['Number Employees'] == 'All') &
                                    (df_survey['Activity Type'] == 'Quits') &
                                    (df_survey['Data Type'] == 'Level') &
                                    (df_survey['Is Monthly']) &
                                    (df_survey['year'] >= 2019)]
    data_hires = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                    (df_survey['Industry'] == 'Total Non-Farm') &
                                    (df_survey['State'] == 'Total US') &
                                    (df_survey['Number Employees'] == 'All') &
                                    (df_survey['Activity Type'] == 'Hires') &
                                    (df_survey['Data Type'] == 'Level') &
                                    (df_survey['Is Monthly']) &
                                    (df_survey['year'] >= 2019)]
    data_openings = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                       (df_survey['Industry'] == 'Total Non-Farm') &
                                       (df_survey['State'] == 'Total US') &
                                       (df_survey['Number Employees'] == 'All') &
                                       (df_survey['Activity Type'] == 'Job Openings') &
                                       (df_survey['Data Type'] == 'Level') &
                                       (df_survey['Is Monthly']) &
                                       (df_survey['year'] >= 2019)]
    data_times = pd.to_datetime(data_times)

    # Create the figure and configure the baseline properties
    fig, ax = plt.subplots(1, figsize=(11, 8.5), dpi=400)
    ax.set_title("Employment Activity by Year")
    ax.set_ylabel("Number of Employees\n(in thousands)")
    ax.grid(which='major', color='lightgrey', linestyle=':', linewidth=0.5)
    ax.grid(which='minor', color='lightgrey', linestyle=':', linewidth=0.5)
    ax.set_ylim(ymin=0, ymax=14000)
    ax.set_xlim(xmin=mdates.date2num(datetime.datetime(2019, 1, 1)),
                xmax=mdates.date2num(datetime.datetime(2021, 8, 1)))

    # Format the datetime x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y-%m'))

    # Draw the data points and legend
    ax.plot(data_times, data_quits, label="Resignations")
    ax.plot(data_times, data_hires, label="New Hires")
    ax.plot(data_times, data_openings, label="Job Openings")
    ax.fill_betweenx(range(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]), 1),
                     mdates.date2num(datetime.datetime(2020, 2, 1)),
                     mdates.date2num(datetime.datetime(2020, 5, 1)),
                     color='lightgrey', alpha=0.5, label='Massive Layoffs')
    ax.legend(loc="best")

    # Rotate the x-axis labels
    for tick in ax.get_xticklabels(which='both'):
        tick.set_rotation(80)

    # Annotate the chart
    ax.annotate('Source: $\it{U.S.\ Bureau\ of\ Labor\ Statistics\ Job\ Openings\ and\ Labor\ Turnover\ Survey}$',
                xy=(mdates.date2num(datetime.datetime(2019, 1, 1)), 0), xytext=(-75, -65),
                textcoords='offset points', color="black", fontsize=8)
    ax.axvline(x=mdates.date2num(datetime.datetime(2020, 1, 1)), color='darkgrey', linestyle='dotted')
    ax.axvline(x=mdates.date2num(datetime.datetime(2020, 3, 1)), color='darkgrey', linestyle='dotted')
    ax.axvline(x=mdates.date2num(datetime.datetime(2020, 12, 1)), color='darkgrey', linestyle='dotted')
    ax.axvline(x=mdates.date2num(datetime.datetime(2021, 4, 1)), color='darkgrey', linestyle='dotted')
    ax.annotate("First Confirmed U.S. Case of COVID-19",
                xy=(mdates.date2num(datetime.datetime(2020, 1, 1)), ax.get_ylim()[1]), xytext=(-2, -158),
                textcoords='offset points', color="black", fontsize=8, rotation=90, ha='right')
    ax.annotate("CARES Act Signed\nCOVID-19 Quarantine Begins",
                xy=(mdates.date2num(datetime.datetime(2020, 3, 1)), ax.get_ylim()[1]), xytext=(-2, -121),
                textcoords='offset points', color="black", fontsize=8, rotation=90, ha='right')
    ax.annotate("COVID-19 Vaccines Available",
                xy=(mdates.date2num(datetime.datetime(2020, 12, 1)), ax.get_ylim()[1]), xytext=(-2, -120),
                textcoords='offset points', color="black", fontsize=8, rotation=90, ha='right')
    ax.annotate("COVID-19 Restrictions Eased",
                xy=(mdates.date2num(datetime.datetime(2021, 4, 1)), ax.get_ylim()[1]), xytext=(-2, -120),
                textcoords='offset points', color="black", fontsize=8, rotation=90, ha='right')

    # Plot employment activities by industry
    print('Creating Employment Activity by Industry Chart')
    # Create lists for the axis data points
    data_industry_quits = []
    data_industry_hires = []
    data_industry_openings = []
    data_industry = []
    # Exclude redundant industry data points
    exclude = ['Total Non-Farm', 'Total Private', 'Durable Goods Manufacturing', 'Non-durable Goods Manufacturing',
               'Trade, Transportation, and Utilities', 'Financial Activities', 'Information',
               'Education and Health Services', 'Leisure and Hospitality', 'Other Services', 'Federal',
               'State and Local', 'State and Local Government Education',
               'State and Local Government, Excluding Education']
    # Populate the axis data points
    for industry in cat.industry.values():
        if industry not in exclude:
            data_industry.append(industry)
            quits = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                       (df_survey['Industry'] == industry) &
                                       (df_survey['State'] == 'Total US') &
                                       (df_survey['Number Employees'] == 'All') &
                                       (df_survey['Activity Type'] == 'Quits') &
                                       (df_survey['Data Type'] == 'Level') &
                                       (df_survey['Is Monthly']) &
                                       (df_survey['DateTime'] == datetime.datetime(2021, 8, 1))]
            hires = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                       (df_survey['Industry'] == industry) &
                                       (df_survey['State'] == 'Total US') &
                                       (df_survey['Number Employees'] == 'All') &
                                       (df_survey['Activity Type'] == 'Hires') &
                                       (df_survey['Data Type'] == 'Level') &
                                       (df_survey['Is Monthly']) &
                                       (df_survey['DateTime'] == datetime.datetime(2021, 8, 1))]
            openings = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                          (df_survey['Industry'] == industry) &
                                          (df_survey['State'] == 'Total US') &
                                          (df_survey['Number Employees'] == 'All') &
                                          (df_survey['Activity Type'] == 'Job Openings') &
                                          (df_survey['Data Type'] == 'Level') &
                                          (df_survey['Is Monthly']) &
                                          (df_survey['DateTime'] == datetime.datetime(2021, 8, 1))]
            data_industry_quits.append(quits.tolist()[0])
            data_industry_hires.append(hires.tolist()[0])
            data_industry_openings.append(openings.tolist()[0])

    # Create buffer data points that will not appear when x margin is zoomed
    # Ensure the shaded area under the job openings line reaches the left and right y-axis
    data_industry.append('Start Line')
    data_industry.append('End LIne')
    data_industry_openings.append(max(data_industry_openings) + 1)
    data_industry_openings.append(0)
    data_industry_quits.append(None)
    data_industry_quits.append(None)
    data_industry_hires.append(None)
    data_industry_hires.append(None)

    # Put the axis data points into a data frame and sort by job openings
    frame = {'Industry': data_industry,
             'Quits': data_industry_quits,
             'Hires': data_industry_hires,
             'Openings': data_industry_openings}
    df_industry = pd.DataFrame(frame)
    df_industry.sort_values('Openings', ascending=False, inplace=True)

    # Create the figure and configure baseline attributes
    fig2, ax2 = plt.subplots(1, figsize=(11, 8.5), dpi=400)
    ax2.set_title("Employment Activity by Industry in August 2021")
    ax2.set_ylabel("Number of Employees\n(in thousands)")
    ax2.set_ylim(ymin=0, ymax=max(data_industry_openings) + 30)

    # Set the column info for the grouped bar chart
    num_column_groups = len(df_industry['Industry'])
    column_group_pos = np.arange(num_column_groups)
    width = 0.3
    ax2.set_xticks(column_group_pos + width / 2)
    ax2.set_xticklabels(df_industry['Industry'], rotation=80, ha='center')
    ax2.tick_params(axis="x", which="both", bottom=False)

    # Shorten the chart box so the x-axis tick labels can fit on the figure
    chartBox = ax.get_position()
    ax2.set_position([chartBox.x0, chartBox.y0 + chartBox.height * .2,
                     chartBox.width,
                     chartBox.height * .8])
    # Set the margins so the chart reaches to the edges of each axis and zooms in past the buffer data
    ax2.margins(x=-0.02, y=0)

    # Draw the data points and legends
    ax2.fill_between(ax2.get_xticks(), df_industry['Openings'], color='honeydew')
    ax2.bar(column_group_pos, df_industry['Quits'], width, label="Resignations")
    ax2.bar(column_group_pos + width, df_industry['Hires'], width, label="New Hires")
    ax2.plot(ax2.get_xticks(), df_industry['Openings'], color='green', label='Job Openings')
    ax2.legend(loc='best')

    # Annotate the chart
    ax2.annotate('Source: $\it{U.S.\ Bureau\ of\ Labor\ Statistics\ Job\ Openings\ and\ Labor\ Turnover\ Survey}$',
                 xy=(1, 0), xytext=(-75, -118), textcoords='offset points', color="black", fontsize=8)

    # Plot resignations by company size
    print('Creating Resignations by Company Size Chart')
    # Create lists for the axis data points
    data_employees_quits = []
    data_employees_hires = []
    data_employees_openings = []
    data_employees = []
    # Exclude redundant employee count data points
    exclude = ['All']
    # Populate the axis data points
    for employees in cat.num_employees.values():
        if employees not in exclude:
            data_employees.append(employees)
            quits = df_survey['value'][(df_survey['Seasonally Adjusted']) &
                                       (df_survey['Industry'] == 'Total Private') &
                                       (df_survey['State'] == 'Total US') &
                                       (df_survey['Number Employees'] == employees) &
                                       (df_survey['Activity Type'] == 'Quits') &
                                       (df_survey['Data Type'] == 'Level') &
                                       (df_survey['Is Monthly']) &
                                       (df_survey['DateTime'] == datetime.datetime(2021, 8, 1))]
            data_employees_quits.append(quits.tolist()[0])

    # Put the axis data points into a data frame
    frame = {'Num Employees': data_employees,
             'Quits': data_employees_quits}
    df_employees = pd.DataFrame(frame)

    # Create the figure and configure baseline attributes
    fig3, ax3 = plt.subplots(1, figsize=(11, 8.5), dpi=400)
    ax3.set_title("Resignations by Employer Size in August 2021")
    ax3.set_ylabel("Number of Employees")
    ax3.set_xlabel("Number of Resignations (in thousands)")
    ax3.tick_params(axis="y", which="both", left=False)

    # Draw the data point and legend
    ax3.barh(df_employees['Num Employees'], df_employees['Quits'], width)

    # Annotate the chart
    ax3.annotate('Source: $\it{U.S.\ Bureau\ of\ Labor\ Statistics\ Job\ Openings\ and\ Labor\ Turnover\ Survey}$',
                 xy=(0, 0), xytext=(-75, -75), textcoords='offset points', color="black", fontsize=8)

    # Plot the labor participation rate choropleth map
    print('Creating Choropleth Charts')
    fig4, ax4 = plt.subplots(2, 1, figsize=(11, 8.5), dpi=400)
    fig4.suptitle('Unemployment Rate by State', fontsize=20)
    world = gpd.read_file(r'.\data\shape files\cb_2018_us_state_5m.shp')

    # Extract the labor participation rate data by state FP
    data_value_aug = df_map['value'][(df_map['Measure'] == 'Unemployment Rate') &
                                     (df_map['year'] == 2021) &
                                     (df_map['period'] == 'M08')]
    data_area_aug = df_map['Area'][(df_map['Measure'] == 'Unemployment Rate') &
                                   (df_map['year'] == 2021) &
                                   (df_map['period'] == 'M08')]
    data_value_apr = df_map['value'][(df_map['Measure'] == 'Unemployment Rate') &
                                     (df_map['year'] == 2021) &
                                     (df_map['period'] == 'M04')]
    data_area_apr = df_map['Area'][(df_map['Measure'] == 'Unemployment Rate') &
                                   (df_map['year'] == 2021) &
                                   (df_map['period'] == 'M04')]

    # Fill in the missing state FP values with None so the length matches with the world state FP
    data_area_list_aug = data_area_aug.to_list()
    data_value_list_aug = data_value_aug.to_list()
    data_area_list_apr = data_area_apr.to_list()
    data_value_list_apr = data_value_apr.to_list()

    # Save the min, max, and center values across each month
    max_value = max(max(data_value_list_apr), max(data_value_list_aug))
    min_value = min(min(data_value_list_apr), min(data_value_list_aug))
    center_value = max_value - (max_value - min_value / 2)

    # Fill in all but two missing state FP values
    for i in range(len(data_area_aug), len(world['STATEFP']) - 2, 1):
        data_area_list_aug.append(None)
        data_value_list_aug.append(None)
        data_area_list_apr.append(None)
        data_value_list_apr.append(None)

    # Use the remaining two missing state FP values to make the legend the same on both maps
    data_area_list_aug.append(None)
    data_value_list_aug.append(max_value)
    data_area_list_apr.append(None)
    data_value_list_apr.append(max_value)
    data_area_list_aug.append(None)
    data_value_list_aug.append(min_value)
    data_area_list_apr.append(None)
    data_value_list_apr.append(min_value)

    # Put the labor participation ratio data into a data frame and sort by state FP
    frame_aug = {'Area': data_area_list_aug,
                 'Value': data_value_list_aug}
    df_map_values_aug = pd.DataFrame(frame_aug)
    df_map_values_aug.sort_values('Area', inplace=True)

    frame_apr = {'Area': data_area_list_apr,
                 'Value': data_value_list_apr}
    df_map_values_apr = pd.DataFrame(frame_apr)
    df_map_values_apr.sort_values('Area', inplace=True)

    # Sort the worlds data by state FP to align it with the labor data
    world.sort_values('STATEFP', inplace=True)
    # Add in the labor data to to the world
    world['Value Apr'] = df_map_values_apr['Value'].to_list()
    world['Value Aug'] = df_map_values_aug['Value'].to_list()

    # Plot the choropleths
    ax4[0] = world.plot('Value Apr', ax=ax4[0], legend=True, edgecolor='black', cmap='coolwarm')
    ax4[0].set_title('April 2021', fontsize=20)
    ax4[0].spines['top'].set_visible(False)
    ax4[0].spines['bottom'].set_visible(False)
    ax4[0].spines['right'].set_visible(False)
    ax4[0].spines['left'].set_visible(False)
    ax4[0].get_xaxis().set_visible(False)
    ax4[0].get_yaxis().set_visible(False)
    ax4[0].set_ylim(ymin=24, ymax=50)
    ax4[0].set_xlim(xmin=-126, xmax=-66)

    ax4[1] = world.plot('Value Aug', ax=ax4[1], legend=True, edgecolor='black', cmap='coolwarm')
    ax4[1].set_title('August 2021', fontsize=20)
    ax4[1].spines['top'].set_visible(False)
    ax4[1].spines['bottom'].set_visible(False)
    ax4[1].spines['right'].set_visible(False)
    ax4[1].spines['left'].set_visible(False)
    ax4[1].get_xaxis().set_visible(False)
    ax4[1].get_yaxis().set_visible(False)
    ax4[1].set_ylim(ymin=24, ymax=50)
    ax4[1].set_xlim(xmin=-126, xmax=-66)

    # Annotate the choropleth figure
    ax4[1].annotate('Source: $\it{U.S.\ Bureau\ of\ Labor\ Statistics\ Local\ Area\ Unemployment\ Statistics}$',
                    xy=(ax4[1].get_xlim()[0], ax4[1].get_ylim()[0]), xytext=(0, -10),
                    textcoords='offset points', color="black", ha='left')

    # Show and save the figures
    print('Displaying All Charts')
    plt.show()
    print('Saving All Charts')
    fig.savefig(r'.\output\Employment Activity by Year.png')
    fig2.savefig(r'.\output\Employment Activity by Industry.png')
    fig3.savefig(r'.\output\Resignations by Employer Size.png')
    fig4.savefig(r'.\output\Labor Force Participation Rate Choropleth.png')
