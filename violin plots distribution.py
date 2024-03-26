import pandas as pd
import xlrd
import numpy as np
from math import factorial
from scipy.stats import randint
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
#import graphviz
from graphviz import Digraph
from pandas import ExcelFile
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)
print('Tools and libraries imported.\n')
data = pd.read_excel(r'C:\Users\Alfredo\Documents\euro\Euro-Football_2012-2023.xlsx')

#----------------------------------------
#DATA CLEANING
#----------------------------------------

# Menghapus baris dengan nilai Null'
data.dropna(subset=['FTHG', 'HTHG','HS','HF','HY','HR',], inplace=True)

#drop 'Referee'
data.drop(['Referee'], axis=1, inplace=True)

#print('Referee column dropped')
data.columns
cols = ['id', 'Country', 'League', 'Div', 'Season', 'HomeTeam', 'AwayTeam', 'HTR', 'FTR']

#convert cols to category type
data[cols] = data[cols].astype('category')
#print(f'{cols} converted to category type')
#plot missing values
print(f"{round((data.isnull().sum().sum()/data.size)*100)}% of the data are missing but all ids are unique: {data.id.nunique() == data.shape[0]}\n")


"""
CHECK DATA APAKAH SELESAI DATA CLEANING?
print(data['Country'].unique().tolist())
print("Total data yang masih ada setelah menghapus baris dengan nilai':", len(data))
"""
#---------------------------------------------------------------------------

#PENAMBAHAN KOLOM BARU
#--------------------------------------------------------------------------
# Renaming Columns
data.rename(columns={'HTHG': 'FHHG', 'HTAG': 'FHAG', 'HTR': 'FHR'}, inplace=True)

# total goals
data['SHHG'] = data['FTHG'] - data['FHHG']  # 2nd half home goals #
data['SHAG'] = data['FTAG'] - data['FHAG']  # 2nd half away goals #
data['FHTG'] = data['FHHG'] + data['FHAG']  # 1st half total goals #
data['SHTG'] = data['SHHG'] + data['SHAG']  # 2nd half total goals #
data['FTTG'] = data['FTHG'] + data['FTAG']  # full-time total goals

# goal difference
data['FTGD'] = abs(data['FTHG'] - data['FTAG'])  # full-time goal difference (absolute value) #
data['FHGD'] = abs(data['FHHG'] - data['FHAG'])  # 1st half goal difference
data['SHGD'] = abs(data['SHHG'] - data['SHAG'])  # 2nd half goal difference

# 2nd half result
data['SHR'] = 'D'  # Default to 'D'
data.loc[data['SHHG'] > data['SHAG'], 'SHR'] = 'H'
data.loc[data['SHHG'] < data['SHAG'], 'SHR'] = 'A'

print('Sample of data:')
data[['FHHG', 'FHAG' ,'SHHG', 'SHAG', 'SHR', 'FHTG', 'SHTG', 'FTTG', 'FTGD', 'FHGD', 'SHGD']].head()

#----------------------------------------------------------------------------------------------------------
# Creating Total Shots (TS)
data['TS'] = data['HS'] + data['AS']

# Creating Total Shots on Target (TST)
data['TST'] = data['HST'] + data['AST']

# Creating Total Corners (TC)
data['TC'] = data['HC'] + data['AC']

# Creating Total Fouls (TF)
data['TF'] = data['HF'] + data['AF']

# Creating Total Yellow Cards (TY)
data['TY'] = data['HY'] + data['AY']

# Creating Total Red Cards (TR)
data['TR'] = data['HR'] + data['AR']

#-----------------------------------------------

f1 = data['HomeTeam'] == 'Arsenal'
a1 = data[f1][['Date','Season', 'HomeTeam', 'HC', 'TC']]
a1['rolling corners'] = a1['HC'].rolling(10).mean()

f2 = data['AwayTeam'] == 'Arsenal'
a2 = data[f2][['Date','Season', 'AwayTeam', 'AC', 'TC']]
a2['rolling corners'] = a2['AC'].rolling(10).mean()

# #plot timeline of corners in facet grid
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

c1 = sns.lineplot(x='Date', y='TC', data=a1[a1['Season'] == '2021-2022'], ax=axes[0], label='corners in the match')
c1 = sns.lineplot(x='Date', y='HC', data=a1[a1['Season'] == '2021-2022'], ax=axes[0], label="Arsenal's corners")
# add reference lines
c1.axhline(y=a1['HC'].mean(), color='orange', linestyle='--', label='mean', linewidth=0.5)
c1.axhline(y=a1['TC'].mean(), color='blue', linestyle='--', label='mean', linewidth=0.3)
c1.set_title('Corners @home')

c2 = sns.lineplot(x='Date', y='TC', data=a2[a2['Season'] == '2021-2022'], ax=axes[1], label='corners in the match')
c2 = sns.lineplot(x='Date', y='AC', data=a2[a2['Season'] == '2021-2022'], ax=axes[1], label="Arsenal's corners")
c2.axhline(y=a2['AC'].mean(), color='orange', linestyle='--', label='mean', linewidth=0.5)
c2.axhline(y=a2['TC'].mean(), color='blue', linestyle='--', label='mean', linewidth=0.3)
c2.set_title('Corners @away')

del a1, a2, f1, f2, c1, c2

plt.show()