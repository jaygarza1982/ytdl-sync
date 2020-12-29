import shutil, os, subprocess
import threading

import testconf as cfg

from DownloadTests import DownloadTest

#Copy the server over to the testing dir and remove all music and clear the test db
if os.path.exists('./testingserver'):
    shutil.rmtree('./testingserver')

if os.path.exists('downloads'):
    shutil.rmtree('downloads')
    os.mkdir('downloads')

shutil.copytree('../main', './testingserver')

shutil.rmtree('./testingserver/music')
os.mkdir('./testingserver/music')
os.remove('./testingserver/test_db.sql')

def start_test_server():
    subprocess.call('cd testingserver; python3 run.py test_db.sql', shell=True)

server_thread = threading.Thread(target=start_test_server)
server_thread.start()

download_test = DownloadTest()

results = []
results.append(download_test.only_url())
results.append(download_test.title_test())
results.append(download_test.title_album_test())
results.append(download_test.title_album_artist())

for result in results:
    print(result)