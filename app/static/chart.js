    //adapted from http://bl.ocks.org/Jverma/887877fc5c2c2d99be10

    function barSplitPace(data, div) {
        //canvas dimensions
        var margin = {top: 20, right: 20, bottom: 70, left: 40};
        var width = 600 - margin.left - margin.right;
        var height = 300 - margin.top - margin.bottom;


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
                .attr("class", "bar")
                .attr("x", function(d) { return x(d.Split); })
                .attr("width", x.rangeBand())
                .attr("y", function(d) { return y(d.Pace); })
                .attr("height", function(d) { return height - y(d.Pace); });
    };


    function barSplitHR(data, div) {
        //canvas dimensions
        var margin = {top: 20, right: 20, bottom: 70, left: 40};
        var width = 600 - margin.left - margin.right;
        var height = 300 - margin.top - margin.bottom;


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
                .attr("class", "bar")
                .attr("x", function(d) { return x(d.Split); })
                .attr("width", x.rangeBand())
                .attr("y", function(d) { return y(d.HR); })
                .attr("height", function(d) { return height - y(d.HR); });
    };