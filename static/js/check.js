$(window).bind('pageshow', function(event) {
    if (event.originalEvent.persisted) {
		window.location.reload();
    }
});

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