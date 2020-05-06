from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON
from sparqlLibrary import *
import pandas as pd
import json
import sys
 
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
 

def getGenre(dfSong,genre):
    for i in genre:   
        resultsGenre1 = getInfoGenre(i)
        resultsGenre1['Level'] = 2
        resultsGenre1 = executeDict(resultsGenre1)
        dfSong = pd.concat([dfSong, resultsGenre1], ignore_index=True)
    return dfSong

def getArtist(dfSong,artist):
    for i in artist:  
        resultsArtist1 = getInfoArtist(i)
        resultsArtist1['Level'] = 3
        resultsArtist1 = executeDict(resultsArtist1)
        dfSong = pd.concat([dfSong, resultsArtist1], ignore_index=True)
    return dfSong

def getMembers(dfSong,members):
    for i in members:
        resultsMembers1 = getInfoMembers(i)
        resultsMembers1['Level'] = 4
        resultsMembers1 = executeDict(resultsMembers1)
        dfSong = pd.concat([dfSong, resultsMembers1], ignore_index=True)
    return dfSong

def mergeData(df1,df2):
    df3 = pd.merge(df1, df2, on=['idProperty', 'idPropertyName', 'idValueProperty', 'valueProperty'], how='inner')
    return df3

#_________________________________________________________________________________________________________________________________


def main(song1,song2,logger):
    logger = logger
    
    try:
        ##PROPIEDADES EN COMUN
        df = commonProperties(song1,song2)
 
    except Exception as error:
        logger.info(error)
    
    ##PROPIEDADES CANCION 1
    dfSong = getInfoSong(song1)
    dfSong = executeDict(dfSong)
    ##AÑADIMOS GENERO 1
    genre = getGenrefrom(dfSong)
    if genre.empty == False:
       logger.info("Se ha encontrado genero")
       dfSong = getGenre(dfSong,genre)
    else:
        logger.info("No se ha encontrado genero de la cancion 1")

    ##AÑADIMOS ARTISTA 1
    artist = getArtistfrom(dfSong)
    if artist.empty == False:
        logger.info("Se ha encontrado artista")
        dfSong = getArtist(dfSong,artist)
    else:
        logger.info("No se ha encontrado artista de la cancion 1")
    
    ##AÑADIMOS MIEMBROS 1
    members = getMembersfrom(dfSong)
    if members.empty == False:
       logger.info("Se han encontrado miembros")
       dfSong = getMembers(dfSong,members)
    else:
        logger.info("No se han encontrado miembros 1")


    #PARSE DATES
    dfSong = parseDates(dfSong)
    

    #________________________________________________________________________________________________________________________________________________
    
    
    
    ##PROPIEDADES CANCION 2
    dfSong2 = getInfoSong(song2)
    dfSong2 = executeDict(dfSong2)
    ##AÑADIMOS GENERO 2
    genre2 = getGenrefrom(dfSong2)
    if genre2.empty == False:
       logger.info("Se ha encontrado genero 2")
       dfSong2 = getGenre(dfSong2,genre2)
    else:
        logger.info("No se ha encontrado genero de la cancion 2")

    ##AÑADIMOS ARTISTA 2
    artist2 = getArtistfrom(dfSong2)
    if artist2.empty == False:
        logger.info("Se ha encontrado artista 2")
        dfSong2 = getArtist(dfSong2,artist2)
    else:
        logger.info("No se ha encontrado artista de la cancion 2")
    
    ##AÑADIMOS MIEMBROS 2
    members2 = getMembersfrom(dfSong2)
    if members2.empty == False:
       logger.info("Se han encontrado miembros 2")
       dfSong2 = getMembers(dfSong2,members2)
    else:
        logger.info("No se han encontrado miembros 2")


    #PARSE DATES
    dfSong2 = parseDates(dfSong2)
    
    finalDataSet = mergeData(dfSong,dfSong2)
    finalDataSet = finalDataSet.drop_duplicates()

    return finalDataSet

#if __name__ == '__main__':
#    main(sys.argv[1], sys.argv[2], sys.argv[3])