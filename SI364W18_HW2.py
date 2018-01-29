## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
class AlbumEntryForm(FlaskForm):
	album_n = StringField("Enter the name of an album:", validators=[Required()])
	rating = RadioField("How much do you like this album? (1 low, 3 high)", choices=[("1", "1"), ("2", "2"), ("3", "3")], validators=[Required()])
	submit = SubmitField("Submit")



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def aristform():
	return render_template("artistform.html")

@app.route("/artistinfo", methods= ['POST', 'GET'])
def artistinfo():
	if request.method == 'GET':
		baseurl = 'https://itunes.apple.com/search?'
		params = {'entity': 'song', 'term': request.args['artist']}
		info = requests.get(baseurl, params= params)
		artist_data = info.json()['results']
		return render_template('artist_info.html', objects= artist_data)

@app.route("/artistlinks")
def artist_links():
	return render_template('artist_links.html')


@app.route("/specific/song/<artist_name>")
def specific_song(artist_name):
	baseurl = 'https://itunes.apple.com/search?'
	params = {'term': artist_name}
	info = requests.get(baseurl, params=params)
	song_data = info.json()['results']
	return render_template('specific_artist.html', results= song_data)

@app.route('/album_entry')
def albumentry():
	form = AlbumEntryForm()
	return render_template('album_entry.html', form=form)

@app.route('/album_result', methods= ('POST', 'GET'))
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method== 'POST' and form.validate_on_submit():
		album_n = form.album_n.data
		rating = form.rating.data
		return render_template('album_data.html', album_n= album_n, rating= rating)
	flash('All fields are required')
	return redirect(url_for('albumentry'))





if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
