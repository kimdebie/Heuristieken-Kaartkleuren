/* 
 * Visualizing the networks 
 * Based on http://bl.ocks.org/mbostock/29cc3cc4078091fd2115
 */


var states = [],
    redConnections = [],
    greenConnections = [],
    yellowConnections = [],
    blueConnections = []

// visualization builds on csv file containing node plus color
d3.csv('http://localhost:8000/Network_files/solutionfile.csv', function(error, dataset){

  // creates an array for each node's color 'state'
  dataset.forEach(function(d){
      if (d.color == "red") {
        redConnections.push(d.connection)
      } else if (d.color == "green") {
        greenConnections.push(d.connection)
      } else if (d.color == "yellow") {
        yellowConnections.push(d.connection)
      } else if (d.color == "blue") {
        blueConnections.push(d.connection)
      };
  });


  // selects grid from html
  d3.select("#grid").text().split("\n").forEach(function(line, i) {
    // splits content of grid
    var re = /\w+/g, m;

    // saves name and relevant color
    while (m = re.exec(line)) states.push({
      name: m[0],
      red: redConnections.indexOf(m[0]) >= 0,
      green: greenConnections.indexOf(m[0]) >= 0,
      yellow: yellowConnections.indexOf(m[0]) >= 0,
      blue: blueConnections.indexOf(m[0]) >= 0,
      // rounding up to accomodate for different input length
      x: Math.ceil(m.index / 3),
      y: i
    });
  });


  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  var gridWidth = d3.max(states, function(d) { return d.x; }) + 1,
      gridHeight = d3.max(states, function(d) { return d.y; }) + 1,
      cellSize = 40;

  // creating objects for every node
  var state = svg.append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    .selectAll(".state")
      .data(states)
    .enter().append("g")
      .attr("class", function(d) { 
        if (d.red) {
          return "state--red"
        } else if (d.green) {
          return "state--green"
        } else if (d.blue){
          return "state--blue"
        }  else if (d.yellow) {
          return "state--yellow"
        }  else {
          return "state"
        }})
      .attr("transform", function(d) { return "translate(" + (d.x - gridWidth / 2) * cellSize + "," + (d.y - gridHeight / 2) * cellSize + ")"; });

  // drawing rectangles around the nodes
  state.append("rect")
      .attr("x", -cellSize / 2)
      .attr("y", -cellSize / 2)
      .attr("width", cellSize - 1)
      .attr("height", cellSize - 1);

  // writes text inside rectangles
  state.append("text")
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });

});