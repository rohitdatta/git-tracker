$(function() {
    $('#check').on('submit', function(e) {
		if(!$('input[name="username"]').val()) {
			sweetAlert('Empty Username', 'Please enter your GitHub username', 'error');
			e.preventDefault();
		} else {
			$('body').find('#submit-button').addClass('submitted');
			$('body').find('#submit-button').html('<div class="loader">Loading...</div>');
		}
    });
});

$(window).bind('beforeunload', function(){
	if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1) {
		$('body').find('#submit-button').removeClass('submitted');
		$('body').find('#submit-button').html('Check');
	}
});