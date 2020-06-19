// Función para alternar entre la vista de ambos grafos
// RECIBE: String param  => id de la network a mostrar,
//         String param2 => id de la network a ocultar
function toggleGraph(param, param2) {
  var x = document.getElementById(param);
  var y = "#".concat("", param);
  var z = "#".concat("", param2);

  // Solo hace el cambio si el elemento está oculto
  if (x.classList.contains("hide")) {
    $(z).toggleClass("hide");
    $(y).toggleClass("hide");
  }
}

// Función para eliminar duplicados de un array
// RECIBE:   Array a => array que se quiere limpiar
// DEVUELVE: array sin elementos repetidos
function uniq(a) {
  var seen = {};
  return a.filter(function(item) {
      return seen.hasOwnProperty(item) ? false : (seen[item] = true);
  });
}

// Al cargar la página obtenemos los datos del Dataset
$(document).ready(function() {
  $.ajax({
    type: "GET",
    url: "/static/cleanDataset.csv",
    dataType: "text"
  }).done(loadSongs);
});

// Cargamos las dos listas de canciones
// RECIBE: texto data => datos del archivo .csv
function loadSongs(data) {
  loadSong(data, 'mySelect1');
  loadSong(data, 'mySelect2');
}

// En esta función se cargan las canciones del dataset en una de las listas del html
// RECIBE: texto data => datos del archivo .csv,
//         String select => id del elemento select de la vista
function loadSong(data, select) {

  //split and get the rows in an array
  var splited = data.split('\n');
  splited.shift();
  var aux = uniq(splited); // Eliminamos repeticiones del array
  var rows = aux.sort();

  //move line by line
  for (var i = 0; i < rows.length; i++) {

    //the value of the current row
    var val = rows[i];

    // get reference to select element
    var sel = document.getElementById(select);

    // create new option element
    var opt = document.createElement('option');

    // create text node to add to option element (opt)
    opt.appendChild( document.createTextNode(val) );

    // add opt to end of select box (sel)
    sel.appendChild(opt);

  }
} 

// Función para filtrar las listas en función de lo que escribe el usuario
// RECIBE: String input  => id del elemento desde el que se realiza la búsqueda,
//         String select => id de la lista a filtrar
function myFilter(input, select) {
    var myInput, filter, ul, li, a, i, txtValue;

    myInput = document.getElementById(input);
    filter = myInput.value.toUpperCase();

    ul = document.getElementById(select);
    li = ul.getElementsByTagName("option");

    for (i = 0; i < li.length; i++) {

        txtValue = ul.getElementsByTagName("option")[i].innerHTML;

        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

// Se comprueba que se hayan seleccionado dos canciones distintas y se avisa en caso contrario
document.getElementById("myForm").onsubmit = function() {
  var f = document.getElementById("mySelect1");
  var g = document.getElementById("mySelect2");
  
  if (f.value == g.value) {
    alert("Has seleccionado dos veces la misma canción. Prueba a compararla con otra de la lista.");
    return false;
  }
  else {
    return true;
  }
};