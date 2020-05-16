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
                songData = getInfSong(song1['item.value'][0])
                genreData = getGenre2(songData,logger)
                artistData = getArtist2(songData,logger)
                membersData = getMembers2(artistData,logger)

                #SONG2
                songData2 = getInfSong(song2['item.value'][0])
                genreData2 = getGenre2(songData2,logger)
                artistData2 = getArtist2(songData2,logger)
                membersData2 = getMembers2(artistData2,logger)

                song1Data = [songData,genreData,artistData,membersData]
                song1Data = pd.concat(song1Data,sort=False)

                song2Data = [songData2,genreData2,artistData2,membersData2]
                song2Data = pd.concat(song2Data,sort=False)

                relationsDF = mergeData(song1Data,song2Data)
                relationsDF = relationsDF.drop_duplicates()

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
        'index2.html'
    )

# Esta es la ruta en la que se muestra nuestro estudio
# Por ahora muestra el dataframe dentro de una tabla,
# se sustituirá por un grafo en una actualización futura
@app.route("/result")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1= thislist[0][1]
    song2= thislist[1][1]
    relationsDF = main(song1,song2) # relationsDF es un DataFrame

    # Nos quedamos con un dataframe en el que solo aparecen las relaciones directas
    level = relationsDF.loc[(relationsDF['Level_x'] == 1) & (relationsDF['Level_y'] == 1)]
    index = level.index.values.tolist()
    
    # graph es un diccionario String:(lista de diccionarios)
    # Creamos el grafo sin aristas y con los nodos de las 2 canciones
    graph = {
        "nodes": [
          {
            "id": 1,
            "caption": "(I can't get no) Satisfaction",
            "root": True,
            "cluster": 1
          },
          {
            "id": 2,
            "caption": "Hey Jude",
            "root": True,
            "cluster": 2
          },
          {
            "id": 3,
            "caption": "aux1",
            "cluster": 3
          },
          {
            "id": 4,
            "caption": "aux2",
            "cluster": 3
          },
          {
            "id": 5,
            "caption": "aux3",
            "cluster": 3
          },
          {
            "id": 6,
            "caption": "aux4",
            "cluster": 3
          }
        ],
        "edges": [
            {
                "source": 1,
                "target": 3
            },
            {
                "source": 3,
                "target": 4
            },
            {
                "source": 2,
                "target": 5
            },
            {
                "source": 5,
                "target": 4
            },
            {
                "source": 3,
                "target": 6
            },
            {
                "source": 5,
                "target": 6
            }
        ]
      }

    # Recorremos todas las relaciones del nivel 1
    for i in index:
        # Añadimos un nodo
        aux1 = {
            "id": len(graph["nodes"])+1, # ID que toca usar
            "caption": level.at[i, 'valueProperty'], # Valor de la propiedad
            "cluster": 4
        }
        graph["nodes"].append(aux1)

        # Añadimos dos aristas para este nodo
        aux2 = {
            "source": 1, # ID de la primera canción
            "target": aux1["id"], # ID del nodo que acabamos de crear
            "caption": level.at[i, 'idPropertyName'] # Nombre de la propiedad
        }
        aux3 = {
            "source": 2, # ID de la segunda canción
            "target": aux1["id"], # ID del nodo que acabamos de crear
            "caption": level.at[i, 'idPropertyName'] # Nombre de la propiedad
        }
        graph["edges"].append(aux2)
        graph["edges"].append(aux3)

    # Guardamos el grafo en un archivo .json
    with open(os.getcwd() + '/static/data/level1.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False)

    return template(
        'graph4.html'
    )

    #return response.json(open(os.getcwd() + '/static/data/level1.json', 'r').read())
    #return response.html(level.to_html())
    #return response.text(graph["edges"])

    #return response.html(relationsDF.to_html())

@app.route("/result2")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1= thislist[0][1]
    song2= thislist[1][1]
    relationsDF = main(song1,song2) # relationsDF es un DataFrame

    return response.html(relationsDF.to_html())

@app.route("/table")
async def test(request):
    
    song1 = 'Start Me Up'
    artist1 = 'The Rolling Stones'

    song2 = 'Let It Be'
    artist2 = 'The Beatles'
    relationsDF = main(song1,artist1,song2,artist2) # relationsDF es un DataFrame

    return response.html(relationsDF.to_html())

@app.route("/graph4")
async def test(request):

    return template(
        'graph4.html'
    )

@app.route("/index")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1= thislist[0][1]
    song2= thislist[1][1]
    relationsDF = main(song1,song2) # relationsDF es un DataFrame

    with open(os.getcwd() + '/static/js/prueba.js', 'w') as file:
        file.write("""
// create an array with nodes
var nodes = new vis.DataSet([
    {id: 1, label: 'Node 1', level: 2},
    {id: 2, label: 'Node 2', level: 4},
    {id: 3, label: 'Satisfaction', level: 1},
    {id: 4, label: 'Hey Jude', level: 5},
    {id: 5, label: 'Node 5', level: 3},
    {id: 6, label: 'Node 6', level: 3}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: 3, to: 1},
    {from: 1, to: 5},
    {from: 4, to: 2},
    {from: 2, to: 5},
    {from: 1, to: 6},
    {from: 2, to: 6}
]);

// create a network
var container = document.getElementById('mynetwork');

// provide the data in the vis format
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
    layout: {
        hierarchical: {
            direction: 'LR'
        }
    },
    edges: {
        arrows: 'to',
        smooth: {
            type: 'cubicBezier',
            forceDirection: 'horizontal'
        }
    }
};

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