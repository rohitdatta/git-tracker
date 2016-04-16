import json
import urllib2
import requests
from datetime import date, timedelta

from flask import Flask, render_template, jsonify, request
from lxml import html
from lxml import etree

app = Flask(__name__)
#host = os.environ.get('HOST')
host = 'http://127.0.0.1:5000'

def get_custom_message(streak):
	start_day = date(2016, 4, 7)
	if date.today() - timedelta(days=streak) <= start_day:
		return 'You\'re in great shape! Keep going for %s more days (until May 6, 2016) and you\'ll get a custom Freetail shirt!' % (str((date(2016, 5, 6) - date.today()).days))
	else:
		start_day = start_day + timedelta(days=1)
		if date.today() - timedelta(days=streak) <= start_day:
			return 'Looks like you started a day late! No worries, we still want you to commit for 30 days, just commit for %s more days (until May 7, 2016) to get your custom Freetail shirt!' % (str((date(2016, 5, 7) - date.today()).days))
		else:
			return 'Our automated check isn\'t able to verify your completion towards a 30 day streak. If you believe this is a mistake, check to make sure all the repositories you committed to are public. If you still think there\'s an error, please reach out to <a href="mailto:hello@freetailhackers.com">hello@freetailhackers.com</a> so we can investigate further.'

def getGitHubActivity(github_username):
	return json.load(urllib2.urlopen('https://api.github.com/users/'+github_username+'/events/public'))

@app.route('/')
def index():
#	if request.method == 'POST':
#		return get_info(username)
	return render_template('index.html', host=host)

def get_streak(username, page_tree):
	current_streaks = page_tree.xpath('//*[@id="contributions-calendar"]/div[5]/span[2]/text()')
	return current_streaks

def get_commits(username, page_tree):
	commit_dict = {}
	streak = get_streak(username, page_tree)[0]
	
	day_streak = 0 if int(streak.split()[0]) == 0 else int(streak.split()[0]) - 1

	current_iteration_day = date.today() - timedelta(days=day_streak)
	end_day = date.today() + timedelta(days=1)
	while current_iteration_day != end_day:
		current_commit = page_tree.xpath('//rect[@data-date="' + str(current_iteration_day) + '"]/@data-count')
		if current_commit:
			commit_dict[str(current_iteration_day)] = current_commit[0]
		current_iteration_day += timedelta(days=1)
		
	commit_keys = commit_dict.keys()
	commit_keys.sort()
	return commit_keys, commit_dict, day_streak

@app.route('/results', endpoint='get-results', methods=['POST'])
def get_results():
	username = request.form['username']
	return get_info(username)

@app.route('/<username>')
def get_info(username):
	page = requests.get('https://github.com/'  + username)
	if page.status_code == 400:
		return render_template('404.html')
	page_tree = html.fromstring(page.content)

	commit_keys, commit_dict, streak = get_commits(username, page_tree)
	message = get_custom_message(streak)
	return render_template('results.html', streak=streak, commits=commit_dict, keys=commit_keys, message=message)

@app.route('/github/<github_username>')
def github_content(github_username):
	return requests.get('https://github.com/'+github_username).content

@app.route('/api/<github_username>')
def github_username(github_username):
	activity = getGitHubActivity(github_username)
	return jsonify(results=activity)

if __name__ == '__main__':
	app.run(debug=True)
