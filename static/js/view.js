function toggleGraph1() {
  var x = document.getElementById("mynetwork");

  if (x.classList.contains("hide")) {
    $("#mynetwork2").toggleClass("hide");
    $("#mynetwork").toggleClass("hide");
  }
}

function toggleGraph2() {
  var x = document.getElementById("mynetwork2");

  if (x.classList.contains("hide")) {
    $("#mynetwork").toggleClass("hide");
    $("#mynetwork2").toggleClass("hide");
  }
}

// Función para eliminar duplicados de un array
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
function loadSongs(data) {
  loadSong(data, 'mySelect1');
  loadSong(data, 'mySelect2');
}

// En esta función se cargan las canciones del dataset en una de las listas del html
function loadSong(data, select) {

  //split and get the rows in an array
  var splited = data.split('\n');
  splited.shift();
  var aux = uniq(splited);
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
function myFunction(input, select) {
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