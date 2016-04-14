$(document).ready(function() {
	var githubUrl = "https://www.github.com/";
	var apiPrefix = "https://api.github.com/users/";
	var apiSuffix = "/events/public";
	function displayStreak(username) {
		$.get(githubUrl + username, function(data) {
			var div = $('<div>');
			div.html(data);
			var streak = div.find('.contrib-number').last().text();
			$('#box').addClass('generated-row');
			$('caption').text("Your GitHub streak is " + streak + ".");
			function addRow(text1, text2) {
				console.log("Should be adding row with " + text1 + " " + text2);
				$row = $('<tr></tr>');
				$row.append($('<td class="date-cell"></td>').text(text1));
				$row.append($('<td class="commit-box"><ul></ul></td>').text(text2));
				$('tbody').append($row);
			}
			function formatDate(date) {
				return date.getMonth() + 1 + "/" + date.getDate();
			}
			addRow('Date', 'Commits');
			var start = new Date(2016, 3, 7);
			for (var date = new Date(); date > start; date.setDate(date.getDate() - 1)) {
				addRow(formatDate(date), '');
			}
			$.ajax(apiPrefix + username + apiSuffix, {
				accepts: {
					json: 'application/vnd.github.v3+json'
				},
				crossDomain: true,
				dataType: 'json',
				success: function(data) {
					data.some(function(ev) {
						var created_at = new Date(ev.created_at);
						console.log(created_at);
						if (created_at < new Date(2016, 3, 7)) {
							return true;
						}
						if (ev.type === "PushEvent" || ev.type === "CreateEvent" && ev.payload.ref === ev.payload.master_branch) {
							var dateText = formatDate(created_at);
							var commitText = ev.type === 'PushEvent' ? "pushed to master at" : "created repository";
							commitText = "<li>" + username + " " + commitText + " " + ev.repo.name + ".</li>";
							$('.date-cell:contains(' + dateText + ')').next().append(commitText);
						}
						return false;
					});
				}
			});
		});
	}

	$('.btn-lg').click(function() {
		username = $('.form-control').val().trim();
		displayStreak(username);
	});
});
