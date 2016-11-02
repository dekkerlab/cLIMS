$(document).ready(function(){
	
    $(".divison").hover(function(){
        $(this).css("background-color", "yellow");
        }, function(){
        $(this).css("background-color", "pink");
    });
    
    $(".edit").click(function(){
    	$('.show').toggleClass("hidden");
    	if ($(this).text() == "Edit")
    	       $(this).text("Done")
    	    else
    	       $(this).text("Edit");
    });
    
    $(".del").click(function(){
    	$('.show').toggleClass("hidden");
    	if ($(this).text() == "Delete")
    	       $(this).text("Done")
    	    else
    	       $(this).text("Delete");
    });
    
    $(".combine").click(function(){
    	$('.show').toggleClass("hidden");
    });
    
    $('.combination').change(function() {
    	var checkedVals = $('.combination:checkbox:checked').map(function() {
    	    return this.value;
    	}).get();
    	lenCheck = checkedVals.length;
    	if(lenCheck>1){
    		$('.add').removeClass('disabled');
    	}
    	else{
    		$('.add').addClass('disabled');
    	}
    });
    
    $(".add").click(function(){
    	var checkedVals = $('.combination:checkbox:checked').map(function() {
    	    return this.value;
    	}).get();
    	joinedVals = checkedVals.join(",");
    	window.location.href = "/combineSamples/"+joinedVals;
    });
    
//	$(".divison").mouseover(function(){
//	    $(".divison").css("background-color", "red");
//	});
//    $(".divison").mouseout(function(){
//        $(".divison").css("background-color", "lightgray");
//    });
//    

        $('[data-toggle="tooltip"]').tooltip();
    
        
    
});
