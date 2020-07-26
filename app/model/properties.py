import os
import csv

class Properties:


    def __init__(self):
           
           
            self.dictSong = ''
            self.dictSongCodes = ''
            self.dictArtist = ''
            self.dictArtistCodes = ''
            self.dictGenre = ''
            self.dictGenreCodes = ''
            self.dictMembers = ''
            self.dictMembersCodes  = ''


            filepath1 = os.getcwd() + '/app/static/csv/Song.csv'
            filepath2 = os.getcwd() + '/app/static/csv/SongCodes.csv'
            filepath3 = os.getcwd() + '/app/static/csv/Artist.csv'
            filepath4 = os.getcwd() + '/app/static/csv/ArtistCodes.csv'
            filepath5 = os.getcwd() + '/app/static/csv/Genre.csv'
            filepath6 = os.getcwd() + '/app/static/csv/GenreCodes.csv'
            filepath7 = os.getcwd() + '/app/static/csv/Members.csv'
            filepath8 = os.getcwd() + '/app/static/csv/MembersCodes.csv'


            with open(filepath1, mode='r') as infile:
                reader = csv.reader(infile)
                self.dictSong = {rows[0]:rows[1] for rows in reader}

            with open(filepath2, newline='') as f:
                reader = csv.reader(f)
                self.dictSongCodes = list(reader)

            with open(filepath3, mode='r') as infile:
                reader = csv.reader(infile)
                self.dictArtist = {rows[0]:rows[1] for rows in reader}

            with open(filepath4, newline='') as f:
                reader = csv.reader(f)
                self.dictArtistCodes = list(reader)

            with open(filepath5, mode='r') as infile:
                reader = csv.reader(infile)
                self.dictGenre = {rows[0]:rows[1] for rows in reader}

            with open(filepath6, newline='') as f:
                reader = csv.reader(f)
                self.dictGenreCodes = list(reader)

            with open(filepath7, mode='r') as infile:
                reader = csv.reader(infile)
                self.dictMembers = {rows[0]:rows[1] for rows in reader}

            with open(filepath8, newline='') as f:
                reader = csv.reader(f)
                self.dictMembersCodes = list(reader)


    def getDictSong(self,mode,text):
        if mode == 'code':
            return str(self.dictSongCodes)
        else:
            if text == False:
                return self.dictSong
            else:
                return str(self.dictSong)

    def getDictArtist(self,mode,text):
        if mode == 'code':
            return str(self.dictArtistCodes)
        else:
            if text == False:
                return self.dictArtist
            else:
                return str(self.dictArtist)

    def getDictGenre(self,mode,text):
        if mode == 'code':
            return str(self.dictGenreCodes)
        else:
            if text == False:
                return self.dictGenre
            else:
                return str(self.dictGenre)

    def getDictMembers(self,mode,text):
        if mode == 'code':
            return str(self.dictMembersCodes)
        else:
            if text == False:
                return self.dictMembers
            else:
                return str(self.dictMembers)



    def getdictValue(self,name,mode):
        res = ''
        if mode == 'SONG':
            res = self.dictSong[name]
        elif mode == 'ARTIST':
            res = self.dictArtist[name]
        elif mode == 'GENRE':
            res = self.dictGenre[name]
        elif mode == 'MEMBERS':
            res = self.dictMembers[name]
        return res


    #AD A NEW PROPERTY TO THE DICT 
    #codeProperty = codigo de la propiedad
    #meaningProperty = nombre de la propiedad
    def addProperty(self,mode,codeProperty,meaningProperty):
        res = True
        aux = 'wdt:'
        if mode == 'SONG':
            if 'codeProperty' in self.dictSong:
                res = False
            else:
                #Añadimos  propiedad en diccionario 
                self.dictSong['codeProperty'] = meaningProperty  
                with open('Song.csv', 'w') as f:
                    for key in self.dictSong.keys():
                        f.write("%s,%s\n"%(key,self.dictSong[key]))
                #Añadimos codigo en lista
                code = aux + codeProperty
                self.dictSongCodes.append(code)
                with open('SongCodes.csv', 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerow(self.dictSongCodes)
                         
        elif mode == 'ARTIST':
            if 'codeProperty' in self.dictArtist:
                res = False
            else:
                #Añadimos  propiedad en diccionario
                self.dictArtist['codeProperty'] = meaningProperty              
                with open('Artist.csv', 'w') as f:
                    for key in self.dictArtist.keys():
                        f.write("%s,%s\n"%(key,self.dictArtist[key]))
                #Añadimos codigo en lista
                code = aux + codeProperty
                self.dictArtistCodes.append(code)
                with open('ArtistCodes.csv', 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
                    wr.writerow(self.dictArtistCodes)
                
        elif mode == 'GENRE':
            if 'codeProperty' in self.dictGenre:
                res = False
            else:
                #Añadimos  propiedad en diccionario
                self.dictGenre['codeProperty'] = meaningProperty                
                with open('Genre.csv', 'w') as f:
                    for key in self.dictGenre.keys():
                        f.write("%s,%s\n"%(key,self.dictGenre[key]))
                #Añadimos codigo en lista
                code = aux + codeProperty
                self.dictGenreCodes.append(code)
                with open('GenreCodes.csv', 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
                    wr.writerow(self.dictGenreCodes)  

        elif mode == 'MEMBERS':
            if 'codeProperty' in self.dictMembers:
                res = False
            else:
                 
                 #Añadimos  propiedad en diccionario
                self.dictMembers['codeProperty'] = meaningProperty 
                with open('Members.csv', 'w') as f:
                    for key in self.dictMembers.keys():
                        f.write("%s,%s\n"%(key,self.dictMembers[key]))
                #Añadimos codigo en lista
                code = aux + codeProperty
                self.dictMembersCodes.append(code)
                with open('MembersCodes.csv', 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
                    wr.writerow(self.dictMembersCodes)  
        return res

