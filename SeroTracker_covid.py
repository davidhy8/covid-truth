import pandas
import numpy as np


df_sero = pandas.read_csv('SeroTracker.csv', dtype={'Country':  str,  'Study Dates' : str, 'Seroprevalence (95% CI)':  str}, usecols={'Country','Study Dates', 'Seroprevalence (95% CI)','Denominator Value'})


df_sero.columns = ['location', 'date', 'participants', 'seroprevalence']


df_sero['end_date'] = df_sero['date'].str.split().str[-1]
df_sero['date'] = df_sero['date'].str.split().str[0]


df_sero['end_date'] = "2020/" + df_sero['end_date']
df_sero['date'] = '2020/' + df_sero['date']


df_sero['date'] = pandas.to_datetime(df_sero['date'], format='%Y/%m/%d', errors='coerce')
df_sero['end_date'] = pandas.to_datetime(df_sero['end_date'], format='%Y/%m/%d', errors='coerce')


df_sero['date'].fillna(df_sero['end_date'],inplace=True)
df_sero['end_date'].fillna(df_sero['date'],inplace=True)


df_sero['date'] = df_sero['date'] + (df_sero['end_date']-df_sero['date'])/2


del df_sero['end_date']


df_sero['seroprevalence'] = df_sero['seroprevalence'].str.split().str[0]


df_sero['seroprevalence'] = df_sero['seroprevalence'].astype(str).str.replace('%','')


df_sero['participants'].fillna(1, inplace=True)


df_sero['date'] = df_sero['date'].dt.to_period('M')


df_sero.to_csv('sero.csv',header = True, index=False)
