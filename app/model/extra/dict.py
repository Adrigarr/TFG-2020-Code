import csv
import os
#SONG
dictSongCodes =['wdt:P136','wdt:P175','wdt:P264','wdt:P361','wdt:P495','wdt:P407','wdt:P106','wdt:P577','wdt:P86',
        'wdt:P571','wdt:P737','wdt:P279','wdt:P166','wdt:P2031','wdt:P358','wdt:P740','wdt:P1411','wdt:P527','wdt:P463',
        'wdt:P412','wdt:P19','wdt:P2341']
        
dictSong = {
        'P136':'genre', 
        'P175':'performer', 
        'P264':'record label', 
        'P361':'part of',
        'P495':'country',
        'P407':'language',
        'P106':'occupation',
        'P577':'publication_date',
        'P86':'compositor',
        'P571':'inception',
        'P737':'influenced by',
        'P279':'subclass',
        'P166':'award received',
        'P2031':'work period start',
        'P358':'discography',
        'P740':'location of formation',
        'P1411':'nominated for',
        'P527':'participnats',
        'P463':'member of',
        'P412':'Voice Type',
        'P19':'place of birth',
        'P2341':'indigenous to'
        }


        #MEMBERS
dictMembers = {
        'P463':'member of',
        'P412':'Voice Type',
        'P19':'place of birth',
        'P2341':'indigenous to',
        'P166':'award received',
        'P2031':'work period start',
        'P358':'discography',
        'P740':'location of formation',
        'P1411':'nominated for',
        'P737':'influenced by',
        'P264':'record label', 
        'P361':'part of',
        'P495':'country',
        'P407':'language',
        'P106':'occupation',    
        }
dictMembersCodes = ['wdt:P463','wdt:P412','wdt:P19','wdt:P2341','wdt:P166','wdt:P2031','wdt:P358','wdt:P740',
        'wdt:P1411','wdt:P737','wdt:P264', 'wdt:P361','wdt:P495','wdt:P407','wdt:P106',]

dictGenre = {
        'P361':'part of',
        'P495':'country',
        'P571':'inception',
        'P737':'influenced by',
        'P279':'subclass',
        'P740':'location of formation',
        'P2341':'indigenous to'
        }
dictGenreCodes = ['wdt:P361','wdt:P495','wdt:P571','wdt:P737','wdt:P279','wdt:P740','wdt:P2341']

        
        #ARTIST
dictArtist = {
        'P136':'genre', 
        'P264':'record label',
        'P361':'part of',
        'P495':'country',
        'P407':'language',
        'P106':'occupation',
        'P571':'inception',
        'P737':'influenced by',
        'P166':'award received',
        'P2031':'work period start',
        'P358':'discography',
        'P740':'location of formation',
        'P1411':'nominated for',
        'P527':'participnats',
        'P412':'Voice Type',
        'P19':'place of birth',
        'P2341':'indigenous to'
        }
dictArtistCodes = ['wdt:P136','wdt:P264','wdt:P361','wdt:P495','wdt:P407','wdt:P106','wdt:P571','wdt:P737','wdt:P166','wdt:P2031',
        'wdt:P358','wdt:P740','wdt:P1411','wdt:P527','wdt:P412','wdt:P19','wdt:P2341']

if __name__ == "__main__":


    
    with open('SongD.csv', 'w') as f:
        for key in dictSong.keys():
            f.write("%s,%s\n"%(key,dictSong[key]))

    with open('ArtistD.csv', 'w') as f:
        for key in dictArtist.keys():
            f.write("%s,%s\n"%(key,dictArtist[key]))

    with open('GenreD.csv', 'w') as f:
        for key in dictGenre.keys():
            f.write("%s,%s\n"%(key,dictGenre[key]))

    with open('MembersD.csv', 'w') as f:
        for key in dictMembers.keys():
            f.write("%s,%s\n"%(key,dictMembers[key]))

    with open('SongListD.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dictSongCodes)
    with open('ArtistListD.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dictArtistCodes)
    with open('GenreListD.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dictGenreCodes)
    with open('MembersListD.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dictMembersCodes)


