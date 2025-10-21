function generate_pie(data) {
    pie_content = [];
    console.log(data);
    pcolor = {}
    
    // Enhanced neon color palette
    const neonColors = [
        '#00ffff', '#ff00ff', '#00ff00', '#ffff00', '#ff9717ff', 
        '#ff0088', '#0088ff', '#88ff00', '#ff8800', '#aa00ff'
    ];
    
    let colorIndex = 0;
    
    $.each(data, function(key, value) {
        if (colorsjson[key]) {
            pcolor[key] = colorsjson[key];
        } else {
            pcolor[key] = neonColors[colorIndex % neonColors.length];
            colorIndex++;
        }
        
        pie_content.push({
            label: key,
            value: data[key],
            color: pcolor[key],
            caption: `${key} - ${data[key]} mins`
        });
    });

    console.log(pie_content);
    
    pie = new d3pie("pieChart", {
        "header": {
            "titleSubtitlePadding": 9
        },
        "footer": {
            "color": "#00ffff",
            "fontSize": 12,
            "font": "VT323, monospace",
            "location": "bottom-left"
        },
        "size": {
            "canvasWidth": 590,
            "pieOuterRadius": "90%",
            "pieInnerRadius": "50%"
        },
        "data": {
            "sortOrder": "value-desc",
            "content": pie_content
        },
        "labels": {
            "outer": {
                "pieDistance": 32
            },
            "inner": {
                "hideWhenLessThanPercentage": 3
            },
            "mainLabel": {
                "fontSize": 14,
                "color": "#00ffff",
                "font": "VT323, monospace"
            },
            "percentage": {
                "color": "#00ffff",
                "decimalPlaces": 2,
                "font": "VT323, monospace"
            },
            "value": {
                "color": "#00ffff",
                "fontSize": 14,
                "font": "VT323, monospace"
            },
            "lines": {
                "enabled": true,
                "color": "#00ffff",
                "style": "dashed"
            },
            "truncation": {
                "enabled": true
            }
        },
        "tooltips": {
            "enabled": true,
            "type": "caption",
            "styles": {
                "fadeInSpeed": 387,
                "backgroundOpacity": 0.9,
                "color": "#00ffff",
                "fontSize": 14,
                "padding": 14,
                "font": "VT323, monospace",
                "borderRadius": 8,
                "borderColor": "#00ffff",
                "borderWidth": 1
            }
        },
        "effects": {
            "pullOutSegmentOnClick": {
                "speed": 400,
                "size": 14,
                "effect": "bounce"
            },
            "highlightSegmentOnMouseover": true
        },
        "misc": {
            "gradient": {
                "enabled": true,
                "percentage": 100
            },
            "colors": {
                "background": "transparent",
                "segments": pie_content.map(item => item.color),
                "stroke": "#0a0a12"
            }
        }
    });
}

$(document).ready(function(){
    processcount = {};
    colorsjson = {};
    colorsloaded = false;

    json_data = $('#json_data').html();
    json_data = JSON.parse(json_data);

    $('#title').html(`<small>Report of</small> <b>${json_data.report_date}</b>`);
    $('#generated').html(`<small>Generated on</small> <b>${json_data.generation_date}</b>`);

    // Add staggered loading animation
    $('.glass-panel').each(function(index) {
        $(this).css('animation-delay', (index * 0.2) + 's');
    });
    initTypewriter();
    buildvisuals();
});

async function buildvisuals() {
    try {
        colorsjson = json_data.colors_data;
        colorsloaded = true;
    } catch(e) {
        console.log("No custom colors loaded, using neon palette");
    }

    var data = json_data.csv_data;
    console.log(data);
    processed_data = []
    data.forEach(function(row) {
        if(processcount[row.process])
            processcount[row.process] = (processcount[row.process]+1);
        else
            processcount[row.process] = 1;
        var date = new Date(row.Date);
        processed_data.push({
            title: row.title,
            process: row.process,
            date: date,
            group: date.getMinutes(),
            variable: date.getHours()
        });
    });
    
    console.log(processcount);

    generate_pie(processcount);
    console.log(processed_data);
    buildHeatMap(processed_data);
    loadnumeric();
}

function generate_color() {
    // Use neon color palette instead of random colors
    const neonColors = ['#00ffff', '#ff00ff', '#00ff00', '#ffff00', '#ff7700', '#ff0088'];
    return neonColors[Math.floor(Math.random() * neonColors.length)];
}

function buildHeatMap(csv_data) {
    var margin = {top: 80, right: 25, bottom: 30, left: 40},
    width = 1200 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

    // Clear previous content
    d3.select("#my_dataviz").html("");

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var myGroups = [];
    for(var i = 0; i<60; i++)
        myGroups.push(i.toString());
    
    var myVars = [];
    for(var i = 23; i>=0; i--)
        myVars.push(i.toString());

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(myGroups)
        .padding(0.05);
        
    svg.append("g")
        .style("font-size", 12)
        .style("font-family", "VT323, monospace")
        .style("color", "#00ffff")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove();

    // Build Y scales and axis:
    var y = d3.scaleBand()
        .range([ height, 0 ])
        .domain(myVars)
        .padding(0.05);
        
    svg.append("g")
        .style("font-size", 12)
        .style("font-family", "VT323, monospace")
        .style("color", "#00ffff")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove();

    // Enhanced tooltip with glass effect
    var tooltip = d3.select("#my_dataviz")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("z-index", "1000")
        .style("pointer-events", "none")
        .style("transition", "all 0.3s ease");

    // Enhanced hover effects
    var mouseover = function(d) {
        tooltip
            .style("opacity", 1)
            .style("display", "block");
            
        d3.select(this)
            .transition()
            .duration(300)
            .attr("width", x.bandwidth() * 1.1)
            .attr("height", y.bandwidth() * 1.1)
            .attr("x", function(d) { return x(d.group) - (x.bandwidth() * 0.05) })
            .attr("y", function(d) { return y(d.variable) - (y.bandwidth() * 0.05) })
            .style("opacity", 1)
            .style("filter", "url(#glow)");
    }
    
    var mousemove = function(d) {
        tooltip
            .html(`
                <div style="text-align: center;">
                    <strong style="color: #00ffff; text-shadow: 0 0 8px #00ffff;">${d.process}</strong><br/>
                    <span style="color: #88ff88;">${d.title}</span><br/>
                    <small style="color: #ffff88;">${d.date.toLocaleString()}</small>
                </div>
            `)
            .style("left", (d3.event.pageX + 15) + "px")
            .style("top", (d3.event.pageY - 15) + "px");
    }
    
    var mouseleave = function(d) {
        tooltip
            .style("opacity", 0)
            .style("display", "none");
            
        d3.select(this)
            .transition()
            .duration(300)
            .attr("width", x.bandwidth())
            .attr("height", y.bandwidth())
            .attr("x", function(d) { return x(d.group) })
            .attr("y", function(d) { return y(d.variable) })
            .style("opacity", 0.8)
            .style("filter", "none");
    }

    // Add glow filter for hover effects
    var defs = svg.append("defs");
    var filter = defs.append("filter")
        .attr("id", "glow")
        .attr("height", "300%")
        .attr("width", "300%")
        .attr("x", "-100%")
        .attr("y", "-100%");
        
    filter.append("feGaussianBlur")
        .attr("stdDeviation", "3.5")
        .attr("result", "coloredBlur");
        
    var feMerge = filter.append("feMerge");
    feMerge.append("feMergeNode")
        .attr("in", "coloredBlur");
    feMerge.append("feMergeNode")
        .attr("in", "SourceGraphic");

    // add the squares with enhanced styling
    console.log(csv_data);
    svg.selectAll()
        .data(csv_data, function(d) {return d.group+':'+d.variable;})
        .enter()
        .append("rect")
        .attr("x", function(d) { return x(d.group) })
        .attr("y", function(d) { return y(d.variable) })
        .attr("rx", 6)  // Rounded corners
        .attr("ry", 6)  // Rounded corners
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function(d) { 
            const color = pcolor[d.process] || generate_color();
            // Convert to semi-transparent with neon border
            return color + "40"; // 25% opacity
        })
        .style("stroke", function(d) { 
            return pcolor[d.process] || generate_color();
        })
        .style("stroke-width", 2)
        .style("opacity", 0.8)
        .style("transition", "all 0.3s ease")
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave);

    // Enhanced titles
    svg.append("text")
        .attr("x", 0)
        .attr("y", -50)
        .attr("text-anchor", "left")
        .style("font-size", "24px")
        .style("font-family", "VT323, monospace")
        .style("fill", "#00ffff")
        .style("text-shadow", "0 0 10px #00ffff")
        .text("Activity");

    svg.append("text")
        .attr("x", 0)
        .attr("y", -20)
        .attr("text-anchor", "left")
        .style("font-size", "16px")
        .style("font-family", "VT323, monospace")
        .style("fill", "#88ffff")
        .style("opacity", 0.8)
        .text("Minute-to-Minute activity map");
}
// Advanced Typewriter system for footer with multiple lines
function initTypewriter() {
    const messages = [
        "No grass was touched during the making of this report", 
        "If you hate this app, contact Manasvi",
        "Warning: May cause sudden urge to go outside",
        "Screen time > Sun time? We don't judge... much",
        "Remember: Real life has better graphics",
        "This app certified 100% grass-free",
        "Error 404: Grass not found",
        "Compiling excuses to stay indoors...",
        "Solar radiation detected. Recommend staying inside",
        "Touch grass.exe not found in system32",
        "Battery low. Please connect to reality",
        "Downloading sunlight... failed",
        "Indoor activities: ██████████ 100%",
        "Outdoor activities: ███░░░░░░░ 30%"
    ];

    const typingElement = document.getElementById('signature');
    let messageIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let isPaused = false;

    function type() {
        const currentMessage = messages[messageIndex];
        
        if (!isDeleting && !isPaused) {
            // Typing forward
            if (charIndex < currentMessage.length) {
                typingElement.textContent = currentMessage.substring(0, charIndex + 1);
                charIndex++;
                setTimeout(type, getRandomSpeed(60, 120));
            } else {
                // Finished typing, pause before deleting
                isPaused = true;
                setTimeout(() => {
                    isPaused = false;
                    isDeleting = true;
                    type();
                }, 1500);
            }
        } else if (isDeleting && !isPaused) {
            // Deleting (backspace effect)
            if (charIndex > 0) {
                typingElement.textContent = currentMessage.substring(0, charIndex - 1);
                charIndex--;
                setTimeout(type, getRandomSpeed(25, 60));
            } else {
                // Finished deleting, move to next message
                isDeleting = false;
                messageIndex = (messageIndex + 1) % messages.length;
                setTimeout(type, 300);
            }
        }
    }

    function getRandomSpeed(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    // Start the typewriter
    setTimeout(type, 2000);
}
function loadnumeric() {
    console.log(pie_content);
    var $numeric = $('#numeric table');
    pie_content.sort(function(a, b) {
        return b.value - a.value;
    });
    
    pie_content.forEach(function(proc){
        $numeric.append(`
            <tr>
                <td>
                    <span class="color-badge" style="background:${proc.color}; box-shadow: 0 0 8px ${proc.color};"></span>
                    ${proc.label}
                </td>
                <td style="font-family: 'VT323', monospace; letter-spacing: 1px;">
                    ${formattime(proc.value)}
                </td>
            </tr>
        `);
    });
}

function formattime(value) {
    const hours = Math.floor(value/60);
    const minutes = value % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}