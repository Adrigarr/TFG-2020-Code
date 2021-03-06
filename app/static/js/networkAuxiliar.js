// Recorremos todos los nodos y llamamos a funcion1 por cada uno de ellos
var nodos = nodes.get();

// Eliminamos aquellos nodos correspondientes a la relación "instance of" a menos que sean "single"
var nodosCentrales = nodos.filter(nodo => nodo.level == 4);
nodosCentrales.forEach(single);

// Evitamos que se superpongan las aristas
for (var i = 0, len = nodosCentrales.length; i < len; i++) {
    dobles(nodosCentrales[i], "1");
}

// Actualizamos nuestra variable nodos
nodos = nodes.get();

for (var i = 0, len = nodos.length; i < len; i++) {
    funcion1(nodos[i], "");  
}


// Eliminamos del segundo grafo posibles nodos que no conectan con ambas canciones
var nodos2 = nodes2.get();
var nodosCentrales2 = nodos2.filter(nodo => nodo.level == 4);
var nodosIntermedios2 = nodos2.filter(nodo => ((nodo.level > 1) && (nodo.level < 7) && (nodo.level != 4)));

nodosCentrales2.forEach(nodoInnecesario);
nodosIntermedios2.forEach(nodoInnecesario);

// Evitamos que se superpongan las aristas
for (var i = 0, len = nodosCentrales2.length; i < len; i++) {
    dobles(nodosCentrales2[i], "2");
}

// Actualizamos nuestra variable nodos2
nodos2 = nodes2.get();

// Recorremos todos los nodos de nodes2 y llamamos a funcion1 por cada uno de ellos
for (var i = 0, len = nodos2.length; i < len; i++) {
    funcion1(nodos2[i], "2");
}



// Función que, dado un nodo del primer grafo, comprueba si es producto de una relación "instance of" y si es un single
// RECIBE: object value => nodo estudiado
function single(value) {
    var aristasConectadas = network.getConnectedEdges(value["id"]); // Aristas conectadas al nodo
    var arista = edges.get(aristasConectadas[0]); // Obtenemos el objeto correspondiente a la primera arista conectada al nodo

    // Si el nodo es una explicación "instance of" pero su valor (id) es distinto a "single", lo borramos junto a sus aristas
    if (arista["label"] == "instance of" && value["id"] != "single") {

        for (var i = 0, len = aristasConectadas.length; i < len; i++) {
            borraArista(aristasConectadas[i], edges);
        }
        nodes.remove(value["id"]);
    }
    
}

// Función que comprueba si un nodo tiene 2 aristas que conecten a un mismo nodo.
// En caso afirmativo, cambia la forma de esas aristas por una curva
// RECIBE: object value       => nodo estudiado
//         String alternative => indica en qué grafo estamos trabajando
function dobles(value, alternative) {
    if (alternative == "1") {
        var net = network;
        var edg = edges;
    }

    else {
        var net = network2;
        var edg = edges2;
    }

    var aristasConectadas = net.getConnectedEdges(value["id"]); // Aristas conectadas al nodo
    var vistos = {};

    for (var i = 0, len = aristasConectadas.length; i < len; i++) {
        var aristaI = edg.get(aristasConectadas[i]);

        if (Object.keys(vistos).includes(aristaI["from"])) {
            edg.update({
                id: aristaI["id"],
                smooth: {
                    enabled: true,
                    type: "curvedCW",
                    roundness: 0.1
                }    
            });

            edg.update({
                id: vistos[aristaI["from"]]["id"],
                smooth: {
                    enabled: true,
                    type: "curvedCCW",
                    roundness: 0.1
                }
            });
        }

        else {
            vistos[aristaI["from"]] = aristaI;
        }
    }
}


// Esta función comprueba si un nodo es innecesario y lo borra en ese caso
// RECIBE: object value => nodo estudiado
function nodoInnecesario(value) {
    var nodosConectados = network2.getConnectedNodes(value["id"]);

    // Si el nodo actual conecta con menos de 2 nodos, significa que está "suelto", así que es innecesario
    // También es innecesario si solo está conectado a dos nodos del mismo grupo o categoría, porque en
    // ese caso corresponde a un nodo del primer grafo, no del segundo
    if ((nodosConectados.length < 2) || ((nodosConectados.length == 2) && (nodes2.get(nodosConectados[0])["group"] == nodes2.get(nodosConectados[1])["group"]))) {
        var aristasConectadas = network2.getConnectedEdges(value["id"]);

        // Borramos todas sus aristas
        for (var i = 0, len = aristasConectadas.length; i < len; i++) {
            borraArista(aristasConectadas[i], edges2);
        }
        // Borramos el nodo innecesario
        nodes2.remove(value["id"]);
    }
}

// RECIBE: object value => nodo estudiado,
//         String array => indica qué array de nodos estamos estudiando
function funcion1(value, array) {
    // Comprobamos que sea un nodo central
    if (value["group"] == "center") {
        var idNodo1 = value["id"];
        var labelNodo1 = value["label"];

        if (array == "") {
            var net = network;
            var nod = nodes;
        }
        else {
            var net = network2;
            var nod = nodes2;
        }

        var nodosConectados1 = net.getConnectedNodes(idNodo1).sort();

        auxNodes = nod.get();

        // Volvemos a recorrer todos los nodos para compararlos
        for (var i = 0, len = auxNodes.length; i < len; i++) {
            labelNodo1 = funcion2(auxNodes[i], idNodo1, labelNodo1, nodosConectados1, array);
        }
    }
}

// RECIBE: object value           => nodo a comparar con el de funcion1(),
//         String idNodo1         => id del nodo de la funcion1(),
//         String labelNodo1      => label del nodo de la funcion1(),
//         array nodosConectados1 => lista de nodos conectados al de la funcion1(),
//         String array => indica qué array de nodos estamos estudiando
// DEVUELVE: String que contiene la nueva label del nodo estudiado en funcion1()
function funcion2(value, idNodo1, labelNodo1, nodosConectados1, array) {

    // Comprobamos que sea un nodo central
    if (value["group"] == "center") {
        var idNodo2 = value["id"];
        var labelNodo2 = value["label"];

        // Nos aseguramos de que no sean el mismo nodo
        if (idNodo1 != idNodo2) {

            if (array == "") {
                var net = network;
                var nod = nodes;
                var edg = edges;
            }
            else {
                var net = network2;
                var nod = nodes2;
                var edg = edges2;
            }

            var nodosConectados2 = net.getConnectedNodes(idNodo2).sort();

            // Comparamos el número de nodos conectados para ahorrar tiempo
            if (nodosConectados1.length == nodosConectados2.length) {
                // Comprobamos que estén conectados a los mismos nodos
                if (JSON.stringify(nodosConectados1) == JSON.stringify(nodosConectados2)) {
                    var aristasConectadas1 = net.getConnectedEdges(idNodo1).sort();
                    var aristasConectadas2 = net.getConnectedEdges(idNodo2).sort();

                    // Comprobamos que estén conectados a las mismos aristas
                    if (aristasConectadas1.length == aristasConectadas2.length) {
                        var conectadas1 = [];
                        var conectadas2 = [];

                        for (var i = 0, len = aristasConectadas1.length; i < len; i++) {
                            conectadas1[i] = fromLabel(aristasConectadas1[i], edg);
                        }
                        for (var i = 0, len = aristasConectadas2.length; i < len; i++) {
                            conectadas2[i] = fromLabel(aristasConectadas2[i], edg);
                        }

                        // Si están conectados a los mismos nodos y aristas, fusionamos ambos nodos
                        if (JSON.stringify(conectadas1.sort()) == JSON.stringify(conectadas2.sort())) {
                            
                            nod.update({
                                id: idNodo1,
                                label: labelNodo1 + "\n — \n" + labelNodo2
                            });
                            
                            for (var i = 0, len = aristasConectadas2.length; i < len; i++) {
                                borraArista(aristasConectadas2[i], edg);
                            }
                            nod.remove(idNodo2);

                            return labelNodo1 + "\n — \n" + labelNodo2;
                        }
                    }

                }
            }
        }
    }

    return labelNodo1;
}

// Función que, dada una arista, devuelve un objeto con su información básica
// RECIBE:   object value => arista a estudiar,
//           object edg   => objeto aristas estudiado
// DEVUELVE: object con la información esencial de la arista (from y label)
function fromLabel(value, edg) {
    var arista = edg.get(value);

    return arista["from"] + arista["label"] + arista["title"];
}

// Función que borra una arista
// RECIBE: object value => arista a eliminar,
//         object edg   => objeto aristas estudiado
function borraArista(value, edg) {
    edg.remove(value);
}



// Cuando se hace click en el primer grafo, se llama a la función
// para mostrar la tabla de datos adicionales
network.on("click", function(params) {
  showTable(params);
});

// Cuando se hace click en el segundo grafo, se llama a la función
// para mostrar la tabla de datos adicionales
network2.on("click", function(params) {
  showTable(params);
});


// Función para mostrar la tabla de datos adicionales en el caso de los nodos de canciones o artistas
// RECIBE: objeto params => objeto con la información del evento
function showTable(params) {
    params.event = "[original event]";

    // Comprobamos si se ha hecho click en (al menos) un nodo
    if (params.nodes.length > 0) {

        // Recortamos los dos últimos caracteres de la ID del nodo para obtener
        // el nombre de nuestro objeto de estudio
        var name = params.nodes[0].slice(0, -2);

        // Se busca un archivo .json con el nombre del objeto de estudio
        // y, si se encuentra, se muestra su contenido en una tabla
        $.getJSON('/app/static/' + name.replace('/', ' ') + '.json')
            .done(function (data) {

                var len = Object.keys(data.ID).length;
                var table = document.getElementById("mytable");

                // Se limpia la tabla para evitar datos residuales
                table.innerHTML = '';

                // Se añade la fila de cabecera
                addRow(table, data.ID[0], "", 'y');
                table.appendChild(document.createElement('tbody'));

                // Se van añadiendo filas a la tabla con todos los datos disponibles
                for (i = 0; i < len; i++) {
                    var lastRowCells = table.rows[table.rows.length-1].cells;

                    // Si se trata de una propiedad que ya está en la tabla, su valor se amplía
                    if (data.idPropertyName[i] == lastRowCells[0].innerHTML) {
                        lastRowCells[1].innerHTML += ", " + data.valueProperty[i];
                    }
                    // Si no, se añade una fila nueva
                    else {
                        addRow(table, data.idPropertyName[i], data.valueProperty[i], 'n');
                    }
                }

            })
    }
}


// Función para añadir una fila de dos celdas a una tabla HTML
// RECIBE: tabla table  => tabla a modificar,
//         String data1 => datos a introducir en la primera celda,
//         String data2 => datos a introducir en la segunda celda
function addRow(table, data1, data2, isHeader) {
    if (isHeader == 'y') {
        var header = table.createTHead();
        var row = header.insertRow(-1); // Se añade una fila a la cabecera de la tabla
        var cell1 = row.insertCell(0); // Se añade una celda a la fila
        var cell2 = row.insertCell(1); // Se añade otra celda a la fila
        cell1.outerHTML = "<th>" + data1 +"</th>";  // Se rellena la primera celda
        cell2.outerHTML = "<th>" + data2 +"</th>";  // Se rellena la segunda celda
    }
    else {

        var row = table.tBodies[0].insertRow(-1); // Se añade una fila al final de la tabla
        var cell1 = row.insertCell(0); // Se añade una celda a la fila
        var cell2 = row.insertCell(1); // Se añade otra celda a la fila
        cell1.innerHTML = data1; // Se rellena la primera celda
        cell2.innerHTML = data2; // Se rellena la segunda celda
    }

    
};