from flask import Flask, request, send_file, send_from_directory, session, make_response, redirect, render_template
from werkzeug.utils import secure_filename

from shutil import copyfile

import re

import random

from YTDL import YTDL

import eyed3

from os import path
import os
import time

import threading

from DBCreator import DBCreator
from User import User
from SQLWriter import SQLWriter

import sys

db_filename = sys.argv[1]

#If the database does not exist, create it
if not path.exists(db_filename):
    db_creator = DBCreator()
    db_creator.create(db_filename)

sql_writer = SQLWriter(db_filename)

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = str(os.urandom(128))

def sync_all_users():
    while True:
        # try:
        usernames = sql_writer.fetchall('SELECT Username FROM Users;')

        for username in usernames:
            print('Syncing', username[0])
            user = User(username[0], sql_writer)
            user.sync_playlists()
            print('Syncing', username[0], 'completed.')
        # except:
            # print('Could not sync user playlists.')
        time.sleep(1)

sync_users_thread = threading.Thread(target=sync_all_users, args=[])
sync_users_thread.daemon = True
sync_users_thread.start()

@app.route('/mp3')
def index_mp3():
    #Store url as well as meta data we will set later
    youtube_url = request.args.get('v')
    filename = request.args.get('filename')
    title = request.args.get('title')
    artist = request.args.get('artist')
    album = request.args.get('album')
    album_art = request.args.get('album-art')

    print(youtube_url, filename, title, artist, album)

    #Download and convert to mp3, files are stored as video_id.mp3
    getter = YTDL()
    getter.download(youtube_url)

    audio_file = 'music/'
    audio_file += getter.get_video_id(youtube_url)
    audio_file += '.mp3'

    #Copy the file to a temporary place so we can edit meta data
    temp_filename = 'tmp/'
    temp_filename += str(random.random() * 100)

    copyfile(audio_file, temp_filename)

    #Edit the meta data of the mp3 file
    eyed3_file = eyed3.load(temp_filename)
    eyed3_file.tag.title = '' if title == None else title
    eyed3_file.tag.artist = '' if artist == None else artist
    eyed3_file.tag.album = '' if album == None else album

    #If we are supplied a link to some album art, read the art file, set the mp3s album art
    if album_art != None:
        if album_art.strip() != '':
            print(album_art, 'is the album art name passed')
            try:
                art_file = 'images/'
                art_file += album_art
                art_data = open(art_file, 'rb').read()
                eyed3_file.tag.images.set(3, art_data, 'png')
            except:
                return_message = 'Was not able to set art. Art file: \'%s\'' % (art_file,)
                print(return_message)
                return return_message

    eyed3_file.tag.save()
    
    #Return the edited audio file to the client
    return send_file(temp_filename, as_attachment=True, attachment_filename=filename)

@app.route('/upload-image', methods=['POST'])
def index_upload_image():
    request_file = request.files['image']
    saved_filename = 'images/'
    saved_filename += str(random.random() * 100)
    saved_filename += secure_filename(request_file.filename)
    request_file.save(saved_filename)
    return saved_filename

@app.route('/title')
def index_title():
    url = request.args.get('url')
    getter = YTDL()
    return getter.get_title(url)

@app.route('/register', methods=['POST'])
def index_register():
    username = request.form['username-ytmp3']
    password = request.form['password-ytmp3']
    password_confirm = request.form['password-confirm-ytmp3']

    if password == password_confirm:
        user = User(username, sql_writer)
        if not user.exists():
            user.create(password)
        else:
            return 'The user {username} already exists.'.format(username=username)
    else:
        return 'Password mismatch.'

    #Insert username into page
    return open('static/login.html', 'r').read().replace('value=""', 'value={username}'.format(username=username))

@app.route('/login', methods=['POST'])
def index_login():
    username = request.form['username-ytmp3']
    password = request.form['password-ytmp3']

    user = User(username, sql_writer)

    if user.auth(password):
        random_bytes = str(os.urandom(64))
        cookie = '{rand}-{username}'.format(rand=random_bytes, username=username)
        session[cookie] = username
        resp = make_response(redirect('/home'))
        resp.set_cookie('login', cookie)
        
        return resp

    return 'Invalid credentials.'

@app.route('/home')
def index_home():
    username = session[request.cookies['login']]
    user = User(username, sql_writer)
    return render_template('home.html', playlists=user.get_playlists(), music=user.get_ready_music())

@app.route('/update-playlists', methods=['POST'])
def index_update_playlists():
    username = session[request.cookies['login']]
    user = User(username, sql_writer)

    playlists = request.form['playlists']
    playlist_urls = playlists.split(',')
    user.update_playlists(playlist_urls)

    return 'Success.'
    
@app.route('/static/<path:path>')
def index_send_static(path):
    return send_from_directory('static', path)

@app.route('/images/<path:path>')
def index_send_image(path):
    return send_from_directory('images', path)

@app.route('/music/<path:path>')
def index_send_music(path):
    file_path = 'music/'
    file_path += path
    return send_file(file_path, as_attachment=True, attachment_filename=request.args.get('title'))

@app.route('/')
def index():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run()


#http://localhost:5000/mp3?v=https://www.youtube.com/watch?v=XFmZPIUpTg4&filename=test filename.mp3&title=test title&album=test album&artist=Slaya
#http://localhost:5000/mp3?v=URL&filename=FILENAME&title=TITLE&album=ALBUM&artist=ARTIST