import time, hashlib, os

class FileCheck:

    def __init__(self, path):
        self.path = path

    def check256(self, hash):
        #Wait for the file to be created
        while not os.path.exists(self.path):
            time.sleep(0.01)

        #Wait for finalization
        time.sleep(0.1)

        #Read the file and return if its hash is as expected
        file_read = open(self.path, 'rb').read()
        return hash == hashlib.sha256(file_read).hexdigest() == hash
