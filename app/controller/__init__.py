from sanic import response
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
import os
import logging
from datetime import datetime, timedelta
import requests
import csv


# local imports
from app import app
from app.helpers.draw import *
from app.helpers.graphmaking import *

from app.model.main import *
#from app.model.getInfoSongs import *
#from app.model.sparqlLibrary import *

# define the environment for the Jinja2 templates
env = Environment(
    loader=PackageLoader('main', 'app/view'),
    autoescape=select_autoescape(['html', 'xml', 'tpl'])
)

# a function for loading an HTML template from the Jinja environment
def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return response.html(template.render(kwargs))





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

    song1 = cleanSong(thislist[0][1])[0]
    artist1 = cleanSong(thislist[0][1])[1]
    song2 = cleanSong(thislist[1][1])[0]
    artist2 = cleanSong(thislist[1][1])[1]

    objectMain = Main(song1, artist1, song2, artist2) # relationsDF es un DataFrame
    
    relationsDF = objectMain.relations
    
    return response.html(relationsDF.to_html())

# Función que sirve para generar un archivo con todas las consultas erróneas. Está por testear
async def status(request):

    tracklist = []

    with open(os.getcwd() + '/app/static/csv/cleanDataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if (len(row) > 2):
                    song = row[0][1:len(row[0])]
                    i = 1
                    while i < len(row)-1: 
                        song += ',' + row[i]
                        i += 1

                    song += ',' + row[i][0:len(row[i]-1)] + ' — ' + row[-1]

                else: 
                    song = row[0] + ' — ' + row[1]

                tracklist.append(song)

                line_count += 1

    file = open(os.getcwd() + '/app/static/status.txt', 'w')

    for a in tracklist:
        for b in tracklist:
            if a != b:
                payload = {"xsong": a,
                           "ysong": b}
                
                req = requests.get('https://explicaciones.herokuapp.com/index', params=payload)

                status = req.status_code

                if (status != 200):
                    file.write('song1: ' + a + ' / song2: ' + b + ' status: ' + str(status) + '\n')

    file.close()

    return response.text('OK')

# Esta es la ruta a la que se dirige tras pulsar el botón de comparación
# Se llama a las funciones necesarias para obtener los grafos y se muestran por pantalla
async def index(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1 = cleanSong(thislist[0][1])[0]
    artist1 = cleanSong(thislist[0][1])[1]
    song2 = cleanSong(thislist[1][1])[0]
    artist2 = cleanSong(thislist[1][1])[1]

    objectMain = Main(song1, artist1, song2, artist2) # relationsDF es un DataFrame

    relationsDF = objectMain.relations

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
app.add_route(status, '/status')

#@app.route("/")
#@app.route("/table")
#@app.route("/graph4")
#@app.route("/random")
#@app.route("/index")