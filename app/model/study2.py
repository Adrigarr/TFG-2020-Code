import pandas as pd
import json
from sparqlLibrary import *

path='genreSongs.csv'
data = pd.read_csv(path,sep=',', error_bad_lines=False)
dataGrouped = data.groupby(['genreLabel.value']).size().reset_index(name='counts')
dataGrouped.to_csv('genreGrouped.csv',index=False)