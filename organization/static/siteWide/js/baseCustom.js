 jQuery(document).ready(function ($) {
	var sessionValue= $("#hdnSession").val();
	if(sessionValue=="True"){
		$(".view_only").hide();
	}
});