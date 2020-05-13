// create an array with nodes
var nodes = new vis.DataSet([
    {id: 1, label: "(I can't get no) Satisfaction", group: 1, level: 1},
    {id: 2, label: "Hey Jude", group: 1, level: 7},
    {id: 3, label: "The Rolling Stones", group: 2, level: 2},
    {id: 4, label: "The Beatles", group: 2, level: 6},
    {id: 5, label: "Mick Jagger", group: 3, level: 3},
    {id: 6, label: "Ringo Starr", group: 3, level: 5},
    {id: 7, label: "English", group: 4, level: 4},
    {id: 8, label: "Rock and Roll", group: 5, level: 4},
    {id: 9, label: "Rock Music", group: 5, level: 4},
    {id: 10, label: "Psychedelic Rock", group: 5, level: 4},
    {id: 11, label: "Grammy Lifetime Achievement Award", group: 5, level: 4},
    {id: 12, label: "Grammy Award Best Music Video", group: 5, level: 4},
    {id: 13, label: "Rock and Roll Hall of Fame", group: 5, level: 4},
    {id: 14, label: "Polydor Records", group: 5, level: 4},
    {id: 15, label: "Chuck Berry", group: 5, level: 4},
    {id: 16, label: "Rock Music", group: 6, level: 4},
    {id: 17, label: "Blues", group: 6, level: 4},
    {id: 18, label: "Rock and Roll", group: 6, level: 4}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: 1, to: 7},
    {from: 1, to: 3},
    {from: 2, to: 7},    
    {from: 2, to: 4},
    {from: 3, to: 5},
    {from: 3, to: 8},
    {from: 3, to: 9},
    {from: 3, to: 10},
    {from: 3, to: 11},
    {from: 3, to: 12},
    {from: 3, to: 13},
    {from: 3, to: 14},
    {from: 3, to: 15},
    {from: 4, to: 6},
    {from: 4, to: 8},
    {from: 4, to: 9},
    {from: 4, to: 10},
    {from: 4, to: 11},
    {from: 4, to: 12},
    {from: 4, to: 13},
    {from: 4, to: 14},
    {from: 4, to: 15},
    {from: 5, to: 16},
    {from: 5, to: 17},
    {from: 5, to: 18},
    {from: 6, to: 16},
    {from: 6, to: 17},
    {from: 6, to: 18}
]);

// create a network
var container = document.getElementById('mynetwork');

// provide the data in the vis format
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
    layout: {
        hierarchical: {
            direction: 'LR'
        }
    },
    edges: {
        arrows: 'to',
        smooth: {
            type: 'cubicBezier',
            forceDirection: 'horizontal'
        }
    },
    nodes: {
    	shape: 'box',
    	widthConstraint: {
    		maximum: 120
    	}
    }
};

// initialize your network!
var network = new vis.Network(container, data, options);