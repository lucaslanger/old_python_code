console.log('Hello')

$(document).ready(function() {

	$('div.section_button').mouseenter(function() {
		$(this).css('background-color','pink');
	});
	$('div.section_button').mouseleave(function() {
		$(this).css('background-color','#FFDDBB'); 
	});
});