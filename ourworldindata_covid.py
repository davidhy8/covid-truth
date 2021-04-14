import pandas
import datetime
from datetime import date
import numpy as np


url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'


df = pandas.read_csv(url, dtype={'location': str}, usecols={'location', 'date','new_cases','new_deaths','new_tests'})
df['date'] = pandas.to_datetime(df['date'])
df.columns = ['location', 'date', 'cases', 'deaths', 'tests']


df2 = pandas.DataFrame(columns=df.columns)
df2 = df[['location','date','cases','deaths','tests']]


df2['date'] = df2['date'].dt.to_period('M')
df2 = df2.groupby(['date','location']).sum()


df2['percent_positivity'] = df2['cases']/df2['tests']
df2['CFR'] = df2['deaths']/df2['cases']


df2['percent_positivity'] = df2['percent_positivity'].replace([np.inf, -np.inf], np.nan)
df2['CFR'] = df2['CFR'].replace([np.inf, -np.inf], np.nan)

print(df2.head)


df2.to_csv('ourworldindata_grouped.csv', na_rep='NaN')
