import requests
import json
import os
import subprocess

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
ytdlp = dirPath + "/binaries/yt-dlp.exe"
aria2c = dirPath + "/binaries/aria2c.exe"
mkvmerge = dirPath + "/binaries/mkvmerge.exe"

input_video = dirPath + '/vid.mp4'
input_audio = dirPath + '/aud.m4a'


inp = input('Enter the Link: ')
fxl = inp.split("/")
cid = fxl[-1]

URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'

header = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://mdisk.me/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}

resp = requests.get(url=URL, headers=header).json()['source']
# print(resp)

subprocess.run([ytdlp, '--no-warning', '-k', '--user-agent',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', '--allow-unplayable-formats', '-F', resp])

vid_format = input('\nEnter Video Format ID: ')
aud_format = input('\nEnter Audio Format ID: ')

if not os.path.exists(input_video):
    subprocess.run([ytdlp, '--no-warning', '-k', '-f', vid_format, resp, '-o', 'vid.mp4', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                   '--allow-unplayable-formats', '--external-downloader', aria2c, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
else:
    pass

if not os.path.exists(input_audio):
    subprocess.run([ytdlp, '--no-warning', '-k', '-f', aud_format, resp, '-o', 'aud.m4a', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                   '--allow-unplayable-formats', '--external-downloader', aria2c, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
else:
    pass

output = requests.get(url=URL, headers=header).json()['filename']
output = output.replace(".mkv", "").replace(".mp4", "")

mkvmerge_command = [mkvmerge, '--ui-language', 'en', '--output', output + '.mkv', '--language', '0:und', '--default-track', '0:yes', '--compression', '0:none', input_video,
                    '--language', '0:en', '--default-track', '0:yes', '--compression', '0:none', input_audio]
subprocess.run(mkvmerge_command)

print('Cleaning Leftovers...')
if os.path.exists(output+'.mkv'):
    os.remove(input_audio)
    os.remove(input_video)
    print('Done!')
