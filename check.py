import json
import urllib2

from flask import Flask, render_template, jsonify

app = Flask(__name__)


def getGitHubActivity(github_username):
	return json.load(urllib2.urlopen('https://api.github.com/users/'+github_username+'/events/public'))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<github_username>')
def github_username(github_username):
	activity = getGitHubActivity(github_username)
	return jsonify(results=activity)

if __name__ == '__main__':
	app.run(debug=True)
