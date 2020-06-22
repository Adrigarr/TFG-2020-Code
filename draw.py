import re

# ----------------------------    FUNCIONES PARA DIBUJAR EL GRAFO --------------------------

def song(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = auxEdges

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambas canciones
    subEdges += ''',
    {from: "''' + level.at[i, 'ID_x'] + '''SX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''SY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def genre(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = auxEdges

    # Añadimos el nodo del género X si es necesario, además de una arista para unirlo a la primera canción
    if ((level.at[i, 'ID_x'] + 'GX') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'ID_x'] + ''' ", title: "Genre", group: "genre", level: 3}'''

        subEdges += ''',
    {from: "''' + songX + '''SX", label: "genre", to: "''' + level.at[i, 'ID_x'] + '''GX"}'''

    # Añadimos el nodo del género Y si es necesario, además de una arista para unirlo a la segunda canción
    if ((level.at[i, 'ID_y'] + 'GY') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'ID_y'] + ''' ", title: "Genre", group: "genre", level: 5}'''

        subEdges += ''',
    {from: "''' + songY + '''SY", label: "genre", to: "''' + level.at[i, 'ID_y'] + '''GY"}'''

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambos géneros
    subEdges += ''',
    {from: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def artist(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = auxEdges

    nodoArtistas = '''{id: "artists", label: ".*", group: "artist", level: 4}'''

    if (re.findall(nodoArtistas, auxNodes) and ((level.at[i, 'ID_x'] in re.findall(nodoArtistas, auxNodes)[0]) or (level.at[i, 'ID_y'] in re.findall(nodoArtistas, auxNodes)[0]))):
        return [subNodes, subEdges]

    # Añadimos el nodo del artista X si es necesario, además de una arista para unirlo a la primera canción
    if ((level.at[i, 'ID_x'] + 'AX') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'ID_x'] + '''AX", label: "''' + level.at[i, 'ID_x'] + ''' ", title: "Artist", group: "artist", level: 2}'''

        subEdges += ''',
    {from: "''' + songX + '''SX", label: "artist", to: "''' + level.at[i, 'ID_x'] + '''AX"}'''

    # Añadimos el nodo del artista Y si es necesario, además de una arista para unirlo a la segunda canción
    if ((level.at[i, 'ID_y'] + 'AY') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'ID_y'] + '''AY", label: "''' + level.at[i, 'ID_y'] + ''' ", title: "Artist", group: "artist", level: 6}'''

        subEdges += ''',
    {from: "''' + songY + '''SY", label: "artist", to: "''' + level.at[i, 'ID_y'] + '''AY"}'''


    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambos artistas
    subEdges += ''',
    {from: "''' + level.at[i, 'ID_x'] + '''AX", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "''' + level.at[i, 'ID_y'] + '''AY", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def member(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY):
    subNodes = ''
    subEdges = auxEdges

    # Añadimos el nodo del miembro X si es necesario, además de una arista para unirlo al primer artista
    if ('MembersX' not in auxNodes):
        subNodes = ''',
    {id: "MembersX", label: "Members of ''' + artistX + '''", title: "Members", group: "member", level: 3}'''
        subEdges += ''',
    {from: "''' + artistX + '''AX", label: "miembros", to: "MembersX"}'''


    # Añadimos el nodo del miembro Y si es necesario, además de una arista para unirlo al segundo artista
    if ('MembersY' not in auxNodes):
        subNodes += ''',
    {id: "MembersY", label: "Members of ''' + artistY + '''", title: "Members", group: "member", level: 5}'''
        subEdges += ''',
    {from: "''' + artistY + '''AY", label: "miembros", to: "MembersY"}'''

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''



    # Añadimos las aristas para unir la propiedad con ambos miembros
    x = level.at[i, 'ID_x']
    y = level.at[i, 'ID_y']
    buscadoX = 'from: "MembersX", label: "' + level.at[i, 'idPropertyName'] +'", title: ".*", value: ., to: "' + level.at[i, 'valueProperty'] + '"'
    buscadoY = 'from: "MembersY", label: "' + level.at[i, 'idPropertyName'] +'", title: ".*", value: ., to: "' + level.at[i, 'valueProperty'] + '"'


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
            auxiliar = re.sub('from: "MembersX", label: "' + level.at[i, 'idPropertyName'] +
                '", title: ".*", value: ', '', encontradoX[0])

            value = re.sub(', to: "' + level.at[i, 'valueProperty'] + '"', '', auxiliar)

            # Actualizamos el valor
            incremento = int(value) + 1
            nuevaArista = encontradoX[0].replace(value,str(incremento))
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
            auxiliar = re.sub('from: "MembersY", label: "' + level.at[i, 'idPropertyName'] +
                '", title: ".*", value: ','',encontradoY[0])

            value = re.sub(', to: "' + level.at[i, 'valueProperty'] + '"', '', auxiliar)

            # Actualizamos el valor
            incremento = int(value) + 1
            nuevaArista = encontradoY[0].replace(value,str(incremento))
            subEdges = re.sub(encontradoY[0], nuevaArista, subEdges)

            # Añadimos el nombre del miembro X al título de la arista
            subEdges = subEdges[:(index + len(splited[0]))] + y + ', ' + subEdges[(index + len(splited[0])):]
    

    # Si no existe la arista de los miembros X a la propiedad, añadimos las dos aristas que forman la explicación
    else:

      subEdges += ''',
    {from: "MembersX", label: "''' + level.at[i, 'idPropertyName'] + '''", title: "''' + x + '''", value: 1, to: "''' + level.at[i, 'valueProperty'] + '''"},
    {from: "MembersY", label: "''' + level.at[i, 'idPropertyName'] + '''", title: "''' + y + '''", value: 1, to: "''' + level.at[i, 'valueProperty'] + '''"}'''


    return [subNodes, subEdges]

def song2(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambas canciones
    subEdges += ''',
    {from: "''' + level.at[i, 'ID_'+XY] + '''S'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def genre2(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    if (XY == 'x'):
        # Añadimos el nodo del género si es necesario, además de una arista para unirlo a la canción correspondiente
        if ((level.at[i, 'ID_x'] + 'GX') not in auxNodes):
            subNodes = ''',
    {id: "''' + level.at[i, 'ID_x'] + '''GX", label: "''' + level.at[i, 'ID_x'] + ''' ", title: "Genre", group: "genre", level: 3}'''

        if (('''{from: "''' + songX + '''SX", label: "genre", to: "''' + level.at[i, 'ID_x'] + '''GX"}''') not in subEdges):
            subEdges += ''',
    {from: "''' + songX + '''SX", label: "genre", to: "''' + level.at[i, 'ID_x'] + '''GX"}'''

    else:
        # Añadimos el nodo del género si es necesario, además de una arista para unirlo a la canción correspondiente
        if ((level.at[i, 'ID_y'] + 'GY') not in auxNodes):
            subNodes = ''',
    {id: "''' + level.at[i, 'ID_y'] + '''GY", label: "''' + level.at[i, 'ID_y'] + ''' ", title: "Genre", group: "genre", level: 5}'''

        if (('''{from: "''' + songY + '''SY", label: "genre", to: "''' + level.at[i, 'ID_y'] + '''GY"}''') not in subEdges):
            subEdges += ''',
    {from: "''' + songY + '''SY", label: "genre", to: "''' + level.at[i, 'ID_y'] + '''GY"}'''

    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # Añadimos la arista para unir la propiedad con el género
    if (('''{from: "''' + level.at[i, 'ID_'+XY] + '''G'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}''') not in subEdges):
        subEdges += ''',
    {from: "''' + level.at[i, 'ID_'+XY] + '''G'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def artist2(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    nodoArtistas = '''{id: "artists", label: ".*", title: "Artist", group: "artist", level: 4}'''

    if (re.findall(nodoArtistas, auxNodes) and ((level.at[i, 'ID_x'] in re.findall(nodoArtistas, auxNodes)[0]) or (level.at[i, 'ID_y'] in re.findall(nodoArtistas, auxNodes)[0]))):
        return [subNodes, subEdges]

    if (XY == 'x'):
        # Añadimos el nodo del artista X si es necesario, además de una arista para unirlo a la primera canción
        if ((level.at[i, 'ID_x'] + 'AX') not in auxNodes):
            subNodes = ''',
    {id: "''' + level.at[i, 'ID_x'] + '''AX", label: "''' + level.at[i, 'ID_x'] + ''' ", title: "Artist", group: "artist", level: 2}'''

        if (('''{from: "''' + songX + '''SX", label: "artist", to: "''' + level.at[i, 'ID_x'] + '''AX"}''') not in subEdges):
            subEdges += ''',
    {from: "''' + songX + '''SX", label: "artist", to: "''' + level.at[i, 'ID_x'] + '''AX"}'''

    else:
        # Añadimos el nodo del artista X si es necesario, además de una arista para unirlo a la primera canción
        if ((level.at[i, 'ID_y'] + 'AY') not in auxNodes):
            subNodes = ''',
    {id: "''' + level.at[i, 'ID_y'] + '''AY", label: "''' + level.at[i, 'ID_y'] + ''' ", title: "Artist", group: "artist", level: 6}'''

        if (('''{from: "''' + songY + '''SY", label: "artist", to: "''' + level.at[i, 'ID_y'] + '''AY"}''') not in subEdges):
            subEdges += ''',
    {from: "''' + songY + '''SY", label: "artist", to: "''' + level.at[i, 'ID_y'] + '''AY"}'''


    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''

    # Añadimos las aristas para unir la propiedad con ambos artistas
    if (('''{from: "''' + level.at[i, 'ID_'+XY] + '''A'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}''') not in subEdges):
        subEdges += ''',
    {from: "''' + level.at[i, 'ID_'+XY] + '''A'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName'] + '''", to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]

def member2(level, i, auxNodes, auxEdges, songX, songY, artistX, artistY, XY):
    subNodes = ''
    subEdges = auxEdges

    if (XY == 'x'):
        # Añadimos el nodo del miembro X si es necesario, además de una arista para unirlo al primer artista
        if ('MembersX' not in auxNodes):
            subNodes = ''',
    {id: "MembersX", label: "Members of ''' + artistX + '''", title: "Members", group: "member", level: 3}'''
            subEdges += ''',
    {from: "''' + artistX + '''AX", label: "miembros", to: "MembersX"}'''

    else:
        # Añadimos el nodo del miembro Y si es necesario, además de una arista para unirlo al segundo artista
        if ('MembersY' not in auxNodes):
            subNodes += ''',
    {id: "MembersY", label: "Members of ''' + artistY + '''", title: "Members", group: "member", level: 5}'''
            subEdges += ''',
    {from: "''' + artistY + '''AY", label: "miembros", to: "MembersY"}'''


    # Añadimos el nodo de la propiedad si es necesario
    if (('id: "'+level.at[i, 'valueProperty']+'",') not in auxNodes):
        subNodes = subNodes + ''',
    {id: "''' + level.at[i, 'valueProperty'] + '''", label: "''' + level.at[i, 'valueProperty'] + '''", group: "center", level: 4}'''


    # Añadimos las aristas para unir la propiedad con ambos miembros
    xy = level.at[i, 'ID_'+XY]
    buscadoXY = 'from: "Members'+XY.upper()+'", label: "' + level.at[i, 'idPropertyName'] +'", title: ".*", value: ., to: "' + level.at[i, 'valueProperty'] + '"'


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
            auxiliar = re.sub('from: "Members'+XY.upper()+'", label: "' + level.at[i, 'idPropertyName'] +
                '", title: ".*", value: ', '', encontradoXY[0])

            value = re.sub(', to: "' + level.at[i, 'valueProperty'] + '"', '', auxiliar)

            # Actualizamos el valor
            incremento = int(value) + 1
            nuevaArista = encontradoXY[0].replace(value,str(incremento))
            subEdges = re.sub(encontradoXY[0], nuevaArista, subEdges)    
            
            # Añadimos el nombre del miembro X al título de la arista
            subEdges = subEdges[:(index + len(splited[0]))] + xy + ', ' + subEdges[(index + len(splited[0])):]
    

    # Si no existe la arista de los miembros X a la propiedad, añadimos las dos aristas que forman la explicación
    else:

      subEdges += ''',
    {from: "Members'''+XY.upper()+'''", label: "''' + level.at[i, 'idPropertyName'] + '''", title: "''' + xy + '''", value: 1, to: "''' + level.at[i, 'valueProperty'] + '''"}'''

    return [subNodes, subEdges]
    
 
switcher = {
        2: song,
        3: genre,
        4: artist,
        5: member
    }

switcher2 = {
        2: song2,
        3: genre2,
        4: artist2,
        5: member2
    }

def cleanSong(song):
    cleanSong = song.split(' — ')

    return cleanSong