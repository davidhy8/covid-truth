import pandas


df_icl = pandas.read_csv('daily-new-estimated-covid-19-infections-icl-model.csv', dtype={'Entity': str}, usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (ICL, mean)'}, parse_dates=['Date'])
df_ihme = pandas.read_csv('daily-new-estimated-covid-19-infections-ihme-model.csv', dtype={'Entity': str}, usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (IHME, mean)'}, parse_dates=['Date'])
df_lshtm = pandas.read_csv('daily-new-estimated-covid-19-infections-lshtm-model.csv', dtype={'Entity': str}, usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (LSHTM, median)'}, parse_dates=['Date'])
df_yyg = pandas.read_csv('daily-new-estimated-covid-19-infections-yyg-model.csv', dtype={'Entity': str}, usecols={'Entity', 'Date', 'Daily new estimated infections of COVID-19 (YYG, mean)'}, parse_dates=['Date'])


df_icl.columns = ['location', 'date', 'ICL_estimate_mean']
df_ihme.columns = ['location', 'date', 'IHME_estimate_mean']
df_lshtm.columns = ['location', 'date', 'LSHTM_estimate_median']
df_yyg.columns = ['location', 'date', 'YYG_estimate_mean']


df_icl['date'] = df_icl['date'].dt.to_period('M')
df_ihme['date'] = df_ihme['date'].dt.to_period('M')
df_lshtm['date'] = df_lshtm['date'].dt.to_period('M')
df_yyg['date'] = df_yyg['date'].dt.to_period('M')


df_icl = df_icl.groupby(['location','date'], as_index = False).sum()
df_ihme = df_ihme.groupby(['location','date']).sum().reset_index()
df_lshtm = df_lshtm.groupby(['location', 'date'], as_index = False).sum()
df_yyg = df_yyg.groupby(['location','date'], as_index = False).sum()


df_icl_ihme = pandas.merge(df_icl, df_ihme, how='outer', left_on=['location', 'date'], right_on=['location','date'])
df_icl_ihme_lshtm = pandas.merge(df_icl_ihme, df_lshtm, how='outer',left_on=['location', 'date'], right_on=['location','date'])
df_all = pandas.merge(df_icl_ihme_lshtm, df_yyg, how='outer', left_on=['location', 'date'], right_on=['location','date'])



df_icl = df_icl.groupby(['location','date'], as_index = False).sum()
df_ihme = df_ihme.groupby(['location','date']).sum().reset_index()
df_lshtm = df_lshtm.groupby(['location', 'date'], as_index = False).sum()
df_yyg = df_yyg.groupby(['location','date'], as_index = False).sum()


df_icl_ihme = pandas.merge(df_icl, df_ihme, how='outer', left_on=['location', 'date'], right_on=['location','date'])
df_icl_ihme_lshtm = pandas.merge(df_icl_ihme, df_lshtm, how='outer',left_on=['location', 'date'], right_on=['location','date'])
df_all = pandas.merge(df_icl_ihme_lshtm, df_yyg, how='outer', left_on=['location', 'date'], right_on=['location','date'])


df_all.to_csv(r'C:\country_estimates.csv', index=False, na_rep = 'NaN')
