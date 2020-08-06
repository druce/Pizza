$(document).ready(function(){
    $('.header').height($(window).height());

    locations = {
        "midtown": {'pretty_name': 'Midtown', coords: '40.7484, -73.9857'},
        "downtown": {'pretty_name': 'Downtown', coords: '40.7077443,-74.0139089'},
        "uppereastside": {'pretty_name': 'Upper East Side', coords: '40.7711473,-73.9661166'},
        "upperwestside": {'pretty_name': 'Upper West Side', coords: '40.778794,-73.984257'},
        "brooklynheights": {'pretty_name': 'Brooklyn Heights', coords: '40.6915812,-73.9954095'},
        "grandarmyplaza": {'pretty_name': 'Grand Army Plaza', coords: '40.671872,-73.972544'},
        "bayridge": {'pretty_name': 'Bay Ridge', coords: '40.624468,-74.0487134'},
        "williamsburg": {'pretty_name': 'Williamsburg', coords: '40.7144609,-73.9553373'},
    }
    
    for (var property in locations) {
        if (locations.hasOwnProperty(property)) {
            $("#" + property).button().click(function(){
                $("#location_button").text($(this).text())
            })
        }
      }

    $("#pizza_action").button().click(function(){
        $("#keyword_button").text($(this).text());
        $("#header").css("background-image", "url('images/pizza.jpg')");
    })

    $("#coffee_action").button().click(function(){
        $("#keyword_button").text($(this).text())
        $("#header").css("background-image", "url('images/coffee.jpg')");
    })

    $.ajax({
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
