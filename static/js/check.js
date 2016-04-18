$(function() {
    $('#check').on('submit', function(e) {
		$('body').find('#submit-button').fadeOut(500, function() {
        $('body').find('#submit-button').html('<i class="fa fa-circle-o-notch fa-spin fa-fw margin-bottom"></i>').fadeIn(500);
    });
		
		
    });
});