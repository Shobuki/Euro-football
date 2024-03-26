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



fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(15, 15), sharey=True, sharex=True)
sns.countplot(x='FTR', data=data[data['Div'] == 'E0'], palette='viridis',order=['H', 'D', 'A'],ax=axes[0, 0]).set_xlabel('')
axes[0, 0].set_title('Englang - Premier League')
sns.countplot(x='FTR', data=data[data['Div'] == 'E1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[0, 1]).set_xlabel('')
axes[0, 1].set_title('Englang - Championship')
sns.countplot(x='FTR', data=data[data['Div'] == 'SP1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[0, 2]).set_xlabel('')
axes[0, 2].set_title('Spain - Primera Division')
sns.countplot(x='FTR', data=data[data['Div'] == 'SP2'], palette='viridis',order=['H', 'D', 'A'],ax=axes[0, 3]).set_xlabel('')
axes[0, 3].set_title('Spain - Segunda Division')
sns.countplot(x='FTR', data=data[data['Div'] == 'I1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[1, 0]).set_xlabel('')
axes[1, 0].set_title('Italy - Serie A')
sns.countplot(x='FTR', data=data[data['Div'] == 'I2'], palette='viridis',order=['H', 'D', 'A'],ax=axes[1, 1]).set_xlabel('')
axes[1, 1].set_title('Italy - Serie B')
sns.countplot(x='FTR', data=data[data['Div'] == 'D1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[1, 2]).set_xlabel('')
axes[1, 2].set_title('Germany - Bundesliga 1')
sns.countplot(x='FTR', data=data[data['Div'] == 'D2'], palette='viridis',order=['H', 'D', 'A'],ax=axes[1, 3]).set_xlabel('')
axes[1, 3].set_title('Germany - Bundesliga 2')
sns.countplot(x='FTR', data=data[data['Div'] == 'F1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[2, 0]).set_xlabel('')
axes[2, 0].set_title('France - Le Championnat')
sns.countplot(x='FTR', data=data[data['Div'] == 'F2'], palette='viridis',order=['H', 'D', 'A'],ax=axes[2, 1]).set_xlabel('')
axes[2, 1].set_title('France - Division 2')
sns.countplot(x='FTR', data=data[data['Div'] == 'SC0'], palette='viridis',order=['H', 'D', 'A'],ax=axes[2, 2]).set_xlabel('')
axes[2, 2].set_title('Scotland - Premier League')
sns.countplot(x='FTR', data=data[data['Div'] == 'SC1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[2, 3]).set_xlabel('')
axes[2, 3].set_title('Scotland - Division 1')
sns.countplot(x='FTR', data=data[data['Div'] == 'N1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[3, 0]).set_xlabel('')
axes[3, 0].set_title('Netherlands - Eredivisie')
sns.countplot(x='FTR', data=data[data['Div'] == 'P1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[3, 1]).set_xlabel('')
axes[3, 1].set_title('Portugal - Liga I')
sns.countplot(x='FTR', data=data[data['Div'] == 'T1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[3, 2]).set_xlabel('')
axes[3, 2].set_title('Turkey - Futbol Ligi 1')
sns.countplot(x='FTR', data=data[data['Div'] == 'G1'], palette='viridis',order=['H', 'D', 'A'],ax=axes[3, 3]).set_xlabel('')
axes[3, 3].set_title('Greece - Ethniki Katigoria')

plt.show()