import datetime 
from datetime import date
import pandas

df = pandas.read_table('metadata.tsv', dtype={'country': str, 'date': str}, usecols={'country','date'}, sep='\t')

df['date'] = df['date'].replace({"XX":"01"}, regex=True)
df.columns = ['date', 'location']

print(df.head())
df['date'] = pandas.to_datetime(df['date'])

df['date'] = df['date'].dt.to_period('M')

df = df.groupby(['date','location']).size().to_frame('sequences')

df.to_csv('metadata_grouped.tsv', sep = '\t', header = True )


