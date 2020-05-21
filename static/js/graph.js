// create an array with nodes
var nodes = new vis.DataSet([
    {id: "Start Me UpSX", label: "Start Me Up", group: 1, level: 1},
    {id: "(I Can't Get No) SatisfactionSY", label: "(I Can't Get No) Satisfaction", group: 1, level: 7},
    {id: "The Rolling Stones", label: "The Rolling Stones", group: 2, level: 4}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: "Start Me UpSX", label: "artist", to: "The Rolling Stones"},
    {from: "(I Can't Get No) SatisfactionSY", label: "artist", to: "The Rolling Stones"},
    {from: "Start Me UpSX", label: "intérprete", to: "The Rolling Stones"},
    {from: "(I Can't Get No) SatisfactionSY", label: "intérprete", to: "The Rolling Stones"}
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
            direction: 'LR',
            levelSeparation: 250
        }
    },
    edges: {
        arrows: 'to'/*,
        smooth: {
            type: 'cubicBezier',
            forceDirection: 'horizontal'
        }*/
    },
    nodes: {
        shape: 'box',
        widthConstraint: {
            maximum: 120
        }
    },
    physics: false
};

// initialize your network!
var network = new vis.Network(container, data, options);