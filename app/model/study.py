import pandas as pd
import json
from sparqlLibrary import *

path='cleanDataset.csv'
data = pd.read_csv(path,sep=',', error_bad_lines=False)
aux = pd.DataFrame()
for row in data.iterrows():
    try:
        g = getGetGenreSong(row[1]['Song'],row[1]['Artist'])
        aux = pd.concat([aux, g], ignore_index=True)
    except:
        aux = aux.append(pd.DataFrame(['None'],columns = ['genreLabel.value']), ignore_index=True)

aux.to_csv('genreSongs.csv',index=False)