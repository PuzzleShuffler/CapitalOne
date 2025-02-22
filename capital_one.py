# libraries
import glob
import pandas as pd
import numpy as np

# import data
files = glob.glob('datasets/*.TXT')

df = pd.DataFrame()

for file in files:
    new_df = pd.read_csv(
        file, 
        header=None,
        names=['state', 'sex', 'year', 'name', 'occurences'])
    df = pd.concat([df, new_df], axis='rows')

##### Question 1 #####
# Structuring the data in separate csv files per state seems annoying to keep up to date. It would be a lot easier just to have one large csv file with all states represented and keep updating it as new data becomes available.
# This way, there will be less chances for errors in data entry.

##### Question 2 #####
df.groupby('name')['occurences'].sum().nlargest(1)

##### Question 3 #####

def gender_ambigous_name(year, top_n):
    # female names
    f_names = df.loc[
    (df['sex'] == 'F') &
    (df['year'] == year),
    'name'
    ]
    # convert to set
    f_names = set(f_names)

    # male names
    m_names = df.loc[
        (df['sex'] == 'M') &
        (df['year'] == 2013),
        'name'
    ]
    # convert to set
    m_names = set(m_names)

    # intersection of sets as list
    a_names = list(f_names.intersection(m_names))

    # df of top 5 occurences
    new_df = df.loc[
        (df['name'].isin(a_names))
    ].groupby('name')['occurences'].sum().nlargest(top_n).reset_index()
    return new_df

gender_ambigous_name(year=2013, top_n=10)
gender_ambigous_name(year=1945, top_n=10)

##### Question 4 #####
# names in 1980
names_1980 = df.loc[
    (df['year'] == 1980),
    'name'
]

# names in 2021
names_2021 = df.loc[
    (df['year'] == 2021),
    'name'
]

# names in both years
valid_names = list(set(names_1980).intersection(set(names_2021)))

# pivot table of both years
q4_df = df.loc[
    (df['name'].isin(valid_names)) &
    (df['year'].isin([1980, 2021]))
       ].pivot_table(index='name', columns='year', aggfunc='sum').reset_index()

# calculate pct_change
q4_df['pct_change'] = np.round((q4_df[('occurences', 2021)] - q4_df[('occurences', 1980)]) / q4_df[('occurences', 1980)] * 100,2)

q4_df.nlargest(columns='pct_change', n=10)

##### Question 5 #####