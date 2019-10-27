$(function() {
    var my_num = 0;

    function poll(){
	//long polling function.  wait for response, update number, then poll again
	console.log("polling...")
	$.ajax({
	    method: "GET",
	    url: "/dice",
	    data: { "number": my_num }
	})
	    .done(function(data) {
		console.log(data);
		$("#dice").html(data.number);
		my_num = data.number;
		poll();
	    });
    }

    $("#dice").click(function() {
	$.ajax({
	    method: "POST",
	    url: "/dice",
	});
    });
    
    poll();
	    
});
