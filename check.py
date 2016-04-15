import json
import urllib2
import requests

from flask import Flask, render_template, jsonify
from lxml import html

app = Flask(__name__)
#host = os.environ.get('HOST')
host = 'http://127.0.0.1:5000'

def getGitHubActivity(github_username):
	return json.load(urllib2.urlopen('https://api.github.com/users/'+github_username+'/events/public'))

@app.route('/')
def index():
	return render_template('index.html', host=host)

def get_streak(username):
	page = requests.get('https://github.com/'  + username)
	page_tree = html.fromstring(page.content)
	current_streaks = page_tree.xpath('//*[@id="contributions-calendar"]/div[5]/span[2]/text()')
	return current_streaks[0]

@app.route('/<username>')
def get_info(username):
	streak = get_streak(username)
#	commits = get_commits(username)
	return render_template('results.html', streak=streak)

@app.route('/github/<github_username>')
def github_content(github_username):
	return requests.get('https://github.com/'+github_username).content

@app.route('/api/<github_username>')
def github_username(github_username):
	activity = getGitHubActivity(github_username)
	return jsonify(results=activity)

if __name__ == '__main__':
	app.run(debug=False)
