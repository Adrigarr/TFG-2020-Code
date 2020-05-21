import logging
import sys
from datetime import datetime, timedelta
from getInfoSongs import *
from sparqlLibrary import *

from sanic import Sanic
from sanic import response
from jinja2 import Environment, PackageLoader, select_autoescape
import os
import json


# define the environment for the Jinja2 templates
env = Environment(
    loader=PackageLoader('main', 'templates'),
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

                song1Data = [songData,genreData,artistData,membersData]
                song1Data = pd.concat(song1Data,sort=False)

                song2Data = [songData2,genreData2,artistData2,membersData2]
                song2Data = pd.concat(song2Data,sort=False)

                relationsDF = mergeData(song1Data,song2Data)
                relationsDF = relationsDF.drop_duplicates()
                relationsDF.to_csv('relations.csv',index=False)

    except Exception as miss:
        logger.info(miss)
    return relationsDF



# ----------------------------    FUNCIONES PARA DIBUJAR EL GRAFO --------------------------

def song(level, i, auxNodes, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = ''

    # Añadimos el nodo de la propiedad si es necesario
    if (level.at[i, 'valueProperty'] not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: 3, level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambas canciones
    subEdges = ''',
    {from: "''' + level.at[i, 'ID_x'] + '''SX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''SY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def genre(level, i, auxNodes, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = ''

    # Añadimos el nodo del género X si es necesario, además de una arista para unirlo a la primera canción
    if ((level.at[i, 'ID_x'] + 'GX') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'ID_x'] + '''", group: 4, level: 3}'''

        subEdges = ''',
    {from: "''' + songX + '''SX", label: "genre", to: "''' + level.at[i, 'ID_x'] + '''GX"}'''

    # Añadimos el nodo del género Y si es necesario, además de una arista para unirlo a la segunda canción
    if ((level.at[i, 'ID_y'] + 'GY') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'ID_y'] + '''", group: 4, level: 5}'''

        subEdges = subEdges + ''',
    {from: "''' + songY + '''SY", label: "genre", to: "''' + level.at[i, 'ID_y'] + '''GY"}'''

    # Añadimos el nodo de la propiedad si es necesario
    if (level.at[i, 'valueProperty'] not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: 3, level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambos géneros
    subEdges = subEdges + ''',
    {from: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def artist(level, i, auxNodes, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = ''

    # Añadimos el nodo de la propiedad si es necesario
    if (level.at[i, 'valueProperty'] not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: 3, level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambos artistas
    subEdges = subEdges + ''',
    {from: "''' + level.at[i, 'ID_x'] + '''AX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''AY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def member(level, i, auxNodes, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = ''

    # Añadimos el nodo del miembro X si es necesario, además de una arista para unirlo al primer artista
    if ((level.at[i, 'ID_x'] + 'MX') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'ID_x'] + '''MX", label: "''' + level.at[i, 'ID_x'] + '''", group: 5, level: 3}'''

        subEdges = ''',
    {from: "''' + artistX + '''AX", label: "member", to: "''' + level.at[i, 'ID_x'] + '''MX"}'''

    # Añadimos el nodo del miembro Y si es necesario, además de una arista para unirlo al segundo artista
    if ((level.at[i, 'ID_y'] + 'MY') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'ID_y'] + '''MY", label: "''' + level.at[i, 'ID_y'] + '''", group: 5, level: 5}'''

        subEdges = subEdges + ''',
    {from: "''' + artistY + '''AY", label: "member", to: "''' + level.at[i, 'ID_y'] + '''MY"}'''

    # Añadimos el nodo de la propiedad si es necesario
    if (level.at[i, 'valueProperty'] not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: 3, level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambos miembros
    subEdges = subEdges + ''',
    {from: "''' + level.at[i, 'ID_x'] + '''MX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''MY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]
 
switcher = {
        2: song,
        3: genre,
        4: artist,
        5: member
    }

# ----------------------------    SECCIÓN DE LA APP Y SUS RUTAS ----------------------------

app = Sanic()

# Serves files from the static folder to the URL /static
app.static('/static', './static')

# Esta es la página principal de la aplicación
@app.route("/")
async def test(request):
    # os.getcwd() devuelve la URL actual
    # template = open(os.getcwd() + "/templates/index.html")
    # return html(template.read())

    # Si el html necesita valores, habría que añadirlos dentro de este template
    # separados por comas. Ej: template('index2.html', var1=var1, var2=var2)
    return template(
        'index2.html'
    )

@app.route("/table")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    #song1 = thislist[0][1]
    #artist1 = thislist[1][1]
    #song2 = thislist[2][1]
    #artist2 = thislist[3][1]

    song1 = "(I Can't Get No) Satisfaction" # "Start Me Up"
    artist1 = "The Rolling Stones"
    song2 = "Hey Jude" # "Let It Be"
    artist2 = "The Beatles"

    relationsDF = main(song1, artist1, song2, artist2) # relationsDF es un DataFrame

    return response.html(relationsDF.to_html())


@app.route("/result")
async def test(request):
    
    song1 = "(I Can't Get No) Satisfaction" # "Start Me Up"
    artist1 = "The Rolling Stones"

    song2 = "Hey Jude" # "Let It Be"
    artist2 = "The Beatles"
    relationsDF = main(song1,artist1,song2,artist2) # relationsDF es un DataFrame

    # Nos quedamos con un dataframe en el que solo aparecen las relaciones directas
    level = relationsDF.loc[relationsDF['Level_x'] == relationsDF['Level_y']]
    level.sort_values(by=['Level_x'], inplace= True)
    index = level.index.values.tolist()

    auxNodes = '''[
    {id: "''' + song1 + '''SX", label: "''' + song1 + '''", group: 1, level: 1},
    {id: "''' + song2 + '''SY", label: "''' + song2 + '''", group: 1, level: 7},
    {id: "''' + artist1 + '''AX", label: "''' + artist1 + '''", group: 2, level: 2},
    {id: "''' + artist2 + '''AY", label: "''' + artist2 + '''", group: 2, level: 6}'''

    auxEdges = '''[
    {from: "''' + song1 + '''SX", label: "artist", to: "''' + artist1 + '''AX"},
    {from: "''' + song2 + '''SY", label: "artist", to: "''' + artist2 + '''AY"}'''


    # Recorremos todas las relaciones del nivel 1
    for i in index:
        # Get the function from switcher dictionary
        func = switcher.get(level.at[i, 'Level_x'], "nothing")
        # Execute the function
        sub = func(level, i, auxNodes, song1, song2, artist1, artist2)

        auxNodes = auxNodes + sub[0]
        auxEdges = auxEdges + sub[1]

    myNodes = auxNodes + '''
]'''

    myEdges = auxEdges + '''
]'''

    #return response.html(level.to_html())
    return response.text(myNodes)


@app.route("/graph4")
async def test(request):

    return template(
        'graph4.html'
    )

@app.route("/index")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1 = thislist[0][1]
    artist1 = thislist[1][1]
    song2 = thislist[2][1]
    artist2 = thislist[3][1]
    relationsDF = main(song1,artist1,song2,artist2) # relationsDF es un DataFrame

    auxNodes = '''[
    {id: "''' + song1 + '''SX", label: "''' + song1 + '''", group: 1, level: 1},
    {id: "''' + song2 + '''SY", label: "''' + song2 + '''", group: 1, level: 7}'''


    if (artist1 == artist2):
        auxNodes = auxNodes + ''',
    {id: "''' + artist1 + '''", label: "''' + artist1 + '''", group: 2, level: 4}'''
        auxEdges = '''[
    {from: "''' + song1 + '''SX", label: "artist", to: "''' + artist1 + '''"},
    {from: "''' + song2 + '''SY", label: "artist", to: "''' + artist1 + '''"}'''

        # Nos quedamos con un dataframe en el que solo aparecen las relaciones directas
        level = relationsDF.loc[(relationsDF['Level_x'] == 2) & (relationsDF['Level_y'] == 2)]

    else:
        auxNodes = auxNodes + ''',
    {id: "''' + artist1 + '''AX", label: "''' + artist1 + '''", group: 2, level: 2},
    {id: "''' + artist2 + '''AY", label: "''' + artist2 + '''", group: 2, level: 6}'''
        auxEdges = '''[
    {from: "''' + song1 + '''SX", label: "artist", to: "''' + artist1 + '''AX"},
    {from: "''' + song2 + '''SY", label: "artist", to: "''' + artist2 + '''AY"}'''

        # Nos quedamos con un dataframe en el que solo aparecen las relaciones directas
        level = relationsDF.loc[relationsDF['Level_x'] == relationsDF['Level_y']]
        level.sort_values(by=['Level_x'], inplace= True)

    index = level.index.values.tolist()

    # Recorremos todas las relaciones del nivel 1
    for i in index:
        # Get the function from switcher dictionary
        func = switcher.get(level.at[i, 'Level_x'], "nothing")
        # Execute the function
        sub = func(level, i, auxNodes, song1, song2, artist1, artist2) #ERROR

        auxNodes = auxNodes + sub[0]
        auxEdges = auxEdges + sub[1]

    myNodes = auxNodes + '''
]'''

    myEdges = auxEdges + '''
]'''

    myData = """{
    nodes: nodes,
    edges: edges
}"""

    myOptions = """{
    layout: {
        hierarchical: {
            direction: 'LR',
            levelSeparation: 250
        }
    },
    edges: {
        arrows: 'to'/*,
        smooth: {
            type: 'cubicBezier',
            forceDirection: 'horizontal'
        }*/
    },
    nodes: {
        shape: 'box',
        widthConstraint: {
            maximum: 120
        }
    },
    physics: false
}"""

    with open(os.getcwd() + '/static/js/graph.js', 'w') as file:
        file.write(f"""
// create an array with nodes
var nodes = new vis.DataSet({myNodes});

// create an array with edges
var edges = new vis.DataSet({myEdges});

// create a network
var container = document.getElementById('mynetwork');

// provide the data in the vis format
var data = {myData};
var options = {myOptions};

// initialize your network!
var network = new vis.Network(container, data, options);
""".strip())

    return template(
        'graph.html'
    )

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', ''))
    )