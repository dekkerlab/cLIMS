$(function() {
	$('.jsonForm select').on('change', function() {
	  var jsonObjPK = this.value;
	  $.ajax({
		    url: "/constructForm/",
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
//		    	$("."+model).empty();
//		    	$("."+model).append( form );
		    	$(".inner").empty();
		    	$(".inner").append( form );
		    	var valuesJson = eval('(' +$( "#jsonForm").val() + ')');
				for (var k in valuesJson) {
					$( "select[name='"+k+"']" ).val(""+valuesJson[k]+"");
					$( "input[name='"+k+"']" ).val(""+valuesJson[k]+"");
				}
				
		    },
		    error: function(ts) { 
                alert("Incorrect Choice");
            }
		});
});
	
	function constructForm(jsObj) {
		form = ""
		for (var key in jsObj) {
			form +=  "<a style='cursor: pointer;'><i class='fa fa-question-circle' title='"+jsObj[key].help+"'></i></a>"
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
	
	$( "span:contains('Biosample modification')" ).append('<a href="/addModification/" title="Add another Modification"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	$( "span:contains('protocol ')" ).append('<a href="/addProtocol/" target="_blank" title="Add another Protocol"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	$( "span:contains('document')" ).append('<a href="/addDocument/" target="_blank" title="Add another Document"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	$( "span:contains('Documents')" ).append('<a href="/addDocument/" target="_blank" title="Add another Document"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	$( "span:contains('References')" ).append('<a href="/addPublication/" target="_blank" title="Add another Publication"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	$( "span:contains('constructs')" ).append('<a href="/addConstruct/" target="_blank" title="Add another Construct"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	$( "span:contains('target')" ).append('<a href="/addTarget/" target="_blank" title="Add another Target"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	
	
	$( ".jsonForm select" ).change();
	
	
	if ( $( ".jsonAnalysis" ).length ) {
		var jsonObjPK = $( ".jsonAnalysis select" ).val();
		console.log(jsonObjPK)
		  $.ajax({
			    url: "/constructForm/",
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
//			    	$("."+model).empty();
//			    	$("."+model).append( form );
			    	$(".inner").empty();
			    	$(".inner").append( form );
			    	var valuesJson = eval('(' +$( "#jsonForm").val() + ')');
					for (var k in valuesJson) {
						$( "select[name='"+k+"']" ).val(""+valuesJson[k]+"");
						$( "input[name='"+k+"']" ).val(""+valuesJson[k]+"");
					}
					
			    },
			    error: function(ts) { 
	                alert("Incorrect Choice");
	            }
			});
		
	}
	
		
});