from SQLWriter import SQLWriter
from YTDL import YTDL

import hashlib
import os

class User:
    def __init__(self, username, sql_writer):
        self.username = username
        self.sql_writer = sql_writer

    #Returns if a user already exists with this username
    def exists(self):
        return self.sql_writer.fetchone(
            """SELECT Username FROM Users WHERE Username = ?;""",
        (self.username,)) != None

    def create(self, password):
        #Insert a user into the database if they do not already exist
        if not self.exists():
            hash_tuple = self.get_hash_and_salt(password)
            hashed_pass = hash_tuple[0]
            generated_salt = hash_tuple[1]
            self.sql_writer.execute(
                """
                    INSERT INTO Users (Username, Password, Salt) VALUES (?, ?, ?);
                """,
            (self.username, hashed_pass, generated_salt,))

    def auth(self, password):
        credentials = self.sql_writer.fetchone(
            """
                SELECT Password, Salt FROM Users WHERE Username = ?;
            """,
        (self.username,))

        return self.get_hash(password, credentials[1]) == credentials[0]

    #Update synced playlists from a list of playlist urls
    def update_playlists(self, playlist_urls):
        #Delete all playlists currently associated with the user
        self.sql_writer.execute(
            """
                DELETE FROM Playlists WHERE UserID = (SELECT UserID FROM Users WHERE Username = ?);
            """,
        (self.username,))

        #Insert all of the playlists given into the Playlists table
        for playlist in playlist_urls:
            if len(playlist) != 0:
                self.sql_writer.execute(
                    """
                        INSERT INTO Playlists (UserID, URL) VALUES ((SELECT UserID FROM Users WHERE Username = ?), ?);
                    """,
                (self.username, playlist,))

    #Get the playlists the user is currently syncing
    def get_playlists(self):
        playlists = []

        playlist_query = self.sql_writer.fetchall(
            """
                SELECT PlaylistID, URL FROM Playlists WHERE UserID = (SELECT UserID FROM Users WHERE Username = ?);
            """,
        (self.username,))

        for query in playlist_query:
            playlists.append({})
            playlists[len(playlists)-1]['PlaylistID'] = query[0]
            playlists[len(playlists)-1]['URL'] = query[1]
        
        return playlists

    def sync_playlists(self):
        getter = YTDL()

        playlists = self.get_playlists()

        for playlist in playlists:
            playlist_urls = getter.get_playlist_urls(playlist['URL'])

            #Remove last video url because it is not a video
            #This may error if playlist is empty
            # playlist_urls.pop()
            
            for url in playlist_urls:
                # try:
                getter.download(url)
                
                #The 'url' is just the video id because ytdl does not need the full url
                url_for_title = 'https://www.youtube.com/watch?v='
                url_for_title += url

                #Check if this user already has this video synced
                # video_id = getter.get_video_id(url)
                pre_synced = self.sql_writer.fetchall(
                    """
                        SELECT VideoID FROM ReadyMusic WHERE UserID = (SELECT UserID FROM Users WHERE Username = ?) AND VideoID = ?;
                    """,
                    (self.username, url,)
                )

                if pre_synced != None and len(pre_synced) == 0:
                    #Insert into DB that the music is ready for user
                    self.sql_writer.execute(
                        """
                            INSERT INTO ReadyMusic (UserID, VideoID, VideoTitle) VALUES ((SELECT UserID FROM Users WHERE Username = ?), ?, ?);
                        """,
                    (self.username, url, getter.get_title(url_for_title),))
                # except:
                    # print('error in sync playlists')

    def get_ready_music(self):
        video_ids = []

        ready_query = self.sql_writer.fetchall(
            """
                SELECT VideoID, VideoTitle FROM ReadyMusic WHERE UserID = (SELECT UserID FROM Users WHERE Username = ?);
            """,
        (self.username,))

        for query in ready_query:
            video_ids.append({})
            video_ids[len(video_ids) - 1]['VideoID'] = query[0]
            video_ids[len(video_ids) - 1]['VideoTitle'] = query[1]

        return video_ids

    # Get a hash and a salt
    def get_hash_and_salt(self, password):
        salt = os.urandom(128)  # Remember this

        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128  # Get a 128 byte key
        )

        return (key, salt,)

    # Get a hash with a salt
    def get_hash(self, password, salt):
        hash = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128  # Get a 128 byte key
        )

        return hash