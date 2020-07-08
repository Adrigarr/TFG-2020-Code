from sanic import response
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
import logging
from datetime import datetime, timedelta


# local imports
from app import app
from app.helpers.draw import *
from app.helpers.graphmaking import *

from app.model.getInfoSongs import *
from app.model.sparqlLibrary import *

# define the environment for the Jinja2 templates
env = Environment(
    loader=PackageLoader('main', 'app/view'),
    autoescape=select_autoescape(['html', 'xml', 'tpl'])
)

# a function for loading an HTML template from the Jinja environment
def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return response.html(template.render(kwargs))



LOG_FILE = datetime.now().strftime("%Y%m%d") + "logfile.log"

def setLogging():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(LOG_FILE)

    logger.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger


def main(arg1,arg2,arg3,arg4):

    #STUDY 1
    song1 = arg1
    artist1 = arg2

    #STUDY 2
    song2 = arg3
    artist2 = arg4

    logger = setLogging()

    #PARSE SONGS
    try:
        #Object 1
        song1 = isSingle(song1,artist1)
        if song1.empty == True:
            song1 = arg1
            song1 = isSong(song1,artist1)

        #Object 2
        song2 = isSingle(song2,artist2)
        if song2.empty == True:
            song2 = arg3
            song2 = isSong(song2,artist2)

    except Exception as miss:
        logger.info(miss)

    #GET PROPERTIES        
    try:
        if song1.empty == True:
            raise Exception('Missing first song')
        else:
            if song2.empty == True:
                raise Exception('Missing second song')
            else:
                #SONG1
                songData = getInfSong(song1['item.value'][0],song1['itemLabel.value'][0])
                genreData = getGenre2(songData,logger)
                artistData = getArtist2(songData,logger)
                membersData = getMembers2(artistData,logger)

                #SONG2
                songData2 = getInfSong(song2['item.value'][0],song2['itemLabel.value'][0])
                genreData2 = getGenre2(songData2,logger)
                artistData2 = getArtist2(songData2,logger)
                membersData2 = getMembers2(artistData2,logger)

                #GENERE SONGINFO
                songData.to_csv('songData1.csv',index=False)
                songData2.to_csv('songData2.csv',index=False)

                #GENERE ARTIST
                artistData.to_csv('artistData.csv',index=False)
                artistData2.to_csv('artistData2.csv',index=False)

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
        logger.info(miss)
    return relationsDF



# Esta es la página principal de la aplicación
async def home(request):
    # os.getcwd() devuelve la URL actual
    # template = open(os.getcwd() + "/view/index.html")
    # return html(template.read())

    # Si el html necesita valores, habría que añadirlos dentro de este template
    # separados por comas. Ej: template('index2.html', var1=var1, var2=var2)
    return template(
        'template.html'
    )

# TEMPORAL
async def table(request):

    song1 = "(I Can't Get No) Satisfaction" # "Start Me Up"
    artist1 = "The Rolling Stones"
    song2 = "Hey Jude" # "Let It Be"
    artist2 = "The Beatles"

    #song1 = "Teardrop"
    #artist1 = "Massive Attack"
    #song2 = "Teardrop"
    #artist2 = "Massive Attack"

    relationsDF = main(song1, artist1, song2, artist2) # relationsDF es un DataFrame

    nolevel = relationsDF.loc[(relationsDF['Level_x'] != relationsDF['Level_y'])]
    nolevel.sort_values(by=['Level_x', 'Level_y', 'idPropertyName', 'valueProperty'], inplace= True)

    level = relationsDF.loc[relationsDF['Level_x'] == relationsDF['Level_y']]
    level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)

    return response.html(nolevel.to_html())

# TEMPORAL
async def graph4(request):

    return template(
        'graph4.html'
    )

# TEMPORAL
async def random(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    return response.text(thislist)

#WIP
async def index(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1 = cleanSong(thislist[0][1])[0]
    artist1 = cleanSong(thislist[0][1])[1]
    song2 = cleanSong(thislist[1][1])[0]
    artist2 = cleanSong(thislist[1][1])[1]

    relationsDF = main(song1, artist1, song2, artist2) # relationsDF es un DataFrame

    generateGraph(song1, song2, artist1, artist2, relationsDF)

    return template(
        'graph.html'
    )




# Static Files
app.static('app/static', './app/static')


# Rutas
app.add_route(home, '/')
app.add_route(index, '/index')
app.add_route(table, '/table') #Temporal
app.add_route(graph4, '/graph4') #Temporal
app.add_route(random, '/random') #Temporal

#@app.route("/")
#@app.route("/table")
#@app.route("/graph4")
#@app.route("/random")
#@app.route("/index")