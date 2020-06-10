
// Recorremos todos los nodos
nodes.forEach(funcion1);
nodes2.forEach(funcion1);

function funcion1(value) {
    // Comprobamos que sea un nodo central
    if (value["group"] == "center") {
        var idNodo1 = value["id"];
        var labelNodo1 = value["label"];

        var nodosConectados1 = network.getConnectedNodes(idNodo1).sort();

        auxNodes = nodes.get();

        // Volvemos a recorrer todos los nodos para compararlos
        for (var i = 0, len = auxNodes.length; i < len; i++) {
            labelNodo1 = funcion2(auxNodes[i], idNodo1, labelNodo1, nodosConectados1);
        }
    }
}

function funcion2(value, idNodo1, labelNodo1, nodosConectados1) {

    // Comprobamos que sea un nodo central
    if (value["group"] == "center") {
        var idNodo2 = value["id"];
        var labelNodo2 = value["label"];

        // Nos aseguramos de que no sean el mismo nodo
        if (idNodo1 != idNodo2) {

            var nodosConectados2 = network.getConnectedNodes(idNodo2).sort();

            // Comparamos el número de nodos conectados para ahorrar tiempo
            if (nodosConectados1.length == nodosConectados2.length) {
                // Comprobamos que estén conectados a los mismos nodos
                if (JSON.stringify(nodosConectados1) == JSON.stringify(nodosConectados2)) {
                    var aristasConectadas1 = network.getConnectedEdges(idNodo1).sort();
                    var aristasConectadas2 = network.getConnectedEdges(idNodo2).sort();

                    if (aristasConectadas1.length == aristasConectadas2.length) {
                        var conectadas1 = aristasConectadas1.map(fromLabel).sort();
                        var conectadas2 = aristasConectadas2.map(fromLabel).sort();

                        if (JSON.stringify(conectadas1) == JSON.stringify(conectadas2)) {
                            
                            nodes.update({
                                id: idNodo1,
                                label: labelNodo1 + "\n — \n" + labelNodo2
                            });

                            aristasConectadas2.forEach(borraArista);
                            nodes.remove(idNodo2);

                            return labelNodo1 + "\n — \n" + labelNodo2;
                        }
                    }

                }
            }
        }
    }

    return labelNodo1;
}

function fromLabel(value) {
    var arista = edges.get(value);

    return arista["from"] + arista["label"];
}

function borraArista(value) {
    edges.remove(value);
}