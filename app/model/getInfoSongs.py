from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON
from app.model.sparqlLibrary import *
import pandas as pd
import json
import sys
 
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
 
##ADD TO DFRESULT GENRES PROPERTIES
def getGenre2(df,logger):
    genre = getGenrefrom(df)
    aux = pd.DataFrame()

    if genre.empty == False:
       logger.info("Se ha encontrado genero")
       
       for i in genre.iterrows():   
           resultsGenre1 = getInfoGenre(i[1]['idValueProperty'],i[1]['valueProperty'])
           resultsGenre1['Level'] = 3
           resultsGenre1 = executeDict(resultsGenre1)
           aux = pd.concat([aux, resultsGenre1], ignore_index=True)
    else:
        logger.info("No se ha encontrado genero de la cancion 1")

    return aux


def getArtist2(df,logger):
    artist = getArtistfrom(df)
    aux = pd.DataFrame()

    if artist.empty == False:
        logger.info("Se ha encontrado artista")

        for i in artist.iterrows():   
            resultsArtist1 = getInfoArtist(i[1]['idValueProperty'],i[1]['valueProperty'])
            resultsArtist1['Level'] = 4
            resultsArtist1 = executeDict(resultsArtist1)
            aux = pd.concat([aux, resultsArtist1], ignore_index=True)

    else:
        logger.info("No se ha encontrado artistas del artista")

    return aux

def getMembers2(df,logger):
    members = getMembersfrom(df)
    aux = pd.DataFrame()

    if members.empty == False:
       logger.info("Se han encontrado miembros")
       for i in members.iterrows():   
            resultsMembers1 = getInfoMembers(i[1]['idValueProperty'],i[1]['valueProperty'])
            resultsMembers1['Level'] = 5
            resultsMembers1 = executeDict(resultsMembers1)
            aux = pd.concat([aux, resultsMembers1], ignore_index=True)
    else:
        logger.info("No se ha encontrado Miembros del grupo ")
    
    return aux


#MERGE DATAFRAMES
def mergeData(df1,df2):
    df3 = pd.merge(df1, df2, on=['idProperty', 'idPropertyName', 'idValueProperty', 'valueProperty'], how='inner')
    
    return df3


def getInfSong(songCode,title):
    dfSong = getInfoSong(songCode,title)

    dfSong = executeDict(dfSong)

    return dfSong


    #PARSE DATES
    dfSong = parseDates(dfSong)

#if __name__ == '__main__':
#    main(sys.argv[1], sys.argv[2], sys.argv[3])