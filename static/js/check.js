$(function() {
    $('#check').on('submit', function(e) {
		$('body').find('#submit-button').addClass('submitted');
		$('body').find('#submit-button').html('<div class="loader">Loading...</div>');
    });
});
