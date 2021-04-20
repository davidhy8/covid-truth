"# covid-data-processor" 

# covid-data-processor
### These scripts were designed to obtain covid-19 related data from various countries across the world and group the data by month

# ourworldindata_covid.py
### This file reads data from Our World in Data and groups the data into country and month. Also calculates the percent positive ratio and CFR

# epidemiological_models.py
### This file reads data from the four epidemiological models (YYG, IHME, ICL, LSHTM) and produces country_estimate which groups the estimates into month and country

# SeroTracker_covid.py 
### This file processes data from SeroTracker and groups the seroprevalence findings for various countries by month

#sero_grouper.R
### This file averages the serofindings for each country by month

# data_merger.py
### This file merges all the data into one csv and calculates the weighted sampling strategy. Ideal sequences is the number of sequences to be obtained from each country based on the IHME estimate and apparent sequences is hte number of sequences to be obtained from each country based on the number of reported cases

# Order to run pipeline:
### Run ourworldindata_covid.py then epidemiological_models.py then SeroTracker_covid.py then sero_grouper.R then finally data_merger.py 
