// Get JSON from API
var request = new XMLHttpRequest();
request.open('GET', 'https://winter-pivot-385718.uc.r.appspot.com/clusters', true);
var myData;

request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
        myData = JSON.parse(request.responseText);
        var width = window.innerWidth,
            height = window.innerHeight,
            padding = 4,
            maxRadius = 7,
            active = false,
            activeNode = d3.select(null);


        var standardZoom = [width/2, height/2, height];

        var nodes = [];
        // Assign radius and data to each node, then push into array.
        for (var i = 0; i < myData.length; ++i) {
            nodes.push({
                radius: myData[i]["articles"].length * maxRadius,
                data: myData[i]["articles"],
                label: myData[i]["label"],
                index: i
            });
        }

        var color = d3.scale.category20()
            .domain(d3.range(myData.length));

        // Use the pack layout to initialize node positions.
        d3.layout.pack()
            .size([width, height])
            .value(function(d) { return d.radius * d.radius; })
            .nodes({values: d3.nest()
                .key(function(d) { return d.label; })
                .entries(nodes)});

        var force = d3.layout.force()
            .nodes(nodes)
            .size([width, height])
            .gravity(.02)
            .charge(0)
            .on("tick", tick)
            .start();

        var svg = d3.select("div#container").append("svg")
            .attr("width", width)
            .attr("height", height)
            .classed("svg-content", true)
            .append("g");

        window.addEventListener("resize", function(e) {
            width = window.innerWidth;
            height = window.innerHeight;
            standardZoom = [width/2, height/2, height];
            d3.select("svg")
                .attr("width", width)
                .attr("height", height);
            force.size([width, height])
        });

        var node = svg.selectAll(".node")
            .data(nodes)
            .enter()
            .append("g")
            .on("click", clicked)
            .call(force.drag);

        node.append("circle")
            .attr("r", function(d) {return d.radius})
            .style("fill", function(d) {return color(d.index)});

        node.append("text")
            .attr("text-anchor", "middle")
            .attr("font-size", function(d) {return Math.sqrt(d.radius * 5)})
            .text(function(d) { return d.label });


        node.transition()
            .duration(750)
            .delay(function(d, i) { return i * 5; });

        function getZoomCoords(e) {
            return [e.x, e.y, e.radius * 2];
        }

        function clicked(e) {
            if (d3.event.defaultPrevented) return; // dragged
            if (!active) { // zoom from standard to selected node
                force.stop();
                showLinks(e);
                activeNode = e;
                active = true;
                transition(svg, standardZoom, getZoomCoords(e));
            } else if (activeNode === e) { // zoom out from selected node
                restoreLabel(activeNode);
                activeNode = d3.select(null);
                active = false;
                transition(svg, getZoomCoords(e), standardZoom);
            } else { // zoom from one node to the other
                restoreLabel(activeNode);
                showLinks(e);
                var oldActiveNode = activeNode;
                activeNode = e;
                transition(svg, getZoomCoords(oldActiveNode), getZoomCoords(e));
            }
        }

        function showLinks(e) {
            d3.selectAll("text")
                .filter(function(d, i) { return i == e.index})
                .attr("font-size", caclulcateLinkFontSize(e))
                .html(buildLinksString(e));
        }

        function restoreLabel(e) {
            d3.selectAll("text")
                .filter(function(d, i) { return i == e.index})
                .attr("font-size", calculateLabelFontSize(e))
                .html(e.label);
        }

        function buildLinksString(e) {
            var dataArr = e.data;
            var ret = "";
            var dy = calculateLinkSpacing(e);
            var y = dataArr.length * (dy / 2) * -1;
            for (var i = 0; i < dataArr.length; ++i) {
                var thisData = dataArr[i];
                ret += "<tspan x=\"0\" y=\"" + y + "\">" +
                    "<a xlink:href=\""  + thisData["link"] + "\" target=\"_blank\">"
                    + makeLink(thisData) +
                    "</a>" +
                    "</tspan>";
                y += dy;
            }
            return ret;
        }

        function truncateText(str, length, ending) {
            if (length == null) {
                length = 100;
            }
            if (ending == null) {
                ending = '...';
            }
            if (str.length > length) {
                return str.substring(0, length - ending.length) + ending;
            } else {
                return str;
            }
        }

        function makeLink(d) {
            return truncateText(d["source"] + ": " + d["raw"], 100);
        }

        function calculateLinkSpacing(d) {
            return caclulcateLinkFontSize(d) * 2.5;
        }

        function caclulcateLinkFontSize(d) {
            return Math.min(6, d.radius / 32);
        }

        function calculateLabelFontSize(d) {
            return Math.sqrt(d.radius * 5);
        }

        function transition(svg, start, end) {
            var center = [width / 2, height / 2],
                i = d3.interpolateZoom(start, end);

            svg.attr("transform", transform(start))
                .transition()
                .delay(100)
                .duration(i.duration * 1.5)
                .attrTween("transform", function() { return function(t) { return transform(i(t)); }; });

            function transform(p) {
                var k = height / p[2];
                return "translate(" + (center[0] - p[0] * k) + "," + (center[1] - p[1] * k) + ")scale(" + k + ")";
            }
        }


        function tick(e) {
            node.each(collide(.5));
            node.attr("transform", function(d) { return 'translate(' + [d.x, d.y] + ')'; })
        }

        // Resolves collisions between d and all other circles.
        function collide(alpha) {
            var quadtree = d3.geom.quadtree(nodes);
            return function(d) {
                var r = d.radius + maxRadius + padding,
                    nx1 = d.x - r,
                    nx2 = d.x + r,
                    ny1 = d.y - r,
                    ny2 = d.y + r;
                quadtree.visit(function(quad, x1, y1, x2, y2) {
                    if (quad.point && (quad.point !== d)) {
                        var x = d.x - quad.point.x,
                            y = d.y - quad.point.y,
                            l = Math.sqrt(x * x + y * y),
                            r = d.radius + quad.point.radius + padding;
                        if (l < r) {
                            l = (l - r) / l * alpha;
                            d.x -= x *= l;
                            d.y -= y *= l;
                            quad.point.x += x;
                            quad.point.y += y;
                        }
                    }
                    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                });
            };
        }
    } else {
        console.log("1");
        d3.select("div#container")
            .text("Difficulties load loading news data!  :(");
    }
};

request.onerror = function() {
    d3.select("div#container")
        .text("Difficulties loading news data!  :(");
};

request.send();
