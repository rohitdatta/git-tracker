import json
import urllib2
import requests

from flask import Flask, render_template, jsonify

app = Flask(__name__)
#host = os.environ.get('HOST')
host = 'http://127.0.0.1:5000'

def getGitHubActivity(github_username):
	return json.load(urllib2.urlopen('https://api.github.com/users/'+github_username+'/events/public'))

@app.route('/')
def index():
	return render_template('index.html', host=host)

@app.route('/github/<github_username>')
def github_content(github_username):
	return requests.get('https://github.com/'+github_username).content

@app.route('/api/<github_username>')
def github_username(github_username):
	activity = getGitHubActivity(github_username)
	return jsonify(results=activity)

if __name__ == '__main__':
	app.run(debug=True)
