// Recorremos todos los nodos y llamamos a funcion1 por cada uno de ellos
nodos = nodes.get();
for (var i = 0, len = nodos.length; i < len; i++) {
    funcion1(nodos[i], "");
}
// Hacemos lo mismo con nodes2
nodos2 = nodes2.get();
for (var i = 0, len = nodos2.length; i < len; i++) {
    funcion1(nodos2[i], "2");
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