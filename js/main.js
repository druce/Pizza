document.pizza_url = 'localhost:8181';

function set_bg() {
    // background resized to match screen dimensions
    // this is messed up on vertical phones, maybe should pick from multiple backgrounds based on aspect ratio
    $('.overlay').height($(window).height());
    key_val = $('#keyword_button').text().toLowerCase().replace(/\s/g, "");
    key_val = key_val == "keyword" ? 'pizza' : key_val;
    bgprop = "url('images/" + key_val + ".jpg')"
    $("body").css("background-image", bgprop);
    // $("body").css("background-size", "cover");
    $("body").css("background-position", "left top");
    $("body").css("background-size", window.innerWidth + "px " + window.innerHeight + "px");
    $('.overlay').height(Math.max($("body").height(), window.innerHeight));
    $('.overlay').width(Math.max($("body").width(), window.innerWidth));

}

function getData() {
    // get data explicitly into an array
    // works but not used
    // build url with params
    // first write to console
    // then update the table

    // console.log('aloha');
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
    // console.log('aloha 2');

}
function searchClick() {

    key_val = $('#keyword_button').text().toLowerCase();
    key_val = key_val.replace(/\s/g, "");
    location_val = $('#location_button').text().toLowerCase();
    location_val = location_val.replace(/\s/g, "");

    if (key_val == 'keyword') {
        alert('Choose a search keyword from the keywords dropdown');
    }
    else if (location_val == 'location') {
        alert('Choose a location from the locations dropdown');
    }
    else {
        new_url = "http://" + document.pizza_url + "/query?location=" + location_val + "&keyword=" + key_val
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
                document.pizza_data_table.clear();
                document.pizza_data_table.rows.add(data);
                document.pizza_data_table.draw();
                set_bg();
            });
        }
        else {
            $.get(new_url, function (data) {
                document.pizza_data_table.clear();
                document.pizza_data_table.rows.add(data);
                document.pizza_data_table.draw();
                set_bg();
            });
        }
    }
}

$(document).ready(function () {
    set_bg();

    locations = {
        "midtown": { 'pretty_name': 'Midtown', coords: '40.7484, -73.9857' },
        "downtown": { 'pretty_name': 'Downtown', coords: '40.7077443,-74.0139089' },
        "uppereastside": { 'pretty_name': 'Upper East Side', coords: '40.7711473,-73.9661166' },
        "upperwestside": { 'pretty_name': 'Upper West Side', coords: '40.778794,-73.984257' },
        "brooklynheights": { 'pretty_name': 'Brooklyn Heights', coords: '40.6915812,-73.9954095' },
        "grandarmyplaza": { 'pretty_name': 'Grand Army Plaza', coords: '40.671872,-73.972544' },
        "bayridge": { 'pretty_name': 'Bay Ridge', coords: '40.6292633,-74.0309554' },
        "williamsburg": { 'pretty_name': 'Williamsburg', coords: '40.7144609,-73.9553373' },
    }

    for (var property in locations) {
        if (locations.hasOwnProperty(property)) {
            $("#" + property).button().click(function () {
                $("#location_button").text($(this).text());
            })
        }
    }

    $("#pizza_action").button().click(function () {
        $("#keyword_button").text($(this).text());
        $("#page_title").text("Pizza Pizza Pizza");
        set_bg();
    });

    $("#coffee_action").button().click(function () {
        $("#keyword_button").text($(this).text())
        $("#page_title").text("Coffee Coffee Coffee");
        set_bg();
    });

    $("#search_button").click(searchClick);
});

/*    $.ajax({
	dataType: 'json',
	url: 'http://localhost:8181',
	success: function(data) {
	    outstr = "";
	    for ( var i=0, len=data.length; i<len; i++ ) {
		outstr += (i+1 + "," + data[i].name + "," + data[i].address + "," + data[i].gmaps_rating + "," + data[i].yelp_rating + "," + data[i].foursquare_rating);
	    }
	    $("#results").html(outstr);
	},
	error: function(data) {
	    console.log('error');
	    console.log(data);
	}
    });
})
*/
