from DBCreator import DBCreator
from SQLWriter import SQLWriter
from User import User

db_filename = 'test_db.sql'

db_creator = DBCreator()
db_creator.create(db_filename)

sql_writer = SQLWriter(db_filename)

# user1 = User('test', sql_writer)
# user1.create('testpass')


# sql_writer.execute('INSERT INTO Users (Username, Password, Salt) VALUES (?, ?, ?);', ('test', 'testpass', 'testsalt',))
user = User('test', sql_writer)
user.create('testpass')
fetchedall = sql_writer.fetchall('SELECT Username FROM Users WHERE Username = ?;', ('test',))
fetchedone = sql_writer.fetchone('SELECT Username FROM Users WHERE Username = ?;', ('test',))
no_exist = sql_writer.fetchone('SELECT Username FROM Users WHERE Username = ?;', ('do-not-exist',))
user2 = User('testy', sql_writer)
print(no_exist == None, 'Non existant user test')
print(fetchedall == [('test',)], 'Fetch all users test')
print(fetchedone == ('test',), 'Fetch one user test')
print(user.exists(), 'User class file test exists')
print(user2.exists() == False, 'User class file test exists')
print(user.auth('testpass'), 'User login success test')
print(user.auth('testpass2') == False, 'User login fail test')

to_insert = [
    'https://www.youtube.com/playlist?list=PL0KPoCNgiWsN4-ZKpAmdLaQvSglBh2nTJ',
    'https://www.youtube.com/playlist?list=PL0KPoCNgiWsMo9jZKemDhv8BfFMBdLnHN'
]

after_insert = """[{'PlaylistID': 1, 'URL': 'https://www.youtube.com/playlist?list=PL0KPoCNgiWsN4-ZKpAmdLaQvSglBh2nTJ'}, {'PlaylistID': 2, 'URL': 'https://www.youtube.com/playlist?list=PL0KPoCNgiWsMo9jZKemDhv8BfFMBdLnHN'}]"""

user.update_playlists(to_insert)
print(str(user.get_playlists()) == after_insert, 'Playlist insert and retrive test')

to_update = ['https://www.youtube.com/playlist?list=PL0KPoCNgiWsN4-ZKpAmdLaQvSglBh2nTJ',]
user.update_playlists(to_update)
after_insert = """[{'PlaylistID': 1, 'URL': 'https://www.youtube.com/playlist?list=PL0KPoCNgiWsN4-ZKpAmdLaQvSglBh2nTJ'}]"""
print(str(user.get_playlists()) == after_insert, 'Playlist update again with removed playlist')

user.update_playlists(['https://www.youtube.com/playlist?list=PL0KPoCNgiWsNEAWbOw5BeCTtL9miFPxqq'])
user.sync_playlists()
ready_music = str(user.get_ready_music())
print('08kMdn8L7Yw' in ready_music and '2LaYILqP9KA' in ready_music, 'Sync playlist test')          #.sort() == ['08kMdn8L7Yw', '2LaYILqP9KA'].sort(), 'Sync playlist test')

fetched_ready_music = str(sql_writer.fetchall('SELECT VideoTitle FROM ReadyMusic WHERE UserID = 1;'))
print('If insects had to introduce themselves.' in fetched_ready_music and 'Super human interview' in fetched_ready_music, 'Video title in ready music table')