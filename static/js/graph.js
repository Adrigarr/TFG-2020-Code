// create an array with nodes
var nodes = new vis.DataSet([
    {id: "(I Can't Get No) Satisfaction", label: "(I Can't Get No) Satisfaction", group: 1, level: 1},
    {id: "Hey Jude", label: "Hey Jude", group: 1, level: 7},
    {id: "The Rolling Stones", label: "The Rolling Stones", group: 2, level: 2},
    {id: "The Beatles", label: "The Beatles", group: 2, level: 6},
    {id: "English", label: "English", group: 3, level: 4}
]);

// create an array with edges
var edges = new vis.DataSet([
    {from: "(I Can't Get No) Satisfaction", label: "artist", to: "The Rolling Stones"},
    {from: "Hey Jude", label: "artist", to: "The Beatles"},
    {from: "(I Can't Get No) Satisfaction", label: "language", to: "English"},
    {from: "Hey Jude", label: "language", to: "English"}
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