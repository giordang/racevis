function splitTable(data, div){
    let table = document.querySelector("table");
    let thData = Object.keys(data[0]);

    let tHead = table.createTHead();
    let row = tHead.insertRow();
    for (let key of thData){
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th);
    }

    for (let element of data){
        let row = table.insertRow();
        for (key in element){
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
    }

};


//adapted from https://medium.com/@kj_schmidt/making-an-animated-donut-chart-with-d3-js-17751fde4679
function hrDist(data, div){
    var width = 350;
    var height = 350;
    var margin = 60;
    var radius = Math.min(width, height) / 2 - margin;
    var donutWidth = 75; 

    var color = d3.scale.ordinal()
        .domain(data)
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56"]);

    var svg = d3.select(div)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');

    var arc = d3.svg.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius);

    var outerArc = d3.svg.arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9);

   var pie = d3.layout.pie()
        .value(function (d) {
             return d.percentage;
        })
        .sort(null);

   var path = svg.selectAll('path')
        .data(pie(data))
        .enter().append('path')
            .on("mouseover", d => mouseover(d))
            .on("mousemove", mousemove)
            .on("mouseout", mouseout)
            .attr('d', arc)
            .attr('fill', function (d) {
                return color(d.data.hr);
            })
            .attr('transform', 'translate(0, 0)')

    svg
    .selectAll('allPolylines')
    .data(pie(data))
    .enter()
    .append('polyline')
        .attr("stroke", "black")
        .style("fill", "none")
        .attr("stroke-width", 1)
        .attr('points', function(d) {
        var posA = arc.centroid(d) 
        var posB = outerArc.centroid(d) 
        var posC = outerArc.centroid(d); 
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 
        posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); 
        return [posA, posB, posC]
        });
        
    svg
    .selectAll('allLabels')
    .data(pie(data))
    .enter()
    .append('text')
        .text( function(d) { console.log(d.data.hr) ; return d.data.hr } )
        .attr('transform', function(d) {
            var pos = outerArc.centroid(d);
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
            return 'translate(' + pos + ')';
        })
        .style('text-anchor', function(d) {
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            return (midangle < Math.PI ? 'start' : 'end')
        });

    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("display", "none");
    
    function mouseover(d) {
        div.style("display", "inline");
        div.text(d.data.percentage)
    }
        
    function mousemove() {
        div
            .style("left", (d3.event.pageX - 34) + "px")
            .style("top", (d3.event.pageY - 12) + "px");
    }
        
    function mouseout() {
        div.style("display", "none");
    }

};

//adapted from https://medium.com/@kj_schmidt/making-an-animated-donut-chart-with-d3-js-17751fde4679
function paceDist(data, div){
    var width = 350;
    var height = 350;
    var margin = 60;
    var radius = Math.min(width, height) / 2 - margin;
    var donutWidth = 75; 

    var color = d3.scale.ordinal()
        .domain(data)
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56"]);

    var svg = d3.select(div)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');

   var arc = d3.svg.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius);

    var outerArc = d3.svg.arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9);

   var pie = d3.layout.pie()
        .value(function (d) {
             return d.percentage;
        })
        .sort(null);

   var path = svg.selectAll('path')
        .data(pie(data))
        .enter().append('path')
            .on("mouseover", d => mouseover(d))
            .on("mousemove", mousemove)
            .on("mouseout", mouseout)
            .attr('d', arc)
            .attr('fill', function (d, i) {
                return color(d.data.pace);
            })
            .attr('transform', 'translate(0, 0)');

    svg
    .selectAll('allPolylines')
    .data(pie(data))
    .enter()
    .append('polyline')
        .attr("stroke", "black")
        .style("fill", "none")
        .attr("stroke-width", 1)
        .attr('points', function(d) {
        var posA = arc.centroid(d) 
        var posB = outerArc.centroid(d) 
        var posC = outerArc.centroid(d); 
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 
        posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); 
        return [posA, posB, posC]
        });

    svg
    .selectAll('allLabels')
    .data(pie(data))
    .enter()
    .append('text')
        .text( function(d) { console.log(d.data.pace) ; return d.data.pace } )
        .attr('transform', function(d) {
            var pos = outerArc.centroid(d);
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
            return 'translate(' + pos + ')';
        })
        .style('text-anchor', function(d) {
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            return (midangle < Math.PI ? 'start' : 'end')
        });


        var div = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("display", "none");
        
        function mouseover(d) {
            div.style("display", "inline");
            div.text(d.data.percentage)
        }
            
        function mousemove() {
            div
                .style("left", (d3.event.pageX - 34) + "px")
                .style("top", (d3.event.pageY - 12) + "px");
        }
            
        function mouseout() {
            div.style("display", "none");
        }

};

//adapted from https://bl.ocks.org/uredkar/71c3a0d93cc05527c83cdc12f9549ab3
function lineAltHrPace(data, div){
    var label = d3.select(div);

    var margin = {top: 20, right: 20, bottom: 70, left: 40};
    var width = 800 - margin.left - margin.right;
    var height = 400 - margin.top - margin.bottom;
    
    var x = d3.scale.linear().range([0, width]);
    var y0 = d3.scale.linear().range([height, 0]);
    var y1 = d3.scale.linear().range([height, 0]);
    var y2 = d3.scale.linear().range([height, 0]);
    
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom");
    var yAxis0 = d3.svg.axis().scale(y0)
        .orient("left");
    var yAxis1 = d3.svg.axis().scale(y1)
        .orient("left");
    var yAxis2 = d3.svg.axis().scale(y2)
        .orient("right");
    
    var valueline0 = d3.svg.line() //altitude
        .x(function(d) { return x(d.total_dist); })
        .y(function(d) { return y0(d.alt); });

    var valueline1 = d3.svg.line() //heart rate
        .x(function(d) { return x(d.total_dist); })
        .y(function(d) { return y1(d.hr); });

    var valueline2 = d3.svg.line() //pace
        .x(function(d) { return x(d.total_dist); })
        .y(function(d) { return y2(d.pace); });
        
    var	svg = d3.select(div)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    data.forEach(function(d) {
        d.total_dist = d.total_dist;
        d.alt = +d.alt;
        d.hr = +d.hr;
        d.pace = +d.pace;
    });
    
    x.domain(d3.extent(data, function(d) { return d.total_dist; }));
    y0.domain(d3.extent(data, function(d) { return d.alt; }));
    y1.domain(d3.extent(data, function(d) { return d.hr; }));
    y2.domain(d3.extent(data, function(d) { return d.pace; }));
    
    svg.append("path")		
        .attr("class", "line_alt")
        .attr("d", valueline0(data)); //altitude
    
    svg.append("path")		
        .attr("class", "line_hr")
        .attr("d", valueline1(data)); //hr

    svg.append("path")		
        .attr("class", "line_pace")
        .attr("d", valueline2(data)); //pace
    
    /*
    svg		
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("r", 10)
        .attr("cx", function(d) {
            return x(d.total_dist)
        })
        .attr("cy", function(d) {
            return y(d.alt)
        })
        .on("mouseover", function(d,i) {
            label.style("transform", "translate("+ x(d.total_dist) +"px," + (y(d.alt)) +"px)")
            label.text(d.alt)
        });   
    */
    
    svg.append("g")		
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    
    svg.append("g")			
        .attr("class", "y axis")
        .call(yAxis0);

    svg.append("g")			
        .attr("class", "y axis")
        .attr("transform", "translate(" + width + ",0)")
        .call(yAxis1);

    svg.append("g")			
        .attr("class", "y axis")
        .attr("transform", "translate(" + width + ",0)")
        .call(yAxis2);

};



//adapted from http://bl.ocks.org/Jverma/887877fc5c2c2d99be10
function barSplitPace(data, div) {
    //canvas dimensions
    var margin = {top: 20, right: 20, bottom: 70, left: 60};
    var width = 350 - margin.left - margin.right;
    var height = 350 - margin.top - margin.bottom;


    //ranges
    var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
    var y = d3.scale.linear().range([height, 0]);

    //axes
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    //SVG
    var svg = d3.select(div)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    //load data
    data.forEach(function(d) {
            d.Split = d.Split;
            d.Pace = + d.Pace;
        });

    //scale data range
    x.domain(data.map(function(d) { return d.Split; }));
    y.domain([0, d3.max(data, function(d) { return d.Pace; })]);

    //add axis
    svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
        .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", "-.55em")
            .attr("transform", "rotate(-90)" );

    svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
        .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 5)
            .attr("dy", ".71em")
            .style("text-anchor", "end")

    //add bars
    svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
            .on("mouseover", d => mouseover(d))
            .on("mousemove", mousemove)
            .on("mouseout", mouseout)
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.Split); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.Pace); })
            .attr("height", function(d) { return height - y(d.Pace); });
    
    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "end")
        .attr("y", -40)
        .attr("x", -55)
        .attr("transform", "rotate(-90)")
        .text("Average Pace (min/mile)");

    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("display", "none");
    
    function mouseover(d) {
        div.style("display", "inline");
        div.text(d.Pace)
    }
        
    function mousemove() {
        div
            .style("left", (d3.event.pageX - 34) + "px")
            .style("top", (d3.event.pageY - 12) + "px");
    }
        
    function mouseout() {
        div.style("display", "none");
    }
};


function barSplitHR(data, div) {
    //canvas dimensions
    var margin = {top: 20, right: 20, bottom: 70, left: 60};
    var width = 350 - margin.left - margin.right;
    var height = 350 - margin.top - margin.bottom;


    //ranges
    var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
    var y = d3.scale.linear().range([height, 0]);

    //axes
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    //SVG
    var svg = d3.select(div)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    //load data
    data.forEach(function(d) {
            d.Split = d.Split;
            d.HR = + d.HR;
        });

    //scale data range
    x.domain(data.map(function(d) { return d.Split; }));
    y.domain([0, d3.max(data, function(d) { return d.HR; })]);

    //add axis
    svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
        .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", "-.55em")
            .attr("transform", "rotate(-90)" );

    svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
        .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 5)
            .attr("dy", ".71em")
            .style("text-anchor", "end")

    //add bars
    svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
            .on("mouseover", d => mouseover(d))
            .on("mousemove", mousemove)
            .on("mouseout", mouseout)
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.Split); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.HR); })
            .attr("height", function(d) { return height - y(d.HR); });

    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "end")
        .attr("y", -40)
        .attr("x", -45)
        .attr("transform", "rotate(-90)")
        .text("Average Heart Rate (bpm)");

    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("display", "none");
    
    function mouseover(d) {
        div.style("display", "inline");
        div.text(d.HR)
    }
        
    function mousemove() {
        div
            .style("left", (d3.event.pageX - 34) + "px")
            .style("top", (d3.event.pageY - 12) + "px");
    }
        
    function mouseout() {
        div.style("display", "none");
    
    }
};