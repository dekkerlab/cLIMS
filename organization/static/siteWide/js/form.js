$(function() {
	$('.jsonForm select').on('change', function() {
		$(".inner").empty();
	  var jsonObjPK = this.value;
	  $.ajax({
		    url: "constructForm/",
		    type: "POST",
		    data: { 
                'pk': jsonObjPK,
            }, 
		    cache:false,
		    dataType: "json",
		    success: function(obj){
		    	jsObj = obj.field_set
		    	form = constructForm(jsObj)
		    	$( ".inner" ).append( form );
		    },
		    error: function(ts) { 
                alert("error");
            }
		});
});
	function constructForm(jsObj) {
		form = ""
		for (var key in jsObj) {
    		 form += "<label>"+key+"</label>";
    		 text = jsObj[key].data;
    		 if (text == "choices"){
    			 choices = jsObj[key].choices;
    			 len = Object.keys(choices).length;
    			 form += "<select name='select'>";
    			 for (i = 1; i <= len; i++) {
    				 optionValue = jsObj[key].choices[i]
    				 form += "<option value="+optionValue+">"+optionValue+"</option>";
    			 }
    			 form += "</select>";
    		 }
    		 else {
    			 form += "<input maxlength='200' name="+key+" type='text'>"
    		 }
    		}
	    return form;
	}
});