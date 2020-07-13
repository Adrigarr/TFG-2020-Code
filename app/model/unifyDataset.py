import pandas as pd
import os

d1 = pd.read_csv('check1.csv')
d2 = pd.read_csv('check1.csv')
d3 = pd.read_csv('check1.csv')
d4 = pd.read_csv('check1.csv')

data = [d1,d2,d3,d4]
data = pd.concat(data,sort=False)

df = data.drop(data[data.Song == '0'].index)

df.to_csv(os.getcwd() + '/app/static/cleanDataset.csv',index=False)