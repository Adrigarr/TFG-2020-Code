from app.model.dataOperations import *
import pandas as pd
import json
import sys
import os
 

class getInfoSongs:

    def __init__(self,logger,sp):
        self.sparq = sp
        self.logger = logger



    def parse2Song(self,name1,name2,artist1,artist2):

        name1 = name1.title()
        name2 = name2.title()
        artist1 = artist1.title()
        artists2 = artist2.title()
        return name1, name2, artist1, artist2

    def parse1Song(self,name,artist):
        name = name.title()
        artist = artist.title()
        return name,artist


    ##ADD TO DFRESULT GENRES PROPERTIES
    def getGenre2(self,df,logger):
        genre = getGenrefrom(df)
        aux = pd.DataFrame()
        if genre.empty == False:
            self.logger.info("Se ha encontrado genero")
        
            for i in genre.iterrows():   
                resultsGenre1 = self.sparq.getInfo('Genre',i[1]['idValueProperty'],i[1]['valueProperty'])
                resultsGenre1['Level'] = 3
                resultsGenre1 = self.sparq.executeDict(resultsGenre1,'Genre')
                aux = pd.concat([aux, resultsGenre1], ignore_index=True)
        else:
            logger.info("No se ha encontrado genero de la cancion 1")
        return aux

    def getArtist2(self,df,logger):
        artist = getArtistfrom(df)
        aux = pd.DataFrame()
        if artist.empty == False:
            logger.info("Se ha encontrado artista")
            for i in artist.iterrows():   
                resultsArtist1 = self.sparq.getInfo('Artist',i[1]['idValueProperty'],i[1]['valueProperty'])
                resultsArtist1['Level'] = 4
                resultsArtist1 = self.sparq.executeDict(resultsArtist1,'Artist')

                #GENERE ARTIST
                resultsArtist1.to_json(os.getcwd() + '/app/static/' + i[1]['valueProperty'] + '.json')

                aux = pd.concat([aux, resultsArtist1], ignore_index=True)
        else:
            logger.info("No se ha encontrado artistas del artista")
        return aux

    def getMembers2(self,df,logger):
        members = getMembersfrom(df)
        aux = pd.DataFrame()
        if members.empty == False:
            logger.info("Se han encontrado miembros")
            for i in members.iterrows():   
                resultsMembers1 = self.sparq.getInfo('Members',i[1]['idValueProperty'],i[1]['valueProperty'])
                resultsMembers1['Level'] = 5
                resultsMembers1 = self.sparq.executeDict(resultsMembers1,'Members')
                aux = pd.concat([aux, resultsMembers1], ignore_index=True)
        else:
            logger.info("No se ha encontrado Miembros del grupo ")
        return aux

    #MERGE DATAFRAMES
    def mergeData(self,df1,df2):
        df3 = pd.merge(df1, df2, on=['idProperty', 'idPropertyName', 'idValueProperty', 'valueProperty'], how='inner')
        return df3

    def getInfSong(self,songCode,title):
        dfSong = self.sparq.getInfo('Song',songCode,title)
        dfSong = self.sparq.executeDict(dfSong,'Song')
        return dfSong

    #PARSE DATES
    def parseDates(self,dfSong):
        res = parseDates(dfSong)
    
    def process(self,song1,artist1,song2,artist2):
        songP1 = song1
        artistP1 = artist1
        songP2 = song2
        artistP2 = artist2
        try:
            #Object 1
            songP1 = self.sparq.isTypeSong('Single',songP1,artistP1)
            if songP1.empty == True:
                songP1 = song1
                songP1 = self.sparq.isTypeSong('Song',songP1,artistP1)
    
            #Object 2
            songP2 = self.sparq.isTypeSong('Single',songP2,artistP2)
            if songP2.empty == True:
                songP2 = song2
                songP2 = self.sparq.isTypeSong('Song',songP2,artistP2)

        except Exception as miss:
            self.logger.info(miss)
       
        #GET PROPERTIES         
        try:
            if songP1.empty == True:
                raise Exception('Missing first song')
            else:
                if songP2.empty == True:
                    raise Exception('Missing second song')
                else:
                    #SONG1
                    songData = self.getInfSong(songP1['item.value'][0],songP1['itemLabel.value'][0])
                    genreData = self.getGenre2(songData,self.logger)
                    artistData = self.getArtist2(songData,self.logger)
                    membersData = self.getMembers2(artistData,self.logger)

                    #SONG2
                    songData2 = self.getInfSong(songP2['item.value'][0],songP2['itemLabel.value'][0])
                    genreData2 = self.getGenre2(songData2,self.logger)
                    artistData2 = self.getArtist2(songData2,self.logger)
                    membersData2 = self.getMembers2(artistData2,self.logger)


                    #GENERE SONGINFO
                    songData.to_json(os.getcwd() + '/app/static/' + songP1['itemLabel.value'][0] + '.json')
                    songData2.to_json(os.getcwd() + '/app/static/' + songP2['itemLabel.value'][0] +'.json')


                    song1Data = [songData,genreData,artistData,membersData]
                    song1Data = pd.concat(song1Data,sort=False)

                    song1Data = parseDates(song1Data)
                    song1Data = formatDates(song1Data)

                    song2Data = [songData2,genreData2,artistData2,membersData2]
                    song2Data = pd.concat(song2Data,sort=False)

                    song2Data = parseDates(song2Data)
                    song2Data = formatDates(song2Data)

                    relationsDF = mergeData(song1Data,song2Data)

                    relationsDF = relationsDF.drop_duplicates()
                    relationsDF.to_csv('relations.csv',index=False)
        except Exception as miss:
            self.logger.info(miss)
        return relationsDF

        