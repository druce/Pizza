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

    $.getJSON('http://54.224.21.240:8181?', function(data) {
	window.mydata = data;
    });
    
})
