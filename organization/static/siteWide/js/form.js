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
		    	if($('#oldForm').is(':checked')){
					$(".makeRequire").prop('required',false);
				}
				if($('#newForm').is(':checked')){
					$(".makeRequire").prop('required',true);
				}
//		    	var valuesJson = eval('(' + $( "#jso").val() + ')');
//		    	console.log(valuesJson);
//				for (var k in valuesJson) {
//					$( "select[name='"+k+"']" ).val("'"+valuesJson[k]+"'");
//					$( "input[name='"+k+"']" ).val("'"+valuesJson[k]+"'");
//				}
				
		    },
		    error: function(ts) { 
               console.log("No value selected in JsonObjectField")
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
    				 form += "<input maxlength='200' name="+key+" type=number step=0.01 " ;
    			 }
    			 else{
    				 form += "<input maxlength='200' name="+key+" type='"+jsObj[key].data+"'"
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
	
	
	
	
	 
	//$( "span:contains('Biosample modification')" ).append('<a href="/addModification/" title="Add another Modification"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	//$( "span:contains('protocol ')" ).append('<a href="/addProtocol/" target="_blank" title="Add another Protocol"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	//$( "span:contains('document')" ).append('<a href="/addDocument/" target="_blank" title="Add another Document"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	
	//$( "span:contains('Document')" ).append('<a id="document_modal" class=\'btn\' href=\'/addDocument/\'>Display modal </a>');
	
	//$( "span:contains('Documents')" ).append('<a href="/addDocument/" target="_blank" title="Add another Document"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	//$( ".formLabel:contains('Documents')" ).append('<a href="/addDocument/" class="add-another" id="add_id_documents" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Document')" ).append('<a href="/addDocument/" class="add-another" id="add_id_document" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('References')" ).append('<a href="/addPublication/" class="add-another" id="add_id_references" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Protocol')" ).append('<a href="/addProtocol/" class="add-another" id="add_id_protocol" onclick="return showAddAnotherPopup(this);"></a>');
	$( ".formLabel:contains('Biosource SOP cell line')" ).append('<a href="/addProtocol/" class="add-another" id="add_id_protocol" onclick="return showAddAnotherPopup(this);"></a>');
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
	
	//if (window.location.href.indexOf("/addBiosample/") > -1) {
		$( ".jsonForm select" ).change();
		
		
	//}
	
	//$( "span:contains('References')" ).append('<a href="/addPublication/" target="_blank" title="Add another Publication"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('constructs')" ).append('<a href="/addConstruct/" target="_blank" title="Add another Construct"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('target')" ).append('<a href="/addTarget/" target="_blank" title="Add another Target"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('imageObjects')" ).append('<a href="/addImageObjects/" target="_blank" title="Add another Image"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('TreatmentRnai')" ).append('<a href="/addTreatmentRnai/" target="_blank" title="Add another TreatmentRnai"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('TreatmentChemical')" ).append('<a href="/addTreatmentChemical/" target="_blank" title="Add another TreatmentChemical"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
//	$( "span:contains('OtherTreatment ')" ).append('<a href="/addOther/" target="_blank" title="Add another Other Treatment"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>');
	
//	
//	$('#id_biosample_treatment').on('change', function() {
//		var selectedTreatment = $( "#id_biosample_treatment option:selected" ).text();
//		if(selectedTreatment=="Already selected TreatmentRnai"){
//			
//			$("#id_biosample_select_old_OtherTreatment").val("");
//			$("#id_biosample_select_old_TreatmentChemical").val("");
//			
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',true);
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',false);
//			$("#id_biosample_select_old_OtherTreatment").prop('required',false);
//		}
//		else if(selectedTreatment=="Already selected TreatmentChemical"){
//			
//			$("#id_biosample_select_old_OtherTreatment").val("");
//			$("#id_biosample_select_old_TreatmentRnai").val("");
//			
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',true);
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',false);
//			$("#id_biosample_select_old_OtherTreatment").prop('required',false);
//		}
//		else if(selectedTreatment=="Already selected OtherTreatment"){
//			
//			$("#id_biosample_select_old_TreatmentChemical").val("");
//			$("#id_biosample_select_old_TreatmentRnai").val("");
//			
//			$("#id_biosample_select_old_OtherTreatment").prop('required',true);
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',false);
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',false);
//		}
//		else {
//			$("#id_biosample_select_old_OtherTreatment").prop('required',false);
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',false);
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',false);
//			
//			$("#id_biosample_select_old_OtherTreatment").val("");
//			$("#id_biosample_select_old_TreatmentChemical").val("");
//			$("#id_biosample_select_old_TreatmentRnai").val("");
//		}
//			
//		
//	});
//	
//	$('#id_biosample_select_old_TreatmentRnai').on('change', function() {
//		var oldTreatment = $( "#id_biosample_select_old_TreatmentRnai option:selected" ).val();
//		if(oldTreatment){
//			$("#id_biosample_select_old_OtherTreatment").val("");
//			$("#id_biosample_select_old_TreatmentChemical").val("");
//			
//			var theText = "Already selected TreatmentRnai";
//			$("#id_biosample_treatment option:contains(" + theText + ")").attr('selected', 'selected');
//			
//			
//			$("#id_biosample_select_old_OtherTreatment").prop('required',false);
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',false);
//			
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',true);
//		}
//		
//	});
//	$('#id_biosample_select_old_OtherTreatment').on('change', function() {
//		var oldTreatment = $( "#id_biosample_select_old_OtherTreatment option:selected" ).val();
//		if(oldTreatment){
//			$("#id_biosample_select_old_TreatmentRnai").val("");
//			$("#id_biosample_select_old_TreatmentChemical").val("");
//			
//			var theText = "Already selected OtherTreatment";
//			$("#id_biosample_treatment option:contains(" + theText + ")").attr('selected', 'selected');
//			
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',false);
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',false);
//			
//			$("#id_biosample_select_old_OtherTreatment").prop('required',true);
//		}
//		
//	});
//	$('#id_biosample_select_old_TreatmentChemical').on('change', function() {
//		var oldTreatment = $( "#id_biosample_select_old_TreatmentChemical option:selected" ).val();
//		if(oldTreatment){
//			$("#id_biosample_select_old_OtherTreatment").val("");
//			$("#id_biosample_select_old_TreatmentRnai").val("");
//			
//			var theText = "Already selected TreatmentChemical";
//			$("#id_biosample_treatment option:contains(" + theText + ")").attr('selected', 'selected');
//			
//			$("#id_biosample_select_old_OtherTreatment").prop('required',false);
//			$("#id_biosample_select_old_TreatmentRnai").prop('required',false);
//			
//			$("#id_biosample_select_old_TreatmentChemical").prop('required',true);
//		}
//		
//	});
	
//	$('#indCheck').click(function() {
//	    $(".indDiv").toggleClass("hidden");
//	});
//	$('#bioCheck').click(function() {
//	    $(".bioDiv").toggleClass("hidden");
//	});
//	$('#samCheck').click(function() {
//	    $(".samDiv").toggleClass("hidden");
//	});
	
//	$("#indCheck").click(function(){
//    	$('#indDiv').toggleClass("hidden");
//	});	
});