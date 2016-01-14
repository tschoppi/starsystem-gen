// GLOBALS
// TODO: Clean up the entire JS code. I feel there are a few things that could be done more nicely...
var day_in_year = 1;
var sweet_spot_scale = 1;
var default_zoom = 1;

function animate_solar_system(toDraw, star_letter, context, canvas, centerX, centerY) {
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Draw a counter representing Earth years
    context.beginPath();
    if (day_in_year > 300){ // We're approaching year end! Holiday season :D
        context.fillStyle = 'red';
        context.strokeStyle = 'red';
    } else { // Rest of the year
        context.fillStyle = 'black';
        context.strokeStyle = 'black';
    }
    // 0 is at 3 o'clock, so we start at 1.5 * Pi. The end angle therefore is offset by that much.
    // Everyday, we increase our end angle by 1/365, drawing ever more of the circle.
    var end_angle = 1.5 * Math.PI + (2 * Math.PI * (day_in_year / 365));
    context.arc(40, 40, 20, 1.5 * Math.PI, end_angle);
    context.stroke();

    if (day_in_year > 300 && day_in_year < 320 || day_in_year > 335 && day_in_year < 366){
        // Flash the text, but not too fast!
        context.beginPath();
        context.fillText("1 year!", 23, 33);
    }
    day_in_year = (day_in_year % 365) + 1 // Start counting at 1, up to 365.

    // Reset to defaults
    context.fillStyle = 'black';
    context.strokeStyle = 'black';

    for (var i = 0; i < toDraw.length; i++) {
        if (getCookie(i + star_letter) == "") {
            // We store the rotation belonging to a given astro_body in a cookie
            document.cookie = i + star_letter + "=" + Math.floor((Math.random() * 360) + 1);
        }

        // Getting the rotation and the axes
        var rotationValue = parseInt(getCookie(i + star_letter), 10);
        var semi_major = toDraw[i].max * sweet_spot_scale;
        var semi_minor = toDraw[i].min * sweet_spot_scale;

        // Draw the ellipse
        context.beginPath();
        context.ellipse(centerX, centerY, semi_major, semi_minor, rotationValue, 0, Math.PI * 2);
        context.stroke();
        context.closePath();

        // We use the general, parameterized ellipse equations to find a point on the eclipse, again rotated.
        toDraw[i].x = centerX + (semi_major * Math.cos(toDraw[i].position) * Math.cos(rotationValue) - semi_minor * Math.sin(toDraw[i].position) * Math.sin(rotationValue));
        toDraw[i].y = centerY + (semi_major * Math.cos(toDraw[i].position) * Math.sin(rotationValue) + semi_minor * Math.sin(toDraw[i].position) * Math.cos(rotationValue));

        // Offset the label to the different quadrants
        var left_right = toDraw[i].x > centerX ? 1 : -2;
        var up_down = toDraw[i].y > centerY ? 1 : -1.5;

        // Actually draw the label, with white BG to always readable
        context.fillStyle = 'white';
        var rectWidth = context.measureText(toDraw[i].name).width;
        context.fillRect((left_right * 10) + toDraw[i].x, (up_down * 12) + toDraw[i].y, rectWidth + 5, 15);
        context.beginPath();
        context.fillStyle = 'black';
        context.textBaseline = 'top';
        context.fillText(toDraw[i].name, (left_right * 10) + toDraw[i].x, (up_down * 12) + toDraw[i].y);

        // Draw a dot to represent the astronomical body
        context.beginPath();
        context.arc(toDraw[i].x, toDraw[i].y, 3, 0, 2 * Math.PI, false);
        context.fill();
        context.stroke();

        // Draw the star last, so it will always be visible
        context.beginPath();
        context.arc(centerX, centerY, 3, 0, 2 * Math.PI, false);
        context.fillStyle = 'yellow';
        context.fill();
        context.stroke();
        context.fillStyle = 'black';

        // Calculate an orbital body's speed around the star and store it in the orbital body
        if (toDraw[i].velocity == 0){
            toDraw[i].velocity = (2 * Math.PI) / toDraw[i].orbital_period;
            if (toDraw[i].velocity == 0){
                toDraw[i].velocity += 0.00000000000000001; // Guarantees a non-zero speed
            }
        }
        // Move orbital body
        if (toDraw[i].position < 2 * Math.PI - toDraw[i].velocity){
            toDraw[i].position += toDraw[i].velocity;
        } else {
            toDraw[i].position = 0;
        }
    }
}

function getCookie(cookieName) {
    // Get a specific cookie based on its name
    var name = cookieName + "=";
    var cookieArray = document.cookie.split(';');
    for(var i=0; i<cookieArray.length; i++) {
        var c = cookieArray[i];
        while (c.charAt(0)==' ') c = c.substring(1); // Trim leading whitespace
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}

function zoomIn(){
    sweet_spot_scale += (default_zoom / 5);
}

function zoomOut(){
    sweet_spot_scale -= (default_zoom / 5);
}

function resetZoom(){
    sweet_spot_scale = default_zoom;
}


document.onreadystatechange = function(){
    if (document.readyState === 'complete'){

        document.cookie = "positionOnEllipse=";
        var canvas = document.getElementById("diagram");
        var star_size = parseFloat(document.getElementById("star-radius").innerHTML);
        var outer_limit = parseFloat(document.getElementById("star-limit").innerHTML);
        var star_letter = document.getElementById("star-letter").innerHTML;

        var overviewTable = document.getElementById("objects-overview");
        var rows = overviewTable.getElementsByTagName("tr");
        var toDraw = [];
        var max_size = 0;
        var min_size = 99999; // Super big, so that we can find smaller numbers
        for (var i = 1; i < rows.length; i++){
            row = rows[i];
            // Row 0 contains the headings, the others are javascript attributes of the rows object (in Chrome!)
            if (row !== '0' && row !== 'item' && row !== 'length' && row !== 'namedItem'){
                var min_cell = document.getElementById('min_radius' + i);
                var max_cell = document.getElementById('max_radius' + i);
                var orbital_period = parseFloat(document.getElementById('orbit_period' + i).innerHTML.split(' ')[0]);
                var name = document.getElementById('name' + i).innerHTML;

                var min_radius = parseFloat(min_cell.innerHTML).toFixed(3);
                var max_radius = parseFloat(max_cell.innerHTML).toFixed(3);

                toDraw.push({max: max_radius / 2, min: min_radius / 2, orbital_period: orbital_period, velocity: 0, position: 0, name: name});
                max_size = max_radius > max_size ? max_radius : max_size;
                min_size = min_radius < min_size ? min_radius : min_size;
            }
        }

        // Scale everything so that the largest orbit is 600px across.
        sweet_spot_scale = 600 / max_size;
        default_zoom = sweet_spot_scale;

        // This would scale the graphic so that the smallest radius is 20px across, and more nicely visible. Results in HUGE outer orbits.
        /*if ((min_size * sweet_spot_scale) < 20){
            console.log(min_size * sweet_spot_scale);
            sweet_spot_scale = 20 / min_size;
            console.log(min_size * sweet_spot_scale);
        }*/

        var context = canvas.getContext("2d");
        var centerX = canvas.width / 2;
        var centerY = canvas.height / 2;

        document.getElementById('diagram-legend').innerHTML = "1px ~ " + (1 / sweet_spot_scale).toFixed(4) + " AU" ;
        document.getElementById('diagram-legend').innerHTML = document.getElementById('diagram-legend').innerHTML +
                "<br/> Orbital bodies are always drawn with a radius of 3px.";

        // We immediately draw the first frame of the animation, no delay.
        animate_solar_system(toDraw, star_letter, context, canvas, centerX, centerY);
        // Every 40ms, repaint the solar system. 24fps requires a frame every 41.666666ms, so we run slightly faster than that.
        window.setInterval(animate_solar_system, 40, toDraw, star_letter, context, canvas, centerX, centerY);
    }
};

// beginPath starts a new Path that can then be drawn with stroke