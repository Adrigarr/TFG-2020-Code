import logging
import sys
from datetime import datetime, timedelta
from getInfoSongs import *
from sparqlLibrary import *
from draw import *

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
        'template.html'
    )

# TEMPORAL
@app.route("/table")
async def test(request):

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
@app.route("/graph4")
async def test(request):

    return template(
        'graph4.html'
    )

# TEMPORAL
@app.route("/prueba")
async def test(request):

    return template(
        'template.html'
    )

# TEMPORAL
@app.route("/random")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    return response.text(thislist)

#WIP
@app.route("/index")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1 = cleanSong(thislist[0][1])[0]
    artist1 = cleanSong(thislist[0][1])[1]
    song2 = cleanSong(thislist[1][1])[0]
    artist2 = cleanSong(thislist[1][1])[1]
    relationsDF = main(song1,artist1,song2,artist2) # relationsDF es un DataFrame

    auxNodes = '''[
    {id: "''' + song1 + '''SX", label: "''' + song1 + '''", group: "song", level: 1},
    {id: "''' + song2 + '''SY", label: "''' + song2 + '''", group: "song", level: 7}'''

    # Nos quedamos con la lista de artistas que coinciden en ambas canciones
    artistList = relationsDF.loc[(relationsDF['idPropertyName'] == 'artist')]

    # Si coincide algún artista, lo tomamos como una relación directa
    if (not artistList.empty):
        index = artistList.index.values.tolist()

        nodoArtistas = ''',
    {id: "artists", label: "''' + artist1 + '''", group: "artist", level: 4}'''

        auxNodes = auxNodes + nodoArtistas

        posicion = auxNodes.find(nodoArtistas) # La posición del nodo
        splited = nodoArtistas.split(artist1) # Partimos nuestra búsqueda para tener la primera parte de la cadena, es decir, todo hasta llegar al label

        # Por cada artista 
        for j in index:

            if (artistList.at[j, 'valueProperty'] not in auxNodes[(posicion + len(splited[0])):]):
                # Añadimos el nombre del artista a la etiqueta del nodo
                auxNodes = auxNodes[:(posicion + len(splited[0]))] + artistList.at[j, 'valueProperty'] + ', ' + auxNodes[(posicion + len(splited[0])):]

        # Añadimos las aristas para unir la propiedad con ambas canciones
        auxEdges = '''{from: "''' + song1 + '''SX", label: "artist", to: "artists"},
        {from: "''' + song2 + '''SY", label: "artist", to: "artists"}'''
            
        # Nos quedamos con un dataframe en el que solo aparecen las relaciones del mismo nivel pero sin contar el estudio de miembros
        level = relationsDF.loc[(relationsDF['Level_x'] == relationsDF['Level_y']) & (relationsDF['Level_x'] != 5)
                                & (relationsDF['idPropertyName'] != 'artist')]
        level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)

    else:
        auxNodes = auxNodes + ''',
    {id: "''' + artist1 + '''AX", label: "''' + artist1 + '''", group: "artist", level: 2},
    {id: "''' + artist2 + '''AY", label: "''' + artist2 + '''", group: "artist", level: 6}'''

        auxEdges = '''{from: "''' + song1 + '''SX", label: "artist", to: "''' + artist1 + '''AX"},
    {from: "''' + song2 + '''SY", label: "artist", to: "''' + artist2 + '''AY"}'''

        # Nos quedamos con un dataframe en el que solo aparecen las relaciones del mismo nivel
        level = relationsDF.loc[(relationsDF['Level_x'] == relationsDF['Level_y']) & (relationsDF['Level_x'] != 5)]
        level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)

    
    auxNodes2 = auxNodes
    auxEdges2 = auxEdges

    index = level.index.values.tolist()

    # Recorremos todas las relaciones
    for i in index:
        # Get the function from switcher dictionary
        func = switcher.get(level.at[i, 'Level_x'], "nothing")
        # Execute the function
        sub = func(level, i, auxNodes, auxEdges, song1, song2, artist1, artist2)

        auxNodes = auxNodes + sub[0]
        auxEdges = sub[1]

    nolevel = relationsDF.loc[(relationsDF['Level_x'] != relationsDF['Level_y']) & (relationsDF['Level_x'] != 5) & (relationsDF['Level_y'] != 5)]
    nolevel.sort_values(by=['Level_x', 'Level_y', 'idPropertyName', 'valueProperty'], inplace= True)
    
    noindex = nolevel.index.values.tolist()

    for k in noindex:
        # Get the function from switcher dictionary
        func = switcher2.get(nolevel.at[k, 'Level_x'], "nothing")
        # Execute the function
        subx = func(nolevel, k, auxNodes2, auxEdges2, song1, song2, artist1, artist2, 'x')

        auxNodes2 = auxNodes2 + subx[0]
        auxEdges2 = subx[1]

        # Get the function from switcher dictionary
        func = switcher2.get(nolevel.at[k, 'Level_y'], "nothing")
        # Execute the function
        suby = func(nolevel, k, auxNodes2, auxEdges2, song1, song2, artist1, artist2, 'y')

        auxNodes2 = auxNodes2 + suby[0]
        auxEdges2 = suby[1]

    # ESTUDIO DE LOS MIEMBROS
    stringAX = '''{id: ".*AX",'''
    stringAY = '''{id: ".*AY",'''

    nodosAX = re.findall(stringAX, auxNodes)
    nodosAY = re.findall(stringAY, auxNodes)

    # Si solo hay un artista por lado, estudiamos las explicaciones de miembros
    if ((len(nodosAX) == 1) & (len(nodosAY) == 1)):
        # Nos quedamos con un dataframe en el que solo aparecen las relaciones del mismo nivel
        level = relationsDF.loc[(relationsDF['Level_x'] == relationsDF['Level_y']) & (relationsDF['Level_x'] == 5)]
        level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)

        index = level.index.values.tolist()

        # Recorremos todas las relaciones
        for i in index:
            # Get the function from switcher dictionary
            func = switcher.get(level.at[i, 'Level_x'], "nothing")
            # Execute the function
            sub = func(level, i, auxNodes, auxEdges, song1, song2, artist1, artist2)

            auxNodes = auxNodes + sub[0]
            auxEdges = sub[1]


        nolevel = relationsDF.loc[(relationsDF['Level_x'] != relationsDF['Level_y']) & ((relationsDF['Level_x'] == 5) | (relationsDF['Level_y'] == 5))]
        nolevel.sort_values(by=['Level_x', 'Level_y', 'idPropertyName', 'valueProperty'], inplace= True)
        
        noindex = nolevel.index.values.tolist()

        for k in noindex:
            # Get the function from switcher dictionary
            func = switcher2.get(nolevel.at[k, 'Level_x'], "nothing")
            # Execute the function
            subx = func(nolevel, k, auxNodes2, auxEdges2, song1, song2, artist1, artist2, 'x')

            auxNodes2 = auxNodes2 + subx[0]
            auxEdges2 = subx[1]

            # Get the function from switcher dictionary
            func = switcher2.get(nolevel.at[k, 'Level_y'], "nothing")
            # Execute the function
            suby = func(nolevel, k, auxNodes2, auxEdges2, song1, song2, artist1, artist2, 'y')

            auxNodes2 = auxNodes2 + suby[0]
            auxEdges2 = suby[1]



    myNodes = auxNodes + '''
]'''

    myEdges = '''[
    ''' + auxEdges + '''
]'''

    myNodes2 = auxNodes2 + '''
]'''

    myEdges2 = '''[
    ''' + auxEdges2 + '''
]'''

    myData = """{
    nodes: nodes,
    edges: edges
}"""

    myData2 = """{
    nodes: nodes2,
    edges: edges2
}"""

    myOptions = """{
    layout: {
        hierarchical: {
            direction: 'LR',
            levelSeparation: 250,
            nodeSpacing: 150
        }
    },
    edges: {
        arrows: 'to',
        arrowStrikethrough: false,
        scaling: {
            label: false
        },
        font: {
            size: 16,
            align: 'middle'
        },
        shadow: true
    },
    nodes: {
        shape: 'box',
        widthConstraint: {
            maximum: 150
        },
        font: {
            size: 18
        },
        shadow: true
    },
    groups: {
        song: {
            color: 'DodgerBlue',
            font: '24px arial #ffffff',
            widthConstraint: {
                maximum: 180
            }
        },
        genre: {
            color: 'LawnGreen'
        },
        artist: {
            color: 'Crimson',
            font: '20px arial #ffffff'
        },
        member: {
            color: 'Orchid'
        },
        center: {
            color: 'Khaki'
        }
    },
    physics: false
}"""

    # Añadimos la hora actual al .js para tener un control de versiones.
    # De esta forma nos aseguramos de que el cliente tenga siempre el .js
    # correcto.
    x = datetime.now()
    date = f"{x.year}{x.month}{x.day}{x.hour}{x.minute}{x.second}"

    with open(os.getcwd() + '/static/js/graph' + date + '.js', 'w') as file:
        file.write(f"""
// create an array with nodes
var nodes = new vis.DataSet({myNodes});
var nodes2 = new vis.DataSet({myNodes2});

// create an array with edges
var edges = new vis.DataSet({myEdges});
var edges2 = new vis.DataSet({myEdges2});

// create a network
var container = document.getElementById('mynetwork');
var container2 = document.getElementById('mynetwork2');

// provide the data in the vis format
var data = {myData};
var data2 = {myData2};
var options = {myOptions};

// initialize your networks!
var network = new vis.Network(container, data, options);
var network2 = new vis.Network(container2, data2, options);

network.moveTo({{
  scale: 0.5             // Zooms out
}});
network2.moveTo({{
  scale: 0.5             // Zooms out
}});
""".strip())

    return template(
        'graph.html',
        var1 = date
    )

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', ''))
    )