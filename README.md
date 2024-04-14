# covid-truth
These scripts were designed to obtain COVID-19 related data from various countries across the world and group the data by month. Epidemiological model and serology studies were used to estimate the "true" prevelance of COVID-19 around world. Meanwhile, sequence sampling suggestions for GISAID are also made in the pipeline. The output file "country_ideal_sequences.csv" can be directly used in the Nybbler repository (https://github.com/nodrogluap/nybbler) to perform weighted sampling. See the paper attached in the description of the repository for more information.

The GISAID metadata cannot be shared. Please visit https://gisaid.org/ to obtain data. The epidemiological models were obtained from:
- ICL model: https://ourworldindata.org/grapher/daily-new-estimated-covid-19-infections-icl-model
- IHME model: https://ourworldindata.org/grapher/daily-new-estimated-covid-19-infections-ihme-model
- LSHTM model: https://ourworldindata.org/grapher/daily-new-estimated-covid-19-infections-lshtm-model
- YYG model: https://ourworldindata.org/grapher/daily-new-estimated-covid-19-infections-yyg-model

Check out my dashboard for the intuition behind this project: https://public.tableau.com/views/COVID-19_17130738417970/Dashboard1?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link
