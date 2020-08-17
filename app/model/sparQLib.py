from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON
from app.model.properties import *
from app.model.dataOperations import *
import pandas as pd
import math
import json


class sparQLSession:

    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        self.prop = Properties()
        self.song = 'SONG'
        self.artist = 'ARTIST'
        self.members = 'MEMBERS'
        self.genre = 'GENRE'
        

    def commonProperties(self,song1,song2):

        auxi = self.prop.getDictSong('code',False)
        auxi = parseQueryString(auxi)
        res = 'Song'

        formatString =f"""SELECT ?same ?item1 ?item1Label 
        WHERE
        {{
        wd:{song1} ?same ?item1. # Primera cancion - Propiedad buscada - Valor de la propiedad
        wd:{song2} ?same ?item2. # Segunda cancion - Propiedad buscada - Valor de la propiedad
        FILTER (?item1 = ?item2). # Nos quedamos solo con las propiedades cuyo valor coincide
        FILTER (?same in ({auxi})). # Nos quedamos con las propiedades relevantes para nosotros: género, intérprete, sello discográfico, compositor, letra de, part of (album),country,language,publication_date
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}"""

        #Que tienen en comun ambas canciones
        self.sparql.setQuery(formatString)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
      
        if len(results['results']['bindings']) != 0:
            results_df = pd.io.json.json_normalize(results['results']['bindings'])
            results_d = results_df[['same.value','item1.value','item1Label.value']]
            results_d['Level']=1
            results_d = tratamientoDataSet(results_d)
            results_d = self.executeDict(results_d,res)
        else:
            #Empty dataset
            results_d = pd.DataFrame(columns=['idProperty','idValueProperty','valueProperty','Level'])
        return results_d

    #Obtener genero de una canción para la clase study
    def getGenreSong(self,song,artist):

        self.sparql.setQuery("""
        SELECT distinct ?genreLabel
        WHERE{  
        ?item ?label "%s"@en. 
        ?item wdt:P175 ?artist.    
        ?artist ?label "%s"@en.
        ?item wdt:P136 ?genre
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """%(song,artist))
        self.sparql.setReturnFormat(JSON)
        results3 = self.sparql.query().convert()
        #print(results3)
        resultsG1 = pd.io.json.json_normalize(results3['results']['bindings'])
        resultsGenre = resultsG1[['genreLabel.value']]
        return resultsGenre

#---------------------------------------------------------------------------------------------------------------------------


    ####PARA RESUMIR:
    #Obtenemos propiedades de la cancion.
    def getInfo(self,mode,item,title):

        res=''

        if mode == 'Song':
            auxi = self.prop.getDictSong('code',True)
            auxi = parseQueryString(auxi)
            res = 'Song'
        elif mode == 'Artist':
            auxi = self.prop.getDictArtist('code',True)
            auxi = parseQueryString(auxi)
            res = 'Artist'

        elif mode == 'Members':
            auxi = self.prop.getDictMembers('code',True)
            auxi = parseQueryString(auxi)
            res = 'Members'

        elif mode == 'Genre':
            auxi = self.prop.getDictGenre('code',True)
            auxi = parseQueryString(auxi)
            res = 'Genre'

        self.sparql.setQuery("""
        SELECT ?same ?item1 ?item1Label 
        WHERE
        {
        wd:%s ?same ?item1.
        FILTER (?same in (%s)).
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """%(item,auxi))
        self.sparql.setReturnFormat(JSON)
        results3 = self.sparql.query().convert()
        resultsI1 = pd.io.json.json_normalize(results3['results']['bindings'])

        resultsItem1 = pd.DataFrame(pd.np.empty((0, 3)))

        if {'same.value','item1.value','item1Label.value'}.issubset(resultsI1.columns):
            resultsItem1 = resultsI1[['same.value','item1.value','item1Label.value']]
        
        if mode == 'Song':
           resultsItem1['Level'] = 1
           
        elif mode == 'Artist':
            resultsItem1['Level'] = 2

        elif mode == 'Members':
            resultsItem1['Level'] = 4

        elif mode == 'Genre':
            resultsItem1['Level'] = 3

        resultsItem1['ID'] = title
        resultsItem1 = tratamientoDataSet(resultsItem1)
        resultsItem1 = self.executeDict(resultsItem1,res)
       
        return resultsItem1


#---------------------------------------------------------------------------------------------------------------------------
    #CHECK IF SONG OR SINGLE EXISTS
    def isTypeSong(self,kind,code,artist):
        if kind == 'Single':
            aux = 'Q134556'
        else:
            aux = 'Q7366'
        self.sparql.setQuery("""SELECT distinct ?item ?itemLabel ?itemDescription 
        WHERE{  
        ?item ?label "%s"@en. 
        ?item wdt:P31 wd:%s.
        ?item wdt:P175 ?artist.    
        ?artist ?label "%s"@en. 
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """%(code,aux,artist))

        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        
        if len(results['results']['bindings']) != 0:
            results_df = pd.io.json.json_normalize(results['results']['bindings'])
            aux = results_df[['item.value','itemLabel.value','itemDescription.value']]
            aux['item.value'] = aux['item.value'].apply(lambda x: x.split('/')[4])
        else:
            #Empty dataset
                aux = pd.Series([])
        return aux


    #Obtenemos el nombre del artista de una cancion
    def checkNameArtist(self,song):
        self.sparql.setQuery("""
        SELECT ?artist ?artistLabel {
        wd:%s wdt:P175 ?artist
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        } 
        """%song)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        resultsA1 = pd.io.json.json_normalize(results['results']['bindings'])
        resultsA1 = resultsA1[['artist.value','artistValue.value']]
        return resultsA1

    def executeDict(self,df,mode):
        if mode == 'Song':
             dic = self.prop.getDictSong('info',False)
        elif mode == 'Artist':
            dic = self.prop.getDictArtist('info',False)
        elif mode == 'Members':
            dic = self.prop.getDictMembers('info',False)
        elif mode == 'Genre':
            dic = self.prop.getDictGenre('info',False)

        df["idPropertyName"]=df["idProperty"].replace(dic, inplace=False)
        return df
