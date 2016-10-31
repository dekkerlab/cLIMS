$(function() {
	$('.jsonForm select').on('change', function() {
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
		    	jsObj = obj.field_set;
		    	model = obj.model;
		    	form = constructForm(jsObj);
		    	$("."+model).empty();
		    	$("."+model).append( form );
		    },
		    error: function(ts) { 
                alert("Incorrect Choice");
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
    			 form += "<select name="+key+">";
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