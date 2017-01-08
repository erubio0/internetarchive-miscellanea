#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from bs4 import BeautifulSoup
import re
import feedparser
import subprocess
from internetarchive import upload
import pprint
import requests
import json

feed = feedparser.parse('http://retromallorca.com/tag/emitido/feed/')

item = feed['items'][0]

text = item['content'][0]['value']

page_url = item['link']
title = item['title']
date = re.search(r'Emisión: (\S*) ',text).group(1)
youtube_url = re.search(r'airYouTubeEmbed\(\"(.*)\"',text).group(1)

if '#' in title:
	id_obj = re.search(r'(.*) #(\d*)',title)
	identifier = id_obj.group(1).replace(' ','') + '-' + id_obj.group(2).replace(' ','')
else:
	id_obj = re.search(r'(.*):(.*)',title)
	identifier = id_obj.group(1).replace(' ','') + '-' + id_obj.group(2).replace(' ','')

description = BeautifulSoup(text,'lxml')

[tag.unwrap() for tag in description('html')]
[tag.unwrap() for tag in description('body')]
[tag.decompose() for tag in description('script')]
[tag.decompose() for tag in description('object')]
[tag.decompose() for tag in description('img')]

def classes_to_remove(tag):
	return tag.has_attr('class') and ( re.match('^a2a', ''.join(tag['class']))  )

[tag.decompose() for tag in description.findAll(classes_to_remove)]

for link in description.findAll('a'):
	link['href'] = 'https://web.archive.org/web/' + date.replace('-','') + '000000/' + link['href']

metadata = dict()

metadata['title'] = title
metadata['collection'] = 'retromallorca'
metadata['description'] = str(description)
metadata['language'] = 'spa'
metadata['licenseurl'] = 'http://creativecommons.org/licenses/by/3.0/'
metadata['mediatype'] = 'movies'
metadata['creator'] = 'RetroActivo Podcast / RetroMallorca'
metadata['publisher'] = 'RetroActivo Podcast / RetroMallorca'
metadata['date'] = date
metadata['subject'] = 'podcast;RetroActivo Podcast;RetroMallorca'

print(identifier + '\n')
pprint.pprint(metadata)

wb_confirm = input('\n\nSave snapshot into the Wayback Machine? ').lower()
if wb_confirm == 'y':
	r = requests.post('https://pragma.archivelab.org', headers={'Content-Type': 'application/json'}, data=json.dumps({'url': page_url}))
	print('\n' + r.text)

upload_confirm = input('\n\nUpload item? ').lower()
if upload_confirm == 'y':
	original_audio_file = subprocess.check_output('../youtube-dl -f bestaudio -o "' + identifier + '_audio.%(ext)s" --get-filename ' + youtube_url, shell=True, universal_newlines=True).replace('\n','')
	video_file = subprocess.check_output('../youtube-dl -f best -o "' + identifier + '.%(ext)s" --get-filename ' + youtube_url, shell=True, universal_newlines=True).replace('\n','')
	audio_file = identifier + '.mp3'
	subprocess.call('../youtube-dl -f bestaudio -o "' + identifier + '_audio.%(ext)s" ' + youtube_url, shell=True)
	subprocess.call('avconv -i ' + original_audio_file + ' ' + audio_file, shell=True)
	os.remove(original_audio_file)
	subprocess.call('../youtube-dl -f best -o "' + identifier + '.%(ext)s" ' + youtube_url, shell=True)
	upload(identifier, [video_file, audio_file], metadata)
	remove_confirm = input('\n\nRemove local files? ').lower()
	if remove_confirm == 'y':
		os.remove(video_file)
		os.remove(audio_file)

