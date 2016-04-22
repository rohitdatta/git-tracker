import json
import urllib2
import requests
from datetime import date, timedelta
from collections import OrderedDict
import sys

from flask import Flask, render_template, jsonify, request, redirect, url_for
from lxml import html
from lxml import etree
import pygal
from pygal.style import Style
from pygal import Config

app = Flask(__name__)

start_date = date(2016, 4, 7)

def render_chart(commit_dict):
	style = Style(
		transition='400ms ease-in',
		font_family='googlefont:Josefin+Sans',
		plot_background='transparent',
		background='transparent',
		colors=('#124E78', '#E8537A')
	)
	config = Config()
	params = {
		'show_y_guides':False,
		'show_x_guides':False,
		'y_labels_major_count':5,
		'show_minor_y_labels':False,
		'style':style,
	}
	config = pygal.Config(no_prefix=True, **params)
	chart = pygal.Line(config, height=400, x_label_rotation=20)
	chart.x_labels = commit_dict.keys()
	print commit_dict
	chart.add('Commits', [int(commit_num) for commit_num in commit_dict.values()])
	chart.title = 'Commit History from %s' % str(start_date)
	chart = chart.render()
	unicode_chart=chart.decode('utf-8')
	return unicode_chart	

def get_custom_message(streak, commit_dict):
	if date.today() - timedelta(days=streak) <= start_date:
		return 'You\'re in great shape! Keep going for %s more days (until May 6, 2016) and you\'ll get a custom Freetail shirt!' % (str((date(2016, 5, 6) - date.today()).days))
	else:
		start_day = start_date + timedelta(days=1)
		if date.today() - timedelta(days=streak) <= start_date:
			return 'Looks like you started a day late! No worries, we still want you to commit for 30 days, just commit for %s more days (until May 7, 2016) to get your custom Freetail shirt!' % (str((date(2016, 5, 7) - date.today()).days))
		else:
			return 'Our automated check isn\'t able to verify your completion towards a 30 day streak. If you believe this is a mistake, check to make sure all the repositories you committed to are public. If you still think there\'s an error, please reach out to <a href="mailto:hello@freetailhackers.com">hello@freetailhackers.com</a> so we can investigate further.'

@app.route('/', endpoint='index')
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
	page = requests.get('https://github.com/users/%s/contributions' % username)
	tree = html.fromstring(page.content)
	while current_iteration_day != end_day:
		current_commit = tree.xpath('//rect[@data-date="' + str(current_iteration_day) + '"]/@data-count')
		if current_commit:
			commit_dict[str(current_iteration_day)] = current_commit[0]
		current_iteration_day += timedelta(days=1)
	sorted_dict = OrderedDict(sorted(commit_dict.items(), key=lambda t:t[0]))
	return sorted_dict

@app.route('/results', endpoint='get-results', methods=['GET', 'POST'])
def get_results():
	if request.method == 'GET':
		return redirect(url_for('index'))
	username = request.form['username']
	page = requests.get('https://github.com/'  + username)
	if page.status_code != 200:
		return render_template('error.html', title='Invalid Username', message='That doesn\'t seem to be a valid GitHub username')
	page_tree = html.fromstring(page.content)
	streak_list = get_streak(username, page_tree)
	if streak_list:
		streak = streak_list[0]
	else:
		return render_template('error.html', title='Invalid Username', message='That doesn\'t seem to be a valid GitHub username')
	commit_dict = get_commits(username, streak)
	message = get_custom_message(int(streak.split()[0]), commit_dict)
	chart = render_chart(commit_dict)
	return render_template('results.html', streak=streak, commits=commit_dict, message=message, chart=chart)
	return get_info(username)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', title='Page Not Found', message='That page doesn\'t exist'), 404

if __name__ == '__main__':
	app.run(debug=True)
