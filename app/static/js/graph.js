// create an array with nodes
var nodes = new vis.DataSet([
    {id: "(I Can't Get No) SatisfactionSX", label: "(I Can't Get No) Satisfaction", title: "Song", group: "song", level: 1},
    {id: "Hey JudeSY", label: "Hey Jude", title: "Song", group: "song", level: 7},
    {id: "English", label: "English", group: "center", level: 4},
    {id: "rock musicGX", label: "rock music ", title: "Genre", group: "genre", level: 3},
    {id: "pop rockGY", label: "pop rock ", title: "Genre", group: "genre", level: 5},
    {id: "United States of America", label: "United States of America", group: "center", level: 4},
    {id: "The BeatlesAY", label: "The Beatles ", title: "Artist", group: "artist", level: 6},
    {id: "Grammy Award for Best Music Video", label: "Grammy Award for Best Music Video", group: "center", level: 4},
    {id: "The Rolling StonesAX", label: "The Rolling Stones ", title: "Artist", group: "artist", level: 2},
    {id: "Grammy Lifetime Achievement Award", label: "Grammy Lifetime Achievement Award", group: "center", level: 4},
    {id: "Rock and Roll Hall of Fame", label: "Rock and Roll Hall of Fame", group: "center", level: 4},
    {id: "United Kingdom", label: "United Kingdom", group: "center", level: 4},
    {id: "blues rock", label: "blues rock", group: "center", level: 4},
    {id: "hard rock", label: "hard rock", group: "center", level: 4},
    {id: "psychedelic rock", label: "psychedelic rock", group: "center", level: 4},
    {id: "rock and roll", label: "rock and roll", group: "center", level: 4},
    {id: "rock music", label: "rock music", group: "center", level: 4},
    {id: "Chuck Berry", label: "Chuck Berry", group: "center", level: 4},
    {id: "Polydor Records", label: "Polydor Records", group: "center", level: 4},
    {id: "MembersX", label: "Members of The Rolling Stones", title: "Members", group: "member", level: 3},
    {id: "MembersY", label: "Members of The Beatles", title: "Members", group: "member", level: 5},
    {id: "baritone", label: "baritone", group: "center", level: 4}
]);
var nodes2 = new vis.DataSet([
    {id: "(I Can't Get No) SatisfactionSX", label: "(I Can't Get No) Satisfaction", title: "Song", group: "song", level: 1},
    {id: "Hey JudeSY", label: "Hey Jude", title: "Song", group: "song", level: 7},
    {id: "rock music", label: "rock music", group: "center", level: 4},
    {id: "The BeatlesAY", label: "The Beatles ", title: "Artist", group: "artist", level: 6},
    {id: "The Rolling StonesAX", label: "The Rolling Stones ", title: "Artist", group: "artist", level: 2},
    {id: "United Kingdom", label: "United Kingdom", group: "center", level: 4},
    {id: "pop rockGY", label: "pop rock ", title: "Genre", group: "genre", level: 5},
    {id: "MembersY", label: "Members of The Beatles", title: "Members", group: "member", level: 5},
    {id: "blues rock", label: "blues rock", group: "center", level: 4},
    {id: "hard rock", label: "hard rock", group: "center", level: 4},
    {id: "psychedelic rock", label: "psychedelic rock", group: "center", level: 4},
    {id: "rock and roll", label: "rock and roll", group: "center", level: 4},
    {id: "MembersX", label: "Members of The Rolling Stones", title: "Members", group: "member", level: 3}
]);

// create an array with edges
var edges = new vis.DataSet([
    {},
    {from: "(I Can't Get No) SatisfactionSX", label: "language", to: "English"},
    {from: "Hey JudeSY", label: "language", to: "English"},
    {from: "(I Can't Get No) SatisfactionSX", label: "genre", to: "rock musicGX"},
    {from: "rock musicGX", label: "country", to: "United States of America"},
    {from: "Hey JudeSY", label: "genre", to: "pop rockGY"},
    {from: "pop rockGY", label: "country", to: "United States of America"},
    {from: "(I Can't Get No) SatisfactionSX", label: "artist", to: "The Rolling StonesAX"},
    {from: "The Rolling StonesAX", label: "award received", to: "Grammy Award for Best Music Video"},
    {from: "Hey JudeSY", label: "artist", to: "The BeatlesAY"},
    {from: "The BeatlesAY", label: "award received", to: "Grammy Award for Best Music Video"},
    {from: "The Rolling StonesAX", label: "award received", to: "Grammy Lifetime Achievement Award"},
    {from: "The BeatlesAY", label: "award received", to: "Grammy Lifetime Achievement Award"},
    {from: "The Rolling StonesAX", label: "award received", to: "Rock and Roll Hall of Fame"},
    {from: "The BeatlesAY", label: "award received", to: "Rock and Roll Hall of Fame"},
    {from: "The Rolling StonesAX", label: "country", to: "United Kingdom"},
    {from: "The BeatlesAY", label: "country", to: "United Kingdom"},
    {from: "The Rolling StonesAX", label: "genre", to: "blues rock"},
    {from: "The BeatlesAY", label: "genre", to: "blues rock"},
    {from: "The Rolling StonesAX", label: "genre", to: "hard rock"},
    {from: "The BeatlesAY", label: "genre", to: "hard rock"},
    {from: "The Rolling StonesAX", label: "genre", to: "psychedelic rock"},
    {from: "The BeatlesAY", label: "genre", to: "psychedelic rock"},
    {from: "The Rolling StonesAX", label: "genre", to: "rock and roll"},
    {from: "The BeatlesAY", label: "genre", to: "rock and roll"},
    {from: "The Rolling StonesAX", label: "genre", to: "rock music"},
    {from: "The BeatlesAY", label: "genre", to: "rock music"},
    {from: "The Rolling StonesAX", label: "influenced by", to: "Chuck Berry"},
    {from: "The BeatlesAY", label: "influenced by", to: "Chuck Berry"},
    {from: "The Rolling StonesAX", label: "record label", to: "Polydor Records"},
    {from: "The BeatlesAY", label: "record label", to: "Polydor Records"},
    {from: "The Rolling StonesAX", label: "miembros", to: "MembersX"},
    {from: "The BeatlesAY", label: "miembros", to: "MembersY"},
        {from: "MembersX", label: "Voice Type", title: "Mick Jagger", value: 1, to: "baritone"},
        {from: "MembersY", label: "Voice Type", title: "Ringo Starr, John Lennon", value: 2, to: "baritone"},
        {from: "MembersX", label: "genre", title: "Mick Taylor, Bill Wyman, Charlie Watts, Brian Jones, Keith Richards", value: 5, to: "blues rock"},
        {from: "MembersY", label: "genre", title: "John Lennon", value: 1, to: "blues rock"},
        {from: "MembersX", label: "genre", title: "Mick Taylor, Charlie Watts, Ronnie Wood", value: 3, to: "hard rock"},
        {from: "MembersY", label: "genre", title: "John Lennon", value: 1, to: "hard rock"},
        {from: "MembersX", label: "genre", title: "Ronnie Wood, Brian Jones", value: 2, to: "psychedelic rock"},
        {from: "MembersY", label: "genre", title: "George Harrison, Paul McCartney, John Lennon", value: 3, to: "psychedelic rock"},
        {from: "MembersX", label: "genre", title: "Bill Wyman, Ronnie Wood, Brian Jones, Keith Richards, Mick Jagger", value: 5, to: "rock and roll"},
        {from: "MembersY", label: "genre", title: "Paul McCartney, John Lennon", value: 2, to: "rock and roll"},
        {from: "MembersX", label: "genre", title: "Bill Wyman, Charlie Watts, Ronnie Wood, Brian Jones, Keith Richards, Mick Jagger", value: 6, to: "rock music"},
        {from: "MembersY", label: "genre", title: "George Harrison, Ringo Starr, John Lennon", value: 3, to: "rock music"}
]);
var edges2 = new vis.DataSet([
    {},
    {from: "(I Can't Get No) SatisfactionSX", label: "genre", to: "rock music"},
    {from: "Hey JudeSY", label: "artist", to: "The BeatlesAY"},
    {from: "The BeatlesAY", label: "genre", to: "rock music"},
    {from: "(I Can't Get No) SatisfactionSX", label: "artist", to: "The Rolling StonesAX"},
    {from: "The Rolling StonesAX", label: "country", to: "United Kingdom"},
    {from: "Hey JudeSY", label: "genre", to: "pop rockGY"},
    {from: "pop rockGY", label: "country", to: "United Kingdom"},
    {from: "(I Can't Get No) SatisfactionSX", label: "genre", to: "rock music"},
    {from: "The BeatlesAY", label: "miembros", to: "MembersY"},
        {from: "MembersY", label: "genre", title: "George Harrison, Ringo Starr, John Lennon", value: 3, to: "rock music"},
    {from: "(I Can't Get No) SatisfactionSX", label: "genre", to: "rock music"},
    {from: "(I Can't Get No) SatisfactionSX", label: "genre", to: "rock music"},
    {from: "The Rolling StonesAX", label: "genre", to: "blues rock"},
        {from: "MembersY", label: "genre", title: "John Lennon", value: 1, to: "blues rock"},
    {from: "The Rolling StonesAX", label: "genre", to: "hard rock"},
        {from: "MembersY", label: "genre", title: "John Lennon", value: 1, to: "hard rock"},
    {from: "The Rolling StonesAX", label: "genre", to: "psychedelic rock"},
        {from: "MembersY", label: "genre", title: "George Harrison, Paul McCartney, John Lennon", value: 3, to: "psychedelic rock"},
    {from: "The Rolling StonesAX", label: "genre", to: "rock and roll"},
        {from: "MembersY", label: "genre", title: "Paul McCartney, John Lennon", value: 2, to: "rock and roll"},
    {from: "The Rolling StonesAX", label: "genre", to: "rock music"},
    {from: "The Rolling StonesAX", label: "miembros", to: "MembersX"},
        {from: "MembersX", label: "genre", title: "Mick Taylor, Bill Wyman, Charlie Watts, Brian Jones, Keith Richards", value: 5, to: "blues rock"},
    {from: "The BeatlesAY", label: "genre", to: "blues rock"},
        {from: "MembersX", label: "genre", title: "Mick Taylor, Charlie Watts, Ronnie Wood", value: 3, to: "hard rock"},
    {from: "The BeatlesAY", label: "genre", to: "hard rock"},
        {from: "MembersX", label: "genre", title: "Ronnie Wood, Brian Jones", value: 2, to: "psychedelic rock"},
    {from: "The BeatlesAY", label: "genre", to: "psychedelic rock"},
        {from: "MembersX", label: "genre", title: "Bill Wyman, Ronnie Wood, Brian Jones, Keith Richards, Mick Jagger", value: 5, to: "rock and roll"},
    {from: "The BeatlesAY", label: "genre", to: "rock and roll"},
        {from: "MembersX", label: "genre", title: "Bill Wyman, Charlie Watts, Ronnie Wood, Brian Jones, Keith Richards, Mick Jagger", value: 6, to: "rock music"}
]);

// create a network
var container = document.getElementById('mynetwork');
var container2 = document.getElementById('mynetwork2');

// provide the data in the vis format
var data = {
    nodes: nodes,
    edges: edges
};
var data2 = {
    nodes: nodes2,
    edges: edges2
};
var options = {
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
        shadow: true
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
};

// initialize your networks!
var network = new vis.Network(container, data, options);
var network2 = new vis.Network(container2, data2, options);

network.moveTo({
  scale: 0.5             // Zooms out
});
network2.moveTo({
  scale: 0.5             // Zooms out
});

// WIP
network.on("click", function(params) {
  params.event = "[original event]";
  if (params.nodes.length > 0) {

    var name = params.nodes[0];


    $.getJSON('/app/static/songData1.json')
        .done(function (data) {

            var len = Object.keys(data.ID).length;
            var table = document.getElementById("mytable");

            addRow(table, data.ID[0], "");

            for (i = 0; i < len; i++) {
                var lastRowCells = table.rows[table.rows.length-1].cells;

                if (data.idPropertyName[i] == lastRowCells[0].innerHTML) {
                    lastRowCells[1].innerHTML += ", " + data.valueProperty[i];
                }
                else {
                    addRow(table, data.idPropertyName[i], data.valueProperty[i]);
                }
            }

        })
  }
});


function addRow(table, data1, data2) {
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = data1;
    cell2.innerHTML = data2;
};