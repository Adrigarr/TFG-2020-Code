import os
from app.helpers.draw import *

# Función que hace un estudio de los artistas para comprobar si alguno coincide 
# RECIBE:    Dataframe relationsDF            => dataframe con la información de las explicaciones,
#            String auxNodes                  => lista denodos del grafo de explicaciones de la misma categoría
#            String song1                     => título de la primera canción,
#            String song2                     => título de la segunda canción,
#            String artist1                   => nombre del primer artista,
# DEVUELVE:  array de 2 Strings y 1 dataframe => auxNodes es la nueva lista de nodos,
#                                                auxEdges es la lista de aristas,
#                                                level es un dataframe con las relaciones del mismo nivel pero sin los miembros
def artistTreatment(relationsDF, auxNodes, song1, song2, artist1):

    # Nos quedamos con la lista de artistas que coinciden en ambas canciones
    artistList = relationsDF.loc[(relationsDF['idPropertyName'] == 'performer')]
    
    # Si coincide algún artista, lo tomamos como una relación directa
    if (not artistList.empty):
        index = artistList.index.values.tolist()

        nodoArtistas = ''',
    {id: "artists", label: "''' + artist1 + '''", title: "Artist", group: "artist", level: 4}'''

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
        level = relationsDF.loc[(relationsDF['Level_x'] == relationsDF['Level_y']) & (relationsDF['Level_x'] != 4)
                                & (relationsDF['idPropertyName'] != 'performer')]
        level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)

    else:

        auxEdges = '''{}'''

        # Nos quedamos con un dataframe en el que solo aparecen las relaciones del mismo nivel pero sin contar el estudio de miembros
        level = relationsDF.loc[(relationsDF['Level_x'] == relationsDF['Level_y']) & (relationsDF['Level_x'] != 4)]
        level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)


    return [auxNodes, auxEdges, level]



# Función que genera el archivo graph.js, que contendrá todo lo necesario para dibujar los grafos de explicaciones
# RECIBE:   String song1          => título de la primera canción,
#           String song2          => título de la segunda canción,
#           String artist1        => nombre del primer artista,
#           String artist2        => nombre del segundo artista,
#           Dataframe relationsDF => dataframe con la información de las explicaciones
def generateGraph(song1, song2, artist1, artist2, relationsDF):

    auxNodes = '''[
    {id: "''' + song1 + '''SX", label: "''' + song1 + '''", title: "Song", group: "song", level: 1},
    {id: "''' + song2 + '''SY", label: "''' + song2 + '''", title: "Song", group: "song", level: 7}'''

    # Se hace un estudio de los artistas y se inicializa la lista de aristas
    aux = artistTreatment(relationsDF, auxNodes, song1, song2, artist1)

    auxNodes = aux[0]
    auxEdges = aux[1]
    level = aux[2] # dataframe en el que solo aparecen las relaciones del mismo nivel pero sin contar el estudio de miembros
    
    auxNodes2 = auxNodes
    auxEdges2 = auxEdges

    index = level.index.values.tolist()

    # Recorremos todas las relaciones
    for i in index:
        # Get the function from switcher dictionary
        func = switcher.get(level.at[i, 'Level_x'], "nothing")
        # Execute the function
        sub = func(level, i, auxNodes, auxEdges, song1, song2, artist1, artist2, 'z')

        auxNodes = auxNodes + sub[0]
        auxEdges = sub[1]

    nolevel = relationsDF.loc[(relationsDF['Level_x'] != relationsDF['Level_y']) & (relationsDF['Level_x'] != 4) & (relationsDF['Level_y'] != 4)]
    nolevel.sort_values(by=['Level_x', 'Level_y', 'idPropertyName', 'valueProperty'], inplace= True)
    
    noindex = nolevel.index.values.tolist()

    for k in noindex:
        # Get the function from switcher dictionary
        func = switcher.get(nolevel.at[k, 'Level_x'], "nothing")
        # Execute the function
        subx = func(nolevel, k, auxNodes2, auxEdges2, song1, song2, artist1, artist2, 'x')

        auxNodes2 = auxNodes2 + subx[0]
        auxEdges2 = subx[1]

        # Get the function from switcher dictionary
        func = switcher.get(nolevel.at[k, 'Level_y'], "nothing")
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
        level = relationsDF.loc[(relationsDF['Level_x'] == relationsDF['Level_y']) & (relationsDF['Level_x'] == 4)]
        level.sort_values(by=['Level_x', 'idPropertyName', 'valueProperty'], inplace= True)

        index = level.index.values.tolist()

        # Recorremos todas las relaciones
        for i in index:
            # Get the function from switcher dictionary
            func = switcher.get(level.at[i, 'Level_x'], "nothing")
            # Execute the function
            sub = func(level, i, auxNodes, auxEdges, song1, song2, artist1, artist2, 'z')

            auxNodes = auxNodes + sub[0]
            auxEdges = sub[1]


        nolevel = relationsDF.loc[(relationsDF['Level_x'] != relationsDF['Level_y']) & ((relationsDF['Level_x'] == 4) | (relationsDF['Level_y'] == 4))]
        nolevel.sort_values(by=['Level_x', 'Level_y', 'idPropertyName', 'valueProperty'], inplace= True)
        
        noindex = nolevel.index.values.tolist()

        for k in noindex:
            # Get the function from switcher dictionary
            func = switcher.get(nolevel.at[k, 'Level_x'], "nothing")
            # Execute the function
            subx = func(nolevel, k, auxNodes2, auxEdges2, song1, song2, artist1, artist2, 'x')

            auxNodes2 = auxNodes2 + subx[0]
            auxEdges2 = subx[1]

            # Get the function from switcher dictionary
            func = switcher.get(nolevel.at[k, 'Level_y'], "nothing")
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
        shadow: true,
        chosen: {
            label: false,
            node: changeChosenNodeBorder
        }
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


    if os.path.exists(os.getcwd() + '/app/static/js/graph.js'):
        os.remove(os.getcwd() + '/app/static/js/graph.js')

    with open(os.getcwd() + '/app/static/js/graph.js', 'w') as file:
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

var changeChosenNodeBorder = function (values, id, selected, hovering) {{
  values.borderColor = "#000000";
  values.borderWidth = 2;
}};

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
  scale: 0.15             // Zooms out
}});
""".strip())