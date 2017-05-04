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
		    	var valuesJson = eval('(' + $( "#jsonForm").val() + ')');
		    	//console.log(valuesJson);
				for (var k in valuesJson) {
					$( "select[name='"+k+"']" ).val(""+valuesJson[k]+"");
					$( "input[name='"+k+"']" ).val(""+valuesJson[k]+"");
				}
				
		    },
		    error: function(ts) { 
               
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
    			 if(jsObj[key].required == "yes"){
        			 form += "class='makeRequire' >";
        		 }
        		 else{
        			 form += ">";
        		 }
    			 for (i = 1; i <= len; i++) {
    				 optionValue = jsObj[key].choices[i]
    				 form += "<option value='"+optionValue+"'>"+optionValue+"</option>";
    			 }
    			 form += "</select>";
    		 }
    		 else {
    			 if(jsObj[key].data  == "float"){
    				 form += "<input maxlength='500' name="+key+" type=number step=0.01 " ;
    			 }
    			 else{
    				 form += "<input maxlength='500' name="+key+" type='"+jsObj[key].data+"'"
    			 }
    			 if(jsObj[key].required == "yes"){
        			 form += "class='makeRequire' >";
        		 }
        		 else{
        			 form += ">";
        		 }
    		 }
    		 
    		}
	    return form;
	}
	
	
//	$( "span:contains('Biosample modification')" ).append('<a href="/addModification/" title="Add another Modification"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('protocol ')" ).append('<a href="/addProtocol/" target="_blank" title="Add another Protocol"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('document')" ).append('<a href="/addDocument/" target="_blank" title="Add another Document"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('Documents')" ).append('<a href="/addDocument/" target="_blank" title="Add another Document"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('References')" ).append('<a href="/addPublication/" target="_blank" title="Add another Publication"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('constructs')" ).append('<a href="/addConstruct/" target="_blank" title="Add another Construct"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('target')" ).append('<a href="/addTarget/" target="_blank" title="Add another Target"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('imageObjects')" ).append('<a href="/addImageObjects/" target="_blank" title="Add another Image"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	
	$( ".formLabel:contains('Document')" ).append('<a href="/addDocument/" class="add-another" id="add_id_document" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('References')" ).append('<a href="/addPublication/" class="add-another" id="add_id_references" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Protocol')" ).append('<a href="/addProtocol/" class="add-another" id="add_id_protocol" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Biosource SOP cell line')" ).append('<a href="/addProtocol/" class="add-another" id="add_id_protocol" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Growth protocol')" ).append('<a href="/addProtocol/" class="add-another" id="add_id_protocol" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('4DN SOP protocol')" ).append('<a href="/addProtocol/" class="add-another" id="add_id_protocol" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Modifications')" ).append('<a href="/addModification/" class="add-another" id="add_id_modifications" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('constructs')" ).append('<a href="/addConstruct/" class="add-another" id="add_id_constructs" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Treatmentrnai target')" ).append('<a href="/addTarget/" class="add-another" id="add_id_treatmentRnai_target" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Targeted region')" ).append('<a href="/addGenomicRegions/" class="add-another" id="add_id_targeted_region" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Imageobjects')" ).append('<a href="/addImageObjects/" class="add-another" id="add_id_imageObjects" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('treatmentrnai')" ).append('<a href="/addTreatmentRnai/" class="add-another" id="add_id_biosample_TreatmentRnai" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('treatmentchemical')" ).append('<a href="/addTreatmentChemical/" class="add-another" id="add_id_biosample_TreatmentChemical" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('othertreatment')" ).append('<a href="/addOther/" class="add-another" id="add_id_biosample_OtherTreatment" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('File barcode')" ).append('<a href="/addBarcode/" class="add-another" id="add_id_file_barcode" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Construct Map')" ).append('<a href="/addDocument/" class="add-another" id="add_id_document" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('File format specifications')" ).append('<a href="/addDocument/" class="add-another" id="add_id_file_format_specifications" onclick="return showAddAnotherPopup(this);"></a>');
	$( "input[name*='date']" ).attr({'type':'date'});
	
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
//	                alert("Incorrect Choice");
	            }
			});
		
	}
	
		
});