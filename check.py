import json
import urllib2
import requests
from datetime import date, timedelta

from flask import Flask, render_template, jsonify, request
from lxml import html
from lxml import etree

app = Flask(__name__)

start_date = date(2016, 4, 7)

def get_custom_message(streak):
	if date.today() - timedelta(days=streak) <= start_date:
		return 'You\'re in great shape! Keep going for %s more days (until May 6, 2016) and you\'ll get a custom Freetail shirt!' % (str((date(2016, 5, 6) - date.today()).days))
	else:
		start_day = start_date + timedelta(days=1)
		if date.today() - timedelta(days=streak) <= start_date:
			return 'Looks like you started a day late! No worries, we still want you to commit for 30 days, just commit for %s more days (until May 7, 2016) to get your custom Freetail shirt!' % (str((date(2016, 5, 7) - date.today()).days))
		else:
			return 'Our automated check isn\'t able to verify your completion towards a 30 day streak. If you believe this is a mistake, check to make sure all the repositories you committed to are public. If you still think there\'s an error, please reach out to <a href="mailto:hello@freetailhackers.com">hello@freetailhackers.com</a> so we can investigate further.'

@app.route('/')
def index():
	return render_template('index.html')

def get_streak(username, page_tree):
	current_streaks = page_tree.xpath('//*[@id="contributions-calendar"]/div[5]/span[2]/text()')
	return current_streaks

def get_commits(username, streak):
	commit_dict = {}
	
	day_streak = 0 if int(streak.split()[0]) == 0 else int(streak.split()[0]) - 1

	current_iteration_day = start_date
	end_day = date.today() + timedelta(days=1)
	while current_iteration_day != end_day:
		page = requests.get('https://github.com/users/%s/contributions' % username)
		tree = html.fromstring(page.content)
		current_commit = tree.xpath('//rect[@data-date="' + str(current_iteration_day) + '"]/@data-count')
		if current_commit:
			commit_dict[str(current_iteration_day)] = current_commit[0]
		current_iteration_day += timedelta(days=1)
	
	commit_keys = commit_dict.keys()
	commit_keys.sort()
	return commit_keys, commit_dict

@app.route('/results', endpoint='get-results', methods=['POST'])
def get_results():
	username = request.form['username']
	return get_info(username)

@app.route('/<username>')
def get_info(username):
	page = requests.get('https://github.com/'  + username)
	if page.status_code != 200:
		return render_template('404.html')
	page_tree = html.fromstring(page.content)
	streak = get_streak(username, page_tree)[0]
	commit_keys, commit_dict = get_commits(username, streak)
	message = get_custom_message(int(streak.split()[0]))
	return render_template('results.html', streak=streak, commits=commit_dict, keys=commit_keys, message=message)

if __name__ == '__main__':
	app.run(debug=True)
