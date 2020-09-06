function set_bg() {
    // set background based on dropdown value and resize to match screen dimensions
    // this is messed up on vertical phones, maybe should pick from multiple backgrounds based on aspect ratio
    $('.overlay').height($(window).height());
    key_val = $('#keyword_button').text().toLowerCase().replace(/\s/g, "");
    key_val = key_val == "keyword" ? 'pizza' : key_val;
    key_val = key_val == "" ? 'pizza' : key_val;
    bgprop = "url('images/" + key_val + ".jpg')"
    $("body").css("background-image", bgprop);
    // $("body").css("background-size", "cover");
    $("body").css("background-position", "left top");
    $("body").css("background-size", window.innerWidth + "px " + window.innerHeight + "px");
    $('.overlay').height(Math.max($("body").height(), window.innerHeight));
    $('.overlay').width(Math.max($("body").width(), window.innerWidth));
}

function set_hovers() {
    // set hover function on each data row
    // highlight row, popup on map 
    $('#output_table > tbody > tr').hover(
        function () {
            $(this).addClass('font-weight-bold');
            id = $(this).find('td').first().text() - 1;
            document.markers[id].openPopup()
        },
        function () {
            $(this).removeClass('font-weight-bold');
            id = $(this).find('td').first().text() - 1;
            document.markers[id].closePopup()
        }
    );
}

function markerFunction(id) {
    // popup based on title. given marker title, loop through all markers and popup specified 
    for (var i in document.markers) {
        var marker = document.markers[i];
        var markerID = marker.options.title;
        if (markerID == id){
            marker.openPopup();
            break;
        };
    }
}

function searchClick() {

    key_val = $('#keyword_input').val();
    lat_val = $('#latitude_input').val();
    lng_val = $('#longitude_input').val();

    new_url = "http://" + document.pizza_url + "/query?lat=" + lat_val + "&lng=" + lng_val + "&keyword=" + key_val;

    if (!$.fn.DataTable.isDataTable('#output_table')) {  // first call, create table
        $("#output_table").html('                <thead> \
                    <tr style="text-align: right;"> \
                        <th>Rank</th> \
                        <th>Name</th> \
                        <th>Address</th> \
                        <th>Distance</th> \
                        <th><i class="fab fa-google fa-lg gmaps_cl"> </i> Google</th> \
                        <th><i class="fab fa-yelp fa-lg yelp_cl"> </i> Yelp</th> \
                        <th><i class="fab fa-foursquare fa-lg foursquare_cl"> </i> Foursquare</th> \
                    </tr> \
                </thead> \
                ');
        document.pizza_data_table = $('#output_table').DataTable({
            "searching": false,
            "lengthChange": false,
            "paging": false,
            "info": false,
            "columns": [
                { "data": "Rank", "orderable": true },
                { "data": "Name", "orderable": true },
                { "data": "Address", "orderable": true },
                { "data": "Distance", "orderable": true, "className": "text-right" },
                { "data": "Google Maps", "orderable": true, "className": "text-right" },
                { "data": "Yelp", "orderable": true, "className": "text-right" },
                { "data": "Foursquare", "orderable": true, "className": "text-right" }
            ]
        });

        $.get(new_url, function (data) {
            // show data for debug
            // for (var i = 0, len = data.length; i < len; i++) {
            //     console.log(data[i]);
            // }
            document.pizza_data_table.clear();
            document.pizza_data_table.rows.add(data);
            document.pizza_data_table.draw();
            set_bg();
            set_hovers();    
            getMap(lat_val, lng_val, data);
        });
    }
    else {
        $.get(new_url, function (data) {
            document.pizza_data_table.clear();
            document.pizza_data_table.rows.add(data);
            document.pizza_data_table.draw();
            set_bg();
            set_hovers();    
            getMap(lat_val, lng_val, data);
        });
    }
}

function getMap(lat_val, lng_val, data) {
    coords = [Number(lat_val), Number(lng_val)]

    $("#leaflet_map").css("height", "384px");
    // location_val = $('#location_button').text().toLowerCase().replace(/\s/g, "");
    var accessToken = 'pk.eyJ1IjoiZHJ1Y2V2IiwiYSI6ImNqbWt4YmJ6ejAyYXcza3A1djhya254ZXMifQ.ZkDU7jNP3QGicJpGRRMF2Q';
    if (document.hasOwnProperty('mymap')) {
        document.mymap.remove()
    }
    document.mymap = L.map('leaflet_map').setView(coords, 14);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: accessToken
    }).addTo(document.mymap);

    // origin of search
    L.marker(coords).addTo(document.mymap).bindPopup("Search location");

    document.markers =  [];
    for (var i = 0, len = data.length; i < len; i++) {
        // console.log(data[i]);
        rating_html = '';
        if (data[i]['Google Maps'] != null) {
            rating_html += "<dt>Google rating</dt><dd>" + data[i]['Google Maps'] + " (" + data[i]['Gratings'] + " ratings)</dd> ";
        }
        if (data[i]['Yelp'] != null) {
            rating_html += "<dt>Yelp rating</dt><dd>" + data[i]['Yelp'] + " (" + data[i]['Yratings'] + " ratings)</dd> ";
        }
        if (data[i]['Foursquare'] != null) {
            rating_html += "<dt>Foursquare rating</dt><dd>" + data[i]['Foursquare'] + " (" + data[i]['Fratings'] + " ratings)</dd> ";
        }
        
        popup_html = " \
<dl> \
<dt>Rank: " + data[i].Rank + "</dt><dd></dd> \
<dt>Name</dt><dd>" + data[i].Name + "</dd> \
<dt>Address</dt><dd>" + data[i].Address + "</dd> \
<dt>Distance</dt><dd>" + data[i].Distance + "</dd> \
" + rating_html + " \
</dl> \
"
        var marker = L.marker([data[i].Lat,  data[i].Lng], {title:"marker_"+i}).addTo(document.mymap).bindPopup(popup_html);
        marker._icon.classList.add("huechange");
        marker.on('mouseover',function(ev) {
            this.openPopup();
        });
        marker.on('mouseout',function(ev) {
            this.closePopup();
        });
        document.markers.push(marker);
    }
}

$(document).ready(function () {
    //document.pizza_url = '3.231.21.40:8181';
    document.pizza_url = 'localhost:8181';
    set_bg();

    document.locations = {
        "midtown": { 'pretty_name': 'Midtown', coords: [40.7484, -73.9857] },
        "downtown": { 'pretty_name': 'Downtown', coords: [40.7077443,-74.0139089] },
        "uppereastside": { 'pretty_name': 'Upper East Side', coords: [40.7711473,-73.9661166] },
        "upperwestside": { 'pretty_name': 'Upper West Side', coords: [40.778794,-73.984257] },
        "brooklynheights": { 'pretty_name': 'Brooklyn Heights', coords: [40.6915812,-73.9954095] },
        "grandarmyplaza": { 'pretty_name': 'Grand Army Plaza', coords: [40.671872,-73.972544] },
        "bayridge": { 'pretty_name': 'Bay Ridge', coords: [40.6292633,-74.0309554] },
        "williamsburg": { 'pretty_name': 'Williamsburg', coords: [40.7144609,-73.9553373] },
    }

    for (var property in document.locations) {
        if (document.locations.hasOwnProperty(property)) {
            $("#" + property).button().click(function () {
                $("#location_button").text($(this).text());
            })
        }
    }

    $("#pizza_action").button().click(function () {
        $("#keyword_button").text($(this).text());
        $("#page_title").text("Pizza…Pizza…Pizza");
        set_bg();
    });

    $("#coffee_action").button().click(function () {
        $("#keyword_button").text($(this).text())
        $("#page_title").text("Coffee…Coffee…Coffee");
        set_bg();
    });

    $("#icecream_action").button().click(function () {
        $("#keyword_button").text($(this).text())
        $("#page_title").text("Ice Cream…Ice Cream…Ice Cream");
        set_bg();
    });

    $("#search_button").click(searchClick);

});

function getData() {
    // get data explicitly into an array
    // not used, we just use native datatables, set contents from json
    // console.log('getdata 1');
    $.ajax({
        dataType: 'json',
        url: 'http://localhost:8181',
        success: function (data) {
            console.log('aloha3');
            console.log(data.length);
            outstr = "";
            for (var i = 0, len = data.length; i < len; i++) {
                console.log(data[i]);
                outstr += (i + 1 + "," + data[i].Name + "," + data[i].Address + "," + data[i]['Google Maps'] + "," + data[i]['Yelp'] + "," + data[i]['Foursquare']);
            }
            console.log(outstr);
        },
        error: function (data) {
            console.log('error');
            console.log(data);
        }
    });
    // console.log('getdata 2');

}
