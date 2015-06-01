var width = $("#github").width();
var height = $("#github").height();

var github_ico = "/static/img/github.ico";
var twitter_ico = "/static/img/twitter.ico";

var github = d3.select("#github").append("svg").attr("width", width).attr("height", height);
var twitter = d3.select("#twitter").append("svg").attr("width", width).attr("height", height);

function draw(error, graph, svg, ico) 
{
    console.log(graph.nodes)

  var force = d3.layout.force()
    .charge(-100)
    .gravity(.05)
    .distance(100)
    .size([width, height]);

  force.nodes(graph.nodes).links(graph.links).start();

  var link = svg.selectAll(".link")
      .data(graph.links)
      .enter().append("line")
      .attr("class", "link")

  var node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter().append("g")
      .attr("class", "node")
      .call(force.drag);

  node.append("image").attr("xlink:href", ico)
  .attr("x", -8)
  .attr("y", -8)
  .attr("width", 16)
  .attr("height", 16);

  node.append("text")
  .attr("dx", 12)
  .attr("dy", ".35em")
  .text(function(d){ return d.name });

  force.on("tick", function(){
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d){ return "translate(" + d.x + "," + d.y + ")"; });

  });
}

d3.json("/static/data/github.json", function(error, graph){draw(error, graph, github, github_ico)});
d3.json("/static/data/twitter.json", function(error, graph){draw(error, graph, twitter, twitter_ico)});

$("button").click(function(events){

	events.preventDefault();

  d3.selectAll("svg").remove();

	Pace.track(function(){

    $.post("/uir", $("form").serialize(), 

      function(data, status){

        var github = d3.select("#github").append("svg").attr("width", width).attr("height", height);
        var twitter = d3.select("#twitter").append("svg").attr("width", width).attr("height", height);

        d3.json("/static/data/" + $("#github_username").val() + "_github.json", function(error, graph){draw(error, graph, github, github_ico)});
        d3.json("/static/data/" + $("#twitter_username").val() + "_twitter.json", function(error, graph){draw(error, graph, twitter, twitter_ico)});

        $("table").html(data);
      });
  });
});
