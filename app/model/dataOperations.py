from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON
import pandas as pd
import math
import json

#Obtenmos el valor real de las propiedades sin caracteres sobrantes
def tratamientoDataSet(df):
    df['same.value']=df['same.value'].apply(lambda x: x.split('/')[5])
    idx = df.index[df['same.value']=='P571']
    aux = df.iloc[idx]['item1.value']
    aux2 = "////"+aux
    df.at[idx, 'item1.value'] = aux2

    idx = df.index[df['same.value']=='P2031']
    aux=df.iloc[idx]['item1.value']
    aux2="////"+aux
    df.at[idx, 'item1.value'] = aux2

    idx = df.index[df['same.value']=='P577']
    aux=df.iloc[idx]['item1.value']
    aux2="////"+aux
    df.at[idx, 'item1.value'] = aux2

    df['item1.value']=df['item1.value'].apply(lambda x: x.split('/')[4])
    df.columns = ['idProperty', 'idValueProperty','valueProperty','Level','ID']
    return df
 
def formatDates(df):
     df['valueProperty'] = df.apply(lambda x: x.valueProperty[2:] if x.idProperty == 'P571' else x.valueProperty, axis=1)
     df['valueProperty'] = df.apply(lambda x: x.valueProperty[2:] if x.idProperty == 'P577' else x.valueProperty, axis=1)   
     return df
#
def getGenrefrom(df):
    if(df['idProperty'] == 'P136').any()==True:
        aux = df.loc[df['idProperty'] =='P136',['idValueProperty','valueProperty']]
    else:
        aux = pd.Series([])
    return aux

#
def getMembersfrom(df):
    if(df['idProperty'] == 'P527').any()==True:
        aux = df.loc[df['idProperty'] =='P527',['idValueProperty','valueProperty']]
    else:
        aux = pd.Series([])
    return aux
#
def getArtistfrom(df):
    if(df['idProperty'] == 'P175').any()==True:
        aux = df.loc[df['idProperty'] =='P175',['idValueProperty','valueProperty']]
    else:
        aux = pd.Series([])
    return aux

def parseDates(dfSong):
    dfSong['valueProperty'] = dfSong.apply(lambda x: x.valueProperty.split('-')[0] if x.idProperty == 'P571' else x.valueProperty, axis=1)
    dfSong['valueProperty'] = dfSong.apply(lambda x: x.valueProperty.split('-')[0] if x.idProperty == 'P2031' else x.valueProperty, axis=1)
    dfSong['valueProperty'] = dfSong.apply(lambda x: x.valueProperty.split('-')[0] if x.idProperty == 'P577' else x.valueProperty, axis=1)
    return dfSong


def groupCSV(df):
    path='genreSongs.csv'
    data = pd.read_csv(path,sep=',', error_bad_lines=False)
    dataGrouped = data.groupby(['genreLabel.value']).size().reset_index(name='counts')
    dataGrouped.to_csv('genreGrouped.csv',index=False)

def parseQueryString(propString):
    propString = propString.replace('[', '')
    propString = propString.replace(']', '')
    propString = propString.replace(' ', '')
    propString = propString.replace("'", '')
    return propString

#MERGE DATAFRAMES
def mergeData(df1,df2):
    df3 = pd.merge(df1, df2, on=['idProperty', 'idPropertyName', 'idValueProperty', 'valueProperty'], how='inner')
    return df3

