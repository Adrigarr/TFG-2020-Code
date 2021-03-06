import re

# ----------------------------    FUNCIONES PARA DIBUJAR EL GRAFO --------------------------

# Esta función analiza una explicación relacionada con el estudio de la canción y genera los nodos y aristas
# necesarios para representarla en el grafo. Puede utilizarse para relaciones entre ambas canciones o entre
# una canción y otro elemento, en cuyo caso solo se llama a esta función para el lado de la canción.
# RECIBE:   dataframe level => dataframe con el que trabajamos,
#           integer i       => índice actual del dataframe,
#           String auxNodes => lista de nodos del grafo,
#           String auxEdges => lista de aristas del grafo,
#           Sring songX     => primera canción a comparar,
#           String songY    => segunda canción a comparar,
#           String artistX  => artista de la primera canción,
#           String artistY  => artista de la segunda canción,
#           String XY       => carácter de control 'x'/'y'/'z'
# DEVUELVE: array de String => subNodes es la lista de nodos a añadir y subEdges es la nueva lista de aristas
def song(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    edgeSX = '''{from: "''' + level.at[i, 'ID_x'] + '''SX", label: "''' + level.at[i, 'idPropertyName_x'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''
    edgeSY = '''{from: "''' + level.at[i, 'ID_y'] + '''SY", label: "''' + level.at[i, 'idPropertyName_x'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # ------------------------------------------------------ XZ --------------------------------------------------------------
    # Si es una explicación de la misma categoría o de distinta categoría por la derecha
    if (XY != 'y'):
        if (edgeSX not in subEdges):
            subEdges += ''',
    ''' + edgeSX

    # ------------------------------------------------------ YZ --------------------------------------------------------------
    # Si es una explicación de la misma categoría o de distinta categoría por la derecha
    if (XY != 'x'):
        if (edgeSY not in subEdges):
            subEdges += ''',
    ''' + edgeSY

    return [subNodes, subEdges]


# Esta función analiza una explicación relacionada con el estudio del género y genera los nodos y aristas
# necesarios para representarla en el grafo. Puede utilizarse para relaciones entre dos géneros o entre
# un género y otro elemento, en cuyo caso solo se llama a esta función para el lado del género.
# RECIBE:   dataframe level => dataframe con el que trabajamos,
#           integer i       => índice actual del dataframe,
#           String auxNodes => lista de nodos del grafo,
#           String auxEdges => lista de aristas del grafo,
#           Sring songX     => primera canción a comparar,
#           String songY    => segunda canción a comparar,
#           String artistX  => artista de la primera canción,
#           String artistY  => artista de la segunda canción,
#           String XY       => carácter de control 'x'/'y'/'z'
# DEVUELVE: array de String => subNodes es la lista de nodos a añadir y subEdges es la nueva lista de aristas
def genre(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    # Si ambos elementos a comparar son el mismo, termina la función. Esto ocurrirá en las explicaciones del mismo nivel que comparen un
    # género consigo mismo
    if (level.at[i, 'ID_x'] == level.at[i, 'ID_y']):
        return [subNodes, subEdges]

    edgeSX = '''{from: "''' + songX + '''SX", label: "genre", to: "''' + level.at[i, 'ID_x'] + '''GX"}'''
    edgeSY = '''{from: "''' + songY + '''SY", label: "genre", to: "''' + level.at[i, 'ID_y'] + '''GY"}'''
    edgeGX = '''{from: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'idPropertyName_x'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''
    edgeGY = '''{from: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'idPropertyName_x'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''


    # ------------------------------------------------------ XZ --------------------------------------------------------------
    # Si es una explicación de la misma categoría o de distinta categoría por la izquierda
    if (XY != 'y'):
        # Añadimos el nodo del género si es necesario, además de una arista para unirlo a la canción correspondiente
        if ((level.at[i, 'ID_x'] + 'GX') not in auxNodes):
            subNodes += ''',
    {id: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'ID_x'] + ''' ", title: "Genre", group: "genre", level: 3}'''

        if (edgeSX not in subEdges):
            subEdges += ''',
    ''' + edgeSX

        # Añadimos la arista para unir la propiedad con el género
        if (edgeGX not in subEdges):
            subEdges += ''',
    ''' + edgeGX


    # ------------------------------------------------------ YZ --------------------------------------------------------------
    # Si es una explicación de la misma categoría o de distinta categoría por la derecha
    if (XY != 'x'):
        # Añadimos el nodo del género si es necesario, además de una arista para unirlo a la canción correspondiente
        if ((level.at[i, 'ID_y'] + 'GY') not in auxNodes):
            subNodes += ''',
    {id: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'ID_y'] + ''' ", title: "Genre", group: "genre", level: 5}'''

        if (edgeSY not in subEdges):
            subEdges += ''',
    ''' + edgeSY

        # Añadimos la arista para unir la propiedad con el género
        if (edgeGY not in subEdges):
            subEdges += ''',
    ''' + edgeGY


    #------------------------------------------------------ XYZ --------------------------------------------------------------
    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes += ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''


    return [subNodes, subEdges]


# Esta función analiza una explicación relacionada con el estudio del artista y genera los nodos y aristas
# necesarios para representarla en el grafo. Puede utilizarse para relaciones entre dos artistas o entre
# un artista y otro elemento, en cuyo caso solo se llama a esta función para el lado del artista.
# RECIBE:   dataframe level => dataframe con el que trabajamos,
#           integer i       => índice actual del dataframe,
#           String auxNodes => lista de nodos del grafo,
#           String auxEdges => lista de aristas del grafo,
#           Sring songX     => primera canción a comparar,
#           String songY    => segunda canción a comparar,
#           String artistX  => artista de la primera canción,
#           String artistY  => artista de la segunda canción,
#           String XY       => carácter de control 'x'/'y'/'z'
# DEVUELVE: array de String => subNodes es la lista de nodos a añadir y subEdges es la nueva lista de aristas
def artist(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    nodoArtistas = '''{id: "artists", label: ".*", title: "Artist", group: "artist", level: 4}'''

    # Si alguno de los artistas pertenece a la explicación directa "Artista" entre las canciones, la función termina
    if (re.findall(nodoArtistas, auxNodes) and ((level.at[i, 'ID_x'] in re.findall(nodoArtistas, auxNodes)[0]) or (level.at[i, 'ID_y'] in re.findall(nodoArtistas, auxNodes)[0]))):
        return [subNodes, subEdges]

    edgeSX = '''{from: "''' + songX + '''SX", label: "artist", to: "''' + level.at[i, 'ID_x'] + '''AX"}'''
    edgeSY = '''{from: "''' + songY + '''SY", label: "artist", to: "''' + level.at[i, 'ID_y'] + '''AY"}'''
    edgeAX = '''{from: "''' + level.at[i, 'ID_x'] + '''AX", label: "''' + level.at[i, 'idPropertyName_x'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''
    edgeAY = '''{from: "''' + level.at[i, 'ID_y'] + '''AY", label: "''' + level.at[i, 'idPropertyName_x'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''



    # ------------------------------------------------------ XZ --------------------------------------------------------------
    if (XY != 'y'):
        # Añadimos el nodo del artista X si es necesario, además de una arista para unirlo a la primera canción
        if ((level.at[i, 'ID_x'] + 'AX') not in auxNodes):
            subNodes += ''',
    {id: "''' + level.at[i, 'ID_x'] + '''AX", label: "''' + level.at[i, 'ID_x'] + ''' ", title: "Artist", group: "artist", level: 2}'''

        if (edgeSX not in subEdges):
            subEdges += ''',
    ''' + edgeSX

        # Añadimos la arista para unir la propiedad con el artista
        if (edgeAX not in subEdges):
            subEdges += ''',
    ''' + edgeAX


    # ------------------------------------------------------ YZ --------------------------------------------------------------
    if (XY != 'x'):
        # Añadimos el nodo del artista Y si es necesario, además de una arista para unirlo a la primera canción
        if ((level.at[i, 'ID_y'] + 'AY') not in auxNodes):
            subNodes += ''',
    {id: "''' + level.at[i, 'ID_y'] + '''AY", label: "''' + level.at[i, 'ID_y'] + ''' ", title: "Artist", group: "artist", level: 6}'''

        if (edgeSY not in subEdges):
            subEdges += ''',
    ''' + edgeSY

        # Añadimos la arista para unir la propiedad con el artista
        if (edgeAY not in subEdges):
            subEdges += ''',
    ''' + edgeAY


    # ------------------------------------------------------ XYZ --------------------------------------------------------------
    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes += ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''


    return [subNodes, subEdges]


# Esta función analiza una explicación relacionada con el estudio de los miembros y genera los nodos y aristas
# necesarios para representarla en el grafo. Puede utilizarse para relaciones entre dos miembros o entre
# un miembro y otro elemento, en cuyo caso solo se llama a esta función para el lado del miembro.
# RECIBE:   dataframe level => dataframe con el que trabajamos,
#           integer i       => índice actual del dataframe,
#           String auxNodes => lista de nodos del grafo,
#           String auxEdges => lista de aristas del grafo,
#           Sring songX     => primera canción a comparar,
#           String songY    => segunda canción a comparar,
#           String artistX  => artista de la primera canción,
#           String artistY  => artista de la segunda canción,
#           String XY       => carácter de control 'x'/'y'/'z'
# DEVUELVE: array de String => subNodes es la lista de nodos a añadir y subEdges es la nueva lista de aristas
def member(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    # Si ambos elementos a comparar son el mismo, termina la función. Esto ocurrirá en las explicaciones del mismo nivel que comparen un
    # género consigo mismo
    if (level.at[i, 'ID_x'] == level.at[i, 'ID_y']):
        return [subNodes, subEdges]

    edgeAX = '''{from: "''' + artistX + '''AX", label: "members", to: "MembersX"}'''
    edgeAY = '''{from: "''' + artistY + '''AY", label: "members", to: "MembersY"}'''
    edgeSX = '''{from: "''' + songX + '''SX", label: "artist", to: "''' + artistX + '''AX"}'''
    edgeSY = '''{from: "''' + songY + '''SY", label: "artist", to: "''' + artistY + '''AY"}'''

    # Si es una explicación de distinta categoría por la izquierda
    if (XY != 'y'):
        # Añadimos el nodo del miembro X si es necesario, además de una arista para unirlo al primer artista
        if ('MembersX' not in auxNodes):
            subNodes += ''',
    {id: "MembersX", label: "Members of ''' + artistX + '''", title: "Members", group: "member", level: 3}'''
            
            subEdges += ''',
    ''' + edgeAX

        # Añadimos el nodo del artista X si es necesario, además de una arista para unirlo a la primera canción
        # Esta parte es útil para los grafos de explicaciones de distinta categoría/nivel
        if (artistX+'AX' not in auxNodes):
            subNodes += ''',
    {id: "''' + artistX + '''AX", label: "''' + artistX + ''' ", title: "Artist", group: "artist", level: 2}'''

        if (edgeSX not in subEdges):
                subEdges += ''',
        ''' + edgeSX

    # Si es una explicación de distinta categoría por la derecha
    if (XY != 'x'):
        # Añadimos el nodo del miembro Y si es necesario, además de una arista para unirlo al segundo artista
        if ('MembersY' not in auxNodes):
            subNodes += ''',
    {id: "MembersY", label: "Members of ''' + artistY + '''", title: "Members", group: "member", level: 5}'''
            
            subEdges += ''',
    ''' + edgeAY

        # Añadimos el nodo del artista Y si es necesario, además de una arista para unirlo a la segunda canción
        # Esta parte es útil para los grafos de explicaciones de distinta categoría/nivel
        if (artistY+'AY' not in auxNodes):
            subNodes += ''',
    {id: "''' + artistY + '''AY", label: "''' + artistY + ''' ", title: "Artist", group: "artist", level: 6}'''

        if (edgeSY not in subEdges):
                subEdges += ''',
        ''' + edgeSY

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes += ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # ------------------------------------------------------ Z --------------------------------------------------------------
    # Si es una explicación de la misma categoría
    if (XY == 'z'):
        # Añadimos las aristas para unir la propiedad con ambos miembros
        x = level.at[i, 'ID_x']
        y = level.at[i, 'ID_y']
        buscadoX = 'from: "MembersX", label: "' + level.at[i, 'idPropertyName_x'] +'", title: ".*", value: ., to: "' + level.at[i, 'valueProperty'] + '"'
        buscadoY = 'from: "MembersY", label: "' + level.at[i, 'idPropertyName_x'] +'", title: ".*", value: ., to: "' + level.at[i, 'valueProperty'] + '"'

        # Buscamos todas las apariciones de buscadoX, con lo que obtenemos la arista exacta (si la hay)
        encontradoX = re.findall(buscadoX, subEdges) # NOTA: Esto es una lista (que debería tener uno o cero elementos)

        # Si ya existe esa arista, la estudiamos para editarla (si es necesario)
        if encontradoX:

            index = subEdges.find(encontradoX[0]) # La posición de la arista X
            splited = buscadoX.split('.*') # Partimos nuestra búsqueda para tener la primera parte de la cadena, es decir, todo hasta llegar al título

            # Si el miembro X no está en el título de la arista, lo añadimos y aumentamos el valor
            # NOTA: Esta comprobación funciona porque el dataframe está ordenado. Si se cambia el orden, habría
            #       que modificar esta parte
            if (x not in subEdges[(index + len(splited[0])):]):

                # Limpiamos el string de la arista para obtener el valor antiguo
                auxiliar = re.sub('from: "MembersX", label: "' + level.at[i, 'idPropertyName_x'] +
                    '", title: ".*", value: ', '', encontradoX[0])

                value = re.sub(', to: "' + level.at[i, 'valueProperty'] + '"', '', auxiliar)

                # Actualizamos el valor
                incremento = int(value) + 1
                nuevaArista = encontradoX[0].replace(value,str(incremento), 1)
                subEdges = re.sub(encontradoX[0], nuevaArista, subEdges)    
                
                # Añadimos el nombre del miembro X al título de la arista
                subEdges = subEdges[:(index + len(splited[0]))] + x + ', ' + subEdges[(index + len(splited[0])):]


            # Buscamos todas las apariciones de buscadoX, con lo que obtenemos la arista exacta
            encontradoY = re.findall(buscadoY, subEdges) # NOTA: Esto es una lista (que debería tener un solo elemento)

            index = subEdges.find(encontradoY[0]) # La posición de la arista Y
            splited = buscadoY.split('.*') # Partimos nuestra búsqueda para tener la primera parte de la cadena, es decir, todo hasta llegar al título

            # Si el miembro Y no está en el título de la arista, lo añadimos y aumentamos el valor
            # NOTA: Esta comprobación funciona porque el dataframe está ordenado. Si se cambia el orden, habría
            #       que modificar esta parte
            if (y not in subEdges[(index + len(splited[0])):]):   

                # Limpiamos el string de la arista para obtener el valor antiguo
                auxiliar = re.sub('from: "MembersY", label: "' + level.at[i, 'idPropertyName_x'] +
                    '", title: ".*", value: ','',encontradoY[0])

                value = re.sub(', to: "' + level.at[i, 'valueProperty'] + '"', '', auxiliar)

                # Actualizamos el valor
                incremento = int(value) + 1
                nuevaArista = encontradoY[0].replace(value,str(incremento), 1)
                subEdges = re.sub(encontradoY[0], nuevaArista, subEdges)

                # Añadimos el nombre del miembro X al título de la arista
                subEdges = subEdges[:(index + len(splited[0]))] + y + ', ' + subEdges[(index + len(splited[0])):]
        

        # Si no existe la arista de los miembros X a la propiedad, añadimos las dos aristas que forman la explicación
        else:

          subEdges += ''',
        {from: "MembersX", label: "''' + level.at[i, 'idPropertyName_x'] + '''", title: "''' + x + '''", value: 1, to: "''' + level.at[i, 'valueProperty'] + '''"},
        {from: "MembersY", label: "''' + level.at[i, 'idPropertyName_x'] + '''", title: "''' + y + '''", value: 1, to: "''' + level.at[i, 'valueProperty'] + '''"}'''


    # ------------------------------------------------------ XY --------------------------------------------------------------
    else:
        # Añadimos las aristas para unir la propiedad con ambos miembros
        xy = level.at[i, 'ID_'+XY]
        buscadoXY = 'from: "Members'+XY.upper()+'", label: "' + level.at[i, 'idPropertyName_x'] +'", title: ".*", value: ., to: "' + level.at[i, 'valueProperty'] + '"'


        # Buscamos todas las apariciones de buscadoXY, con lo que obtenemos la arista exacta (si la hay)
        encontradoXY = re.findall(buscadoXY, subEdges) # NOTA: Esto es una lista (que debería tener uno o cero elementos)

        # Si ya existe esa arista, la estudiamos para editarla (si es necesario)
        if encontradoXY:

            index = subEdges.find(encontradoXY[0]) # La posición de la arista X
            splited = buscadoXY.split('.*') # Partimos nuestra búsqueda para tener la primera parte de la cadena, es decir, todo hasta llegar al título

            # Si el miembro X no está en el título de la arista, lo añadimos y aumentamos el valor
            # NOTA: Esta comprobación funciona porque el dataframe está ordenado. Si se cambia el orden, habría
            #       que modificar esta parte
            if (xy not in subEdges[(index + len(splited[0])):]):

                # Limpiamos el string de la arista para obtener el valor antiguo
                auxiliar = re.sub('from: "Members'+XY.upper()+'", label: "' + level.at[i, 'idPropertyName_x'] +
                    '", title: ".*", value: ', '', encontradoXY[0])

                value = re.sub(', to: "' + level.at[i, 'valueProperty'] + '"', '', auxiliar)

                # Actualizamos el valor
                incremento = int(value) + 1
                nuevaArista = encontradoXY[0].replace(value,str(incremento), 1)
                subEdges = re.sub(encontradoXY[0], nuevaArista, subEdges)    
                
                # Añadimos el nombre del miembro X al título de la arista
                subEdges = subEdges[:(index + len(splited[0]))] + xy + ', ' + subEdges[(index + len(splited[0])):]
        

        # Si no existe la arista de los miembros X a la propiedad, añadimos las dos aristas que forman la explicación
        else:

          subEdges += ''',
        {from: "Members'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName_x'] + '''", title: "''' + xy + '''", value: 1, to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]




# Switch que devuelve el nombre de la función a la que corresponde cada número 
switcher = {
        1: song,
        2: artist,
        3: genre,
        4: member
    }

def cleanSong(song):
    cleanSong = song.split(' — ')

    return cleanSong