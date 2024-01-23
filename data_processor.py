import pandas
import datetime
from datetime import date
import numpy as np
import matplotlib.pyplot as mp


# Load and process raw COVID-19 data and returns statistics for each month
def raw_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df_raw = pandas.read_csv(url, dtype={'location': str},
                             usecols={'location', 'date', 'new_cases', 'new_deaths', 'new_tests'})
    df_raw['date'] = pandas.to_datetime(df_raw['date'])
    df_raw.columns = ['location', 'date', 'cases', 'deaths', 'tests']

    df_raw['date'] = df_raw['date'].dt.to_period('M')
    df_raw = df_raw.groupby(['date', 'location']).sum()
    df_raw['percent_positivity'] = df_raw['cases'] / df_raw['tests']
    df_raw['CFR'] = df_raw['deaths'] / df_raw['cases']

    df_raw['percent_positivity'] = df_raw['percent_positivity'].replace([np.inf, -np.inf], np.nan)
    df_raw['CFR'] = df_raw['CFR'].replace([np.inf, -np.inf], np.nan)
    df_raw.to_csv('output/ourworldindata_grouped.csv', na_rep='NaN')

    return df_raw


# Load and process epidemiological model data from https://www.ourworldindata.org
# and returns prevalence estimates for each month
def model_data():
    df_icl = pandas.read_csv('data/daily-new-estimated-covid-19-infections-icl-model.csv', dtype={'Entity': str},
                             usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (ICL, mean)'},
                             parse_dates=['Date'])
    df_ihme = pandas.read_csv('data/daily-new-estimated-covid-19-infections-ihme-model.csv', dtype={'Entity': str},
                              usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (IHME, mean)'},
                              parse_dates=['Date'])
    df_lshtm = pandas.read_csv('data/daily-new-estimated-covid-19-infections-lshtm-model.csv', dtype={'Entity': str},
                               usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (LSHTM, median)'},
                               parse_dates=['Date'])
    df_yyg = pandas.read_csv('data/daily-new-estimated-covid-19-infections-yyg-model.csv', dtype={'Entity': str},
                             usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (YYG, mean)'},
                             parse_dates=['Date'])

    df_icl.columns = ['location', 'date', 'ICL_estimate_mean']
    df_ihme.columns = ['location', 'date', 'IHME_estimate_mean']
    df_lshtm.columns = ['location', 'date', 'LSHTM_estimate_median']
    df_yyg.columns = ['location', 'date', 'YYG_estimate_mean']

    df_icl = df_icl.groupby(['location', 'date'], as_index=False).sum()
    df_ihme = df_ihme.groupby(['location', 'date']).sum().reset_index()
    df_lshtm = df_lshtm.groupby(['location', 'date'], as_index=False).sum()
    df_yyg = df_yyg.groupby(['location', 'date'], as_index=False).sum()

    df_icl_ihme = pandas.merge(df_icl, df_ihme, how='outer', left_on=['location', 'date'],
                               right_on=['location', 'date'])
    df_icl_ihme_lshtm = pandas.merge(df_icl_ihme, df_lshtm, how='outer', left_on=['location', 'date'],
                                     right_on=['location', 'date'])
    df_models = pandas.merge(df_icl_ihme_lshtm, df_yyg, how='outer', left_on=['location', 'date'],
                          right_on=['location', 'date'])

    df_models.to_csv('output/country_estimates.csv', index=False, na_rep='NaN')

    return df_models


def weighted_mean(values, weights):
    return np.average(values, weights=weights)


# Load and process serology data and returns lower bound of serology prevalence estimates for each month
def sero_data():
    serotracker_data = "https://raw.githubusercontent.com/serotracker/sars-cov-2-data/main/serotracker_dataset.csv"
    df_sero = pandas.read_csv(serotracker_data,
                              dtype={'country': str, 'sampling_end_date': str, 'sampling_start_date': str,
                                     'seroprev_95_ci_lower': float, 'denominator_value': int},
                              usecols={'country', 'sampling_start_date', 'sampling_end_date', 'seroprev_95_ci_lower',
                                       'denominator_value'})

    df_sero.columns = ['location', 'start_date', 'end_date', 'participants', 'seroprevalence']

    df_sero['start_date'] = pandas.to_datetime(df_sero['start_date'], format='%Y/%m/%d', errors='coerce')
    df_sero['end_date'] = pandas.to_datetime(df_sero['end_date'], format='%Y/%m/%d', errors='coerce')

    df_sero['start_date'].fillna(df_sero['end_date'], inplace=True)
    df_sero['end_date'].fillna(df_sero['start_date'], inplace=True)

    df_sero['date'] = df_sero['start_date'] + (df_sero['end_date'] - df_sero['start_date']) / 2

    del df_sero['end_date']
    del df_sero['start_date']

    df_sero['participants'].fillna(1, inplace=True)
    df_sero['date'] = df_sero['date'].dt.to_period('M')

    df_sero = df_sero[df_sero['seroprevalence'].notna()]
    df_sero = df_sero[df_sero['participants'].notna()]

    df_sero = df_sero.groupby(['location', 'date'], as_index=False).agg(sero_study_participants=('participants', np.sum),
                                                                        avg_seroprevalence=('seroprevalence',
                                                                                  lambda x: weighted_mean(x,
                                                                                                          df_sero.loc[
                                                                                                              x.index, 'participants'])))
    df_sero.to_csv('sero.csv', header=True, index=False)

    return df_sero


# Load SARS-CoV-2 sequence metadata from https://www.gisaid.org
def sequence_counter():
    df_sequences = pandas.read_table('data/metadata.tsv', dtype={'country': str, 'date': str}, usecols={'country', 'date'}, sep='\t')

    df_sequences['date'] = df_sequences['date'].replace({"XX": "01"}, regex=True)
    df_sequences.columns = ['date', 'location']

    df_sequences['date'] = pandas.to_datetime(df_sequences['date'], errors = 'coerce')
    df_sequences = df_sequences.dropna(subset=['date'])
    df_sequences['date'] = df_sequences['date'].dt.to_period('M')
    df_sequences = df_sequences.groupby(['date', 'location']).size().to_frame('sequences')

    df_sequences.to_csv('output/metadata_grouped.tsv', sep='\t', header=True)
    return df_sequences


# Merge dataframes with all the information and return it
def merge_df(df_raw, df_models, df_sero, df_sequences):
    df_merged = pandas.merge(df_raw, df_sequences, how='left', left_on=['location', 'date'], right_on=['location', 'date'])
    df_merged['sequencing_rate'] = df_merged['sequences'] / df_merged['cases']
    df_merged['sequencing_rate'] = df_merged['sequencing_rate'].replace([np.inf, -np.inf], np.nan)

    df_merged = pandas.merge(df_merged, df_sero, how='left', left_on=['location', 'date'], right_on=['location', 'date'])
    df_merged = pandas.merge(df_merged, df_models, how='left', left_on=['location', 'date'], right_on=['location', 'date'])

    return df_merged


# Filter the dataframes by start and end date in the format YYYY-MM-DD and calculate various statistics
def calc_df(start_date, end_date, df, num_of_seq):
    df = df[df['date'] >= start_date] & df[df['date'] <= end_date]
    months = pandas.date_range(start_date, end_date, freq='MS').strftime("%Y-%m").tolist()
    sequences = {}
    estimates = {}
    cases = {}
    sequences_ideal = {}

    for month in months:
        df.loc[(df['location'] =='World') & (df['date'] == month), 'sequences'] = df.loc[df['date'] == month, 'sequences'].sum()
        sequences[month] = df.loc[(df['location'] == 'World') & (df['date'] == month), 'sequences'].values[0]

        estimates[month] = df.loc[(df['location'] == 'World') & (df['date'] == month), 'IHME_estimate_mean'].values[0]

        df.loc[df['date'] == month, 'sequence_contribution'] = df['sequences'] / sequences[month]

    estimate_all = sum(estimates.values())

    for month in months:
        df.loc[df['date'] == month, 'sequence_contribution'] = df['sequences'] / sequences[month]
        sequences_ideal = estimates[month]/estimate_all * num_of_seq

        df.loc[df['date'] == month, 'estimate_contribution'] = df['IHME_estimate_mean'] / estimates[month]
        df.loc[df['date'] == month, 'ideal_sequences'] = df['estimate_contribution'] * sequences_ideal[month]

        cases[month] = df.loc[(df['location'] == 'World') & (df['date'] == month), 'cases'].values[0]
        df.loc[df['date'] == month, 'case_contribution'] = df['cases'] / cases[month]
        df.loc[df['date'] == month, 'apparent_sequences'] = df['case_contribution'] * sequences_ideal[month]

    df_estimate_outlier = df.loc[df['sequences'] < df['ideal_sequences']]
    df_case_outlier = df.loc[df['sequences'] < df['apparent_sequences']]

    # Create downstream file for Nybbler to perform weighted subsampling
    df_final = df[['location', 'date', 'ideal_sequences']]
    df_final['location'] = df_final['location'].replace(['United States'], 'USA')
    df_final['ideal_sequences'] = df_final['ideal_sequences'].apply(np.ceil)
    df_final = df_final[df_final['location'] != 'World']
    df_final.to_csv('output/country_ideal_sequences.csv', index=False, na_rep='NaN')

    df.to_csv('output/country_all_data.csv', index=False, na_rep='NaN')
    df_estimate_outlier.to_csv('output/country_estimate_outlier_data.csv', index=False, na_rep='NaN')
    df_case_outlier.to_csv('output/country_case_outlier_data.csv', index=False, na_rep='NaN')

    return df

if __name__ == '__main__':
    df_raw = raw_data()
    df_models = model_data()
    df_sero = sero_data()
    df_sequences = sequence_counter()
    df_merged = merge_df(df_raw, df_models, df_sero, df_sequences)
    df = calc_df('2020-02', '2020-10', df_merged, 25000)






