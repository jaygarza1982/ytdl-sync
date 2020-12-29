import youtube_dl
import re
from os import path
import requests

class YTDL:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best', 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'music/',
        }
        #Add a progress hook for getting final file name
        #We will use this to add to a database of downloaded files
        self.ydl_opts['progress_hooks'] = [self.get_final_filename_hook]

    def get_final_filename_hook(self, d):
        if d['status'] == 'finished':
            print('Downloaded ', d['filename'])
    
    def download(self, url):
        #Before we get the video id, we could be syncing playlist
        #If we are syncing, the url passed will be the video id, check for this first
        possible_filename = 'music/{url}.mp3'.format(url=url)

        if not path.exists(possible_filename):
            filename = '%(id)s'
            #Get the video id, we later check if we have already downloaded it
            video_id = self.get_video_id(url)

            filename_downloaded = 'music/'
            filename_downloaded += video_id
            filename_downloaded += '.mp3'

            #Check to see if we have already downloaded this video
            if not path.exists(filename_downloaded) and filename_downloaded != 'music/id error.mp3':
                #Remove mp3 from filename because it will be added by ytdl
                if filename.lower().endswith('.mp3'):
                    filename = filename[:len(filename)-4]

                self.ydl_opts['outtmpl'] = 'music/'
                self.ydl_opts['outtmpl'] += filename
                self.ydl_opts['outtmpl'] += '.tmp'
                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([url])
            else:
                print('Video already downloaded to \'%s\'... Skipping.' % (filename_downloaded,))
        else:
            print('Video already downloaded to \'%s\'... Skipping.' % (possible_filename,))

    def get_playlist_urls(self, playlist_url):
        ydl = youtube_dl.YoutubeDL( {
            'ignoreerrors': True,
            'quiet': True
        })

        ids = []
        with ydl:
            playlist_dict = ydl.extract_info(playlist_url, download=False)
            regex_matches = re.findall(r"'id': '(\S{11})'", str(playlist_dict))

            for match in regex_matches:
                ids.append(str(match))

        print('playlist ids', ids)
        return ids

    def get_video_id(self, url):
        ydl = youtube_dl.YoutubeDL({
            'ignoreerrors': True,
            'quiet': True,
        })

        id = ''
        with ydl:
            extracted_info = ydl.extract_info(url, download=False)
            # r"'id': '(\S{11})'"
            regex_matches = re.findall(r"'id': '(\S{11})'", str(extracted_info))
            # regex_matches = re.findall(r"'id': \S{12}", str(extracted_info))
            
            try:
                id = regex_matches[0]#[7:]
            except:
                print('Could not download video', url)
                return 'id error'

        return id

    def get_title(self, url):
        try:
            if url != '':
                page = requests.get(url).content.decode('ascii', 'ignore')
                title = re.findall(r'<title>(.*?)</title>', str(page))[0]
                
                #Return title of page without the ' - YouTube'
                return title[0:len(title)-10]
        except:
            print('Could not get', url)

        return ''
