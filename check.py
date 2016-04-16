import json
import urllib2
import requests
import datetime

from flask import Flask, render_template, jsonify, request
from lxml import html
from lxml import etree

app = Flask(__name__)
#host = os.environ.get('HOST')
host = 'http://127.0.0.1:5000'

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

	current_iteration_day = datetime.date.today() - datetime.timedelta(days=day_streak)
	end_day = datetime.date.today() + datetime.timedelta(days=1)
	while current_iteration_day != end_day:
		current_commit = page_tree.xpath('//rect[@data-date="' + str(current_iteration_day) + '"]/@data-count')
		if current_commit:
			commit_dict[str(current_iteration_day)] = current_commit[0]
		current_iteration_day += datetime.timedelta(days=1)
		
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

	return render_template('results.html', streak=streak, commits=commit_dict, keys=commit_keys)

@app.route('/github/<github_username>')
def github_content(github_username):
	return requests.get('https://github.com/'+github_username).content

@app.route('/api/<github_username>')
def github_username(github_username):
	activity = getGitHubActivity(github_username)
	return jsonify(results=activity)

if __name__ == '__main__':
	app.run(debug=True)
