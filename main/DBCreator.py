import sqlite3

from SQLWriter import SQLWriter

class DBCreator:
    def create(self, db_file):
        #Touch db file
        open(db_file, 'w').close()

        sql_writer = SQLWriter(db_file)

        #Create a user table that contains login information as well as their unique ID
        sql_writer.execute('CREATE TABLE Users (UserID Integer NOT NULL PRIMARY KEY, Username VARCHAR(24), Password BINARY(128), Salt Binary(128));')

        #Create a Playlists table that contains playlists that are being synced by users
        sql_writer.execute('CREATE TABLE Playlists (PlaylistID Integer NOT NULL PRIMARY KEY, UserID Integer, URL TEXT);')

        #Create a ReadyMusic table that contains music files that are ready that were requested by a user
        sql_writer.execute('CREATE TABLE ReadyMusic (ReadyMusicID Integer NOT NULL PRIMARY KEY, UserID Integer, VideoID VARCHAR(11), VideoTitle TEXT)')