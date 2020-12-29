import testconf as cfg

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os

import hashlib
import time

from FileCheck import FileCheck

class DownloadTest:

    def __init__(self):
        downloads_dir = os.path.abspath('downloads')
        options = Options()
        options.set_preference('browser.download.folderList', 2)
        options.set_preference('browser.download.dir', downloads_dir)
        options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/mpeg')

        self.browser = webdriver.Firefox(firefox_options=options)

    def _inputs(self, args):
        self.browser.get('http://{ip}:{port}'.format(ip=cfg.host['ip'], port=cfg.host['port']))

        for arg in args:
            self.browser.find_element_by_id(arg).send_keys(args[arg])

        self.browser.find_element_by_id('btnDownload').click()

    def only_url(self):
        filename = 'test file name.mp3'
        args = {
            'url': cfg.test_urls[0],
            'filename': filename,
        }

        self._inputs(args)

        fc = FileCheck('downloads/{file}'.format(file=filename))
        return(fc.check256('7947c0f35877611cd7279c5ee51387044e2938f937e59267b38831637224e98c'), 'Test no args, only url')

    def title_test(self):
        filename = 'title test file.mp3'
        args = {
            'url': cfg.test_urls[0],
            'filename': filename,
            'title': 'test title test',
        }

        self._inputs(args)

        fc = FileCheck('downloads/{file}'.format(file=filename))
        checked = fc.check256('099f9dd290bacf2604336ee287e4c08ef3b170ecc5b1fd16bda9fae53372f907')

        return(checked, 'Test title')

    def title_album_test(self):
        filename = 'test with title and album.mp3'
        args = {
            'url': cfg.test_urls[1],
            'filename': filename,
            'title': 'test title with album',
            'album': 'testalbum_nameZ'
        }

        self._inputs(args)

        fc = FileCheck('downloads/{file}'.format(file=filename))
        checked = fc.check256('397a965a640743a558b86bf45dc81f40040de9eac865c88c37712cfa638f5549')

        return(checked, 'Test with title and album')

    def title_album_artist(self):
        filename = 'test with title album artist.mp3'
        args = {
            'url': cfg.test_urls[1],
            'filename': filename,
            'title': 'test title with all',
            'album': 'test album contains all',
            'artist': 'coolest artist!!',
        }

        self._inputs(args)

        fc = FileCheck('downloads/{file}'.format(file=filename))
        checked = fc.check256('11bcefc99fc4b3c097769f1fef682e55efe507555630e0eef37a860079dbf3d6')

        return(checked, 'Test with title, album, artist')