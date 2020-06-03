from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON
import pandas as pd
import json
 


#Diccionarios para obtener el nombre de la propiedad
dic = {'P136':'género', 'P175':'intérprete', 'P264':'sello discográfico', 'P86':'compositor', 'P361':'forma parte de','P495':'country','P407':'language',
       'P577':'publication_date','P86':'compositor','P571':'inception','P737':'influenced by','P279':'subclass','P166':'award received','P2031':'work period start',
       'P358':'discography','P740':'location of formation','P1411':'nominated for','P527':'participants','P463':'member of','P172':'Voice Type','P19':'place of birth'}




#sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

def commonProperties(song1,song2):
     #Que tienen en comun ambas canciones
      sparql.setQuery("""SELECT ?same ?item1 ?item1Label 
      WHERE
      {
      wd:%s ?same ?item1. # Primera cancion - Propiedad buscada - Valor de la propiedad
      wd:%s ?same ?item2. # Segunda cancion - Propiedad buscada - Valor de la propiedad
      FILTER (?item1 = ?item2). # Nos quedamos solo con las propiedades cuyo valor coincide
      # Género, Intérprete (Artista), Sello discofráfico, Compositor, Parte de, Idioma, Fecha de publicación, Discografía
      FILTER (?same in (wdt:P136, wdt:P175, wdt:P264, wdt:P86, wdt:P361, wdt:P495, wdt:P407,wdt:P577,wdt:P358)). # Nos quedamos con las propiedades relevantes para nosotros: género, intérprete, sello discográfico, compositor, letra de, forma parte de (album),country,language,publication_date
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
      }
      """%(song1,song2))
      sparql.setReturnFormat(JSON)
      results = sparql.query().convert()
      
      if len(results['results']['bindings']) != 0:
          results_df = pd.io.json.json_normalize(results['results']['bindings'])
          results_d=results_df[['same.value','item1.value','item1Label.value']]
          results_d['Level']=1
          results_d=tratamientoDataSet(results_d)
          results_d = executeDict(results_d)
      else:
          #Empty dataset
          results_d = pd.DataFrame(columns=['idProperty','idValueProperty','valueProperty','Level'])
      return results_d

#FUNCIONES:

#Obtenemos el valor real de las propiedades sin caracteres sobrantes
def tratamientoDataSet(df):
    df['same.value']=df['same.value'].apply(lambda x: x.split('/')[5])
    idx = df.index[df['same.value']=='P571']
    aux=df.iloc[idx]['item1.value']
    aux2="////"+aux
    df.at[idx, 'item1.value'] = aux2

    idx = df.index[df['same.value']=='P577']
    aux=df.iloc[idx]['item1.value']
    aux2="////"+aux
    df.at[idx, 'item1.value'] = aux2

    df['item1.value']=df['item1.value'].apply(lambda x: x.split('/')[4])
    df.columns = ['idProperty', 'idValueProperty','valueProperty','Level', 'ID']
    return df


#Obtenemos propiedades de la cancion.
def getInfoSong(song, title):
    sparql.setQuery("""
    SELECT ?same ?item1 ?item1Label 
    WHERE
    {
    wd:%s ?same ?item1.
    # Género, Intérprete (Artista), Sello discográfico, País, Compositor, Parte de, Idioma, Fecha de publicación, Discografía
    FILTER (?same in (wdt:P136, wdt:P175, wdt:P264, wdt:P495,wdt:P86,wdt:P361, wdt:P407,wdt:P577,wdt:P358)).
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """%song)
    sparql.setReturnFormat(JSON)
    results3 = sparql.query().convert()
    #print(results3)
    resultsI1 = pd.io.json.json_normalize(results3['results']['bindings'])
    resultsItem1=resultsI1[['same.value','item1.value','item1Label.value']]
    resultsItem1['Level']=2
    resultsItem1['ID'] = title
    resultsItem1=tratamientoDataSet(resultsItem1)

    
    return resultsItem1

#Obtenemos propiedades del género.
def getInfoGenre(genre, title):
    sparql.setQuery("""
    SELECT ?same ?item1 ?item1Label 
    WHERE
    {
    wd:%s ?same ?item1.
    # Origen, País, Influenciado por, Subclase, Parte de
    FILTER (?same in (wdt:P571, wdt:P495, wdt:P737, wdt:P279, wdt:P361)).
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """%genre)

    sparql.setReturnFormat(JSON)
    results4 = sparql.query().convert()
    resultsG1 = pd.io.json.json_normalize(results4['results']['bindings'])
    resultsG1=resultsG1[['same.value','item1.value','item1Label.value']]
    resultsG1['Level'] = 2
    resultsG1['ID'] = title
    resultsGenre1 = tratamientoDataSet(resultsG1)
    resultsGenre1 = executeDict(resultsGenre1)


    return resultsGenre1

#Obtenemos propiedades del Artista.
def getInfoArtist(artist, name):
    sparql.setQuery("""
    SELECT ?same ?item1 ?item1Label 
    WHERE
    {
    wd:%s ?same ?item1.
    # Origen, Género, País, Influenciado por, Sello discográfico, Discografía, Lugar de formación, Premio recibido, Nominado a, Participantes, Miembro de, Tipo de voz
    FILTER (?same in (wdt:P571, wdt:P136, wdt:P495, wdt:P737, wdt:P264, wdt:P358, wdt:P740, wdt:P166, wdt:1411, wdt:P527, wdt:P463, wdt:P172)).
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """%artist)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    resultsA1 = pd.io.json.json_normalize(results['results']['bindings'])
    resultsA1=resultsA1[['same.value','item1.value','item1Label.value']]
    resultsA1['Level'] = 3
    resultsA1['ID'] = name
    resultArtist1 = tratamientoDataSet(resultsA1)
    resultArtist1 = executeDict(resultArtist1)

    
    return resultArtist1

#Obtenemos propiedades del Miembro
def getInfoMembers(member, name):
    sparql.setQuery("""
    SELECT ?same ?item1 ?item1Label 
    WHERE
    {
    wd:%s ?same ?item1.
    # Lugar de nacimiento, _, Miembro de, Género, _, Tipo de voz
    FILTER (?same in (wdt:P19, wdt:P66, wdt:P463, wdt:P136, wdt:P102, wdt:P172)).
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """%member)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    resultsM1 = pd.io.json.json_normalize(results['results']['bindings'])
    resultsM1 = resultsM1[['same.value','item1.value','item1Label.value']]
    resultsM1['Level'] = 4
    resultsM1['ID'] = name
    resultMember1 = tratamientoDataSet(resultsM1)
    resultMember1 = executeDict(resultMember1)

    
    return resultMember1

def getGenrefrom(df):
    if(df['idProperty'] == 'P136').any()==True:
        aux = df.loc[df['idProperty'] =='P136',['idValueProperty','valueProperty']]
    else:
        aux = pd.Series([])
    return aux

def getMembersfrom(df):
    if(df['idProperty'] == 'P527').any()==True:
        aux = df.loc[df['idProperty'] =='P527',['idValueProperty','valueProperty']]
    else:
        aux = pd.Series([])
    return aux

def getArtistfrom(df):
    if(df['idProperty'] == 'P175').any()==True:
        aux = df.loc[df['idProperty'] =='P175',['idValueProperty','valueProperty']]
    else:
        aux = pd.Series([])
    return aux

def addProperty(codeProperty,meaningProperty):
    res = True
    if 'codeProperty' in dic:
        res = False
    else:
        dic['codeProperty'] = meaningProperty     
    return res

def executeDict(df):
    df["idPropertyName"]=df["idProperty"].replace(dic, inplace=False)
    return df

def parseDates(dfSong):
    dfSong['valueProperty'] = dfSong.apply(lambda x: x.valueProperty.split('-')[0] if x.idProperty == 'P571' else x.valueProperty, axis=1)
    dfSong['valueProperty'] = dfSong.apply(lambda x: x.valueProperty.split('-')[0] if x.idProperty == 'P2031' else x.valueProperty, axis=1)
    dfSong['valueProperty'] = dfSong.apply(lambda x: x.valueProperty.split('-')[0] if x.idProperty == 'P577' else x.valueProperty, axis=1)
    return dfSong

#CHECK IF SONG OR SINGLE EXISTS
def isSingle(single,artist):
    sparql.setQuery("""SELECT distinct ?item ?itemLabel ?itemDescription 
    WHERE{  
    ?item ?label "%s"@en. 
    ?item wdt:P31 wd:Q134556.
    ?item wdt:P175 ?artist.    
    ?artist ?label "%s"@en. 
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """%(single,artist))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results['results']['bindings']) != 0:
        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        aux = results_df[['item.value','itemLabel.value','itemDescription.value']]
        aux['item.value'] = aux['item.value'].apply(lambda x: x.split('/')[4])
    else:
        #Empty dataset
            aux = pd.Series([])
    return aux

def isSong(song,artist):
    #Que tienen en comun ambas canciones
    sparql.setQuery("""SELECT distinct ?item ?itemLabel ?itemDescription 
    WHERE{  
    ?item ?label "%s"@en.  
    ?item wdt:P31 wd:Q7366.
    ?item wdt:P175 ?artist.    
    ?artist ?label "%s"@en.  
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """%(song,artist))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results['results']['bindings']) != 0:
        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        aux = results_df[['item.value','itemLabel.value','itemDescription.value']]
        aux['item.value'] = aux['item.value'].apply(lambda x: x.split('/')[4])
    else:
        #Empty dataset
            aux = pd.Series([]) 
    return aux

#Obtenemos el nombre del artista de una cancion
def checkNameArtist(song):
    sparql.setQuery("""
    SELECT ?artist ?artistLabel {
    wd:%s wdt:P175 ?artist
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } 
    """%song)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    resultsA1 = pd.io.json.json_normalize(results['results']['bindings'])
    resultsA1=resultsA1[['artist.value','artistValue.value']]
    return resultsA1