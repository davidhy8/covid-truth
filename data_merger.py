import pandas
import numpy as np
import matplotlib.pyplot as mp


genomes = 'metadata_grouped.tsv'
countries = 'ourworldindata_grouped.csv'


df_genomes = pandas.read_table(genomes)
df_countries = pandas.read_csv(countries)


df_merged = pandas.merge(df_countries, df_genomes, how='left', left_on=['location','date'], right_on=['location','date'])
df_merged['sequencing_rate'] = df_merged['sequences']/df_merged['cases']
df_merged['sequencing_rate'] = df_merged['sequencing_rate'].replace([np.inf, -np.inf], np.nan)


#df_country = df_merged
df_sero = pandas.read_csv('new_sero.csv')
df_estimates = pandas.read_csv('country_estimates.csv')


df_sero.columns = ['location', 'date', 'sero_study_participants', 'avg_seroprevalence']


df_merged = pandas.merge(df_merged, df_sero, how='left', left_on=['location', 'date'], right_on=['location', 'date'])
df_merged = pandas.merge(df_merged, df_estimates, how='left', left_on=['location', 'date'], right_on=['location','date'])
#df_merged.to_csv('country_data.csv', na_rep = 'NaN', index=False)


df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-02'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-02', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-03'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-03', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-04'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-04', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-05'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-05', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-06'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-06', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-07'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-07', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-08'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-08', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-09'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-09', 'sequences'].sum()
df_merged.loc[(df_merged['location'] =='World') & (df_merged['date'] == '2020-10'), 'sequences'] = df_merged.loc[df_merged['date'] == '2020-10', 'sequences'].sum()


sequence_2020_02 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-02'), 'sequences'].values[0]
sequence_2020_03 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-03'), 'sequences'].values[0]
sequence_2020_04 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-04'), 'sequences'].values[0]
sequence_2020_05 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-05'), 'sequences'].values[0]
sequence_2020_06 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-06'), 'sequences'].values[0]
sequence_2020_07 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-07'), 'sequences'].values[0]
sequence_2020_08 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-08'), 'sequences'].values[0]
sequence_2020_09 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-09'), 'sequences'].values[0]
sequence_2020_10 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-10'), 'sequences'].values[0]

estimate_2020_02 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-02'), 'IHME_estimate_mean'].values[0]
estimate_2020_03 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-03'), 'IHME_estimate_mean'].values[0]
estimate_2020_04 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-04'), 'IHME_estimate_mean'].values[0]
estimate_2020_05 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-05'), 'IHME_estimate_mean'].values[0]
estimate_2020_06 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-06'), 'IHME_estimate_mean'].values[0]
estimate_2020_07 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-07'), 'IHME_estimate_mean'].values[0]
estimate_2020_08 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-08'), 'IHME_estimate_mean'].values[0]
estimate_2020_09 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-09'), 'IHME_estimate_mean'].values[0]
estimate_2020_10 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-10'), 'IHME_estimate_mean'].values[0]

estimate_all = estimate_2020_02 + estimate_2020_03 + estimate_2020_04 + estimate_2020_05 + estimate_2020_06 + estimate_2020_07 + estimate_2020_08 + estimate_2020_09 + estimate_2020_10


df_merged.loc[df_merged['date'] == '2020-02','sequence_contribution'] = df_merged['sequences']/sequence_2020_02
df_merged.loc[df_merged['date'] == '2020-03','sequence_contribution'] = df_merged['sequences']/sequence_2020_03
df_merged.loc[df_merged['date'] == '2020-04','sequence_contribution'] = df_merged['sequences']/sequence_2020_04
df_merged.loc[df_merged['date'] == '2020-05','sequence_contribution'] = df_merged['sequences']/sequence_2020_05
df_merged.loc[df_merged['date'] == '2020-06','sequence_contribution'] = df_merged['sequences']/sequence_2020_06
df_merged.loc[df_merged['date'] == '2020-07','sequence_contribution'] = df_merged['sequences']/sequence_2020_07
df_merged.loc[df_merged['date'] == '2020-08','sequence_contribution'] = df_merged['sequences']/sequence_2020_08
df_merged.loc[df_merged['date'] == '2020-09','sequence_contribution'] = df_merged['sequences']/sequence_2020_09
df_merged.loc[df_merged['date'] == '2020-10','sequence_contribution'] = df_merged['sequences']/sequence_2020_10

sequence_2020_02 = estimate_2020_02/estimate_all * 25000
sequence_2020_03 = estimate_2020_03/estimate_all * 25000
sequence_2020_04 = estimate_2020_04/estimate_all * 25000
sequence_2020_05 = estimate_2020_05/estimate_all * 25000
sequence_2020_06 = estimate_2020_06/estimate_all * 25000
sequence_2020_07 = estimate_2020_07/estimate_all * 25000
sequence_2020_08 = estimate_2020_08/estimate_all * 25000
sequence_2020_09 = estimate_2020_09/estimate_all * 25000
sequence_2020_10 = estimate_2020_10/estimate_all * 25000

df_merged.loc[df_merged['date'] == '2020-02','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_02
df_merged.loc[df_merged['date'] == '2020-03','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_03
df_merged.loc[df_merged['date'] == '2020-04','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_04
df_merged.loc[df_merged['date'] == '2020-05','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_05
df_merged.loc[df_merged['date'] == '2020-06','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_06
df_merged.loc[df_merged['date'] == '2020-07','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_07
df_merged.loc[df_merged['date'] == '2020-08','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_08
df_merged.loc[df_merged['date'] == '2020-09','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_09
df_merged.loc[df_merged['date'] == '2020-10','estimate_contribution'] = df_merged['IHME_estimate_mean']/estimate_2020_10


df_merged.loc[df_merged['date'] == '2020-02', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_02
df_merged.loc[df_merged['date'] == '2020-03', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_03
df_merged.loc[df_merged['date'] == '2020-04', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_04
df_merged.loc[df_merged['date'] == '2020-05', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_05
df_merged.loc[df_merged['date'] == '2020-06', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_06
df_merged.loc[df_merged['date'] == '2020-07', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_07
df_merged.loc[df_merged['date'] == '2020-08', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_08
df_merged.loc[df_merged['date'] == '2020-09', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_09
df_merged.loc[df_merged['date'] == '2020-10', 'ideal_sequences'] = df_merged['estimate_contribution'] * sequence_2020_10


case_2020_02 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-02'), 'cases'].values[0]
case_2020_03 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-03'), 'cases'].values[0]
case_2020_04 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-04'), 'cases'].values[0]
case_2020_05 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-05'), 'cases'].values[0]
case_2020_06 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-06'), 'cases'].values[0]
case_2020_07 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-07'), 'cases'].values[0]
case_2020_08 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-08'), 'cases'].values[0]
case_2020_09 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-09'), 'cases'].values[0]
case_2020_10 = df_merged.loc[(df_merged['location'] == 'World') & (df_merged['date'] == '2020-10'), 'cases'].values[0]

df_merged.loc[df_merged['date'] == '2020-02','case_contribution'] = df_merged['cases']/case_2020_02
df_merged.loc[df_merged['date'] == '2020-03','case_contribution'] = df_merged['cases']/case_2020_03
df_merged.loc[df_merged['date'] == '2020-04','case_contribution'] = df_merged['cases']/case_2020_04
df_merged.loc[df_merged['date'] == '2020-05','case_contribution'] = df_merged['cases']/case_2020_05
df_merged.loc[df_merged['date'] == '2020-06','case_contribution'] = df_merged['cases']/case_2020_06
df_merged.loc[df_merged['date'] == '2020-07','case_contribution'] = df_merged['cases']/case_2020_07
df_merged.loc[df_merged['date'] == '2020-08','case_contribution'] = df_merged['cases']/case_2020_08
df_merged.loc[df_merged['date'] == '2020-09','case_contribution'] = df_merged['cases']/case_2020_09
df_merged.loc[df_merged['date'] == '2020-10','case_contribution'] = df_merged['cases']/case_2020_10



df_merged.loc[df_merged['date'] == '2020-02', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_02
df_merged.loc[df_merged['date'] == '2020-03', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_03
df_merged.loc[df_merged['date'] == '2020-04', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_04
df_merged.loc[df_merged['date'] == '2020-05', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_05
df_merged.loc[df_merged['date'] == '2020-06', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_06
df_merged.loc[df_merged['date'] == '2020-07', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_07
df_merged.loc[df_merged['date'] == '2020-08', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_08
df_merged.loc[df_merged['date'] == '2020-09', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_09
df_merged.loc[df_merged['date'] == '2020-10', 'apparent_sequences'] = df_merged['case_contribution'] * sequence_2020_10


df_estimate_outlier = df_merged.loc[df_merged['sequences'] < df_merged['ideal_sequences']]

df_case_outlier = df_merged.loc[df_merged['sequences'] < df_merged['apparent_sequences']]

df_final = df_merged[['location', 'date', 'ideal_sequences']]
df_final_new = df_final
df_final_new['location'] = df_final_new['location'].replace(['United States'], 'USA')

df_final['ideal_sequences'] = df_final['ideal_sequences'].apply(np.ceil)

df_final_no_world = df_final[df_final['location'] != 'World']



df_merged.to_csv('country_all_data.csv', index=False, na_rep='NaN')

df_estimate_outlier.to_csv('country_estimate_outlier_data.csv', index=False, na_rep='NaN')

#df_case_outlier.to_csv('country_case_outlier_data.csv', index=False, na_rep='NaN')

# Uncomment line below to create file that can be fed directly into Nybbler
#df_final.to_csv('country_ideal_sequences.csv', index=False, na_rep='NaN')
df_final_new.to_csv('country_ideal_sequences.csv', index=False, na_rep='NaN')

#df_final_no_world.to_csv('country_ideal_sequences_no_world.csv', index=False, na_rep='NaN')
