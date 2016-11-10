# -*- coding: utf-8 -*-

import os
import time
import dbus
import requests
from BeautifulSoup import BeautifulSoup
old = None

while 1:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    if metadata != old:
        os.system('clear')
        old = metadata
        r_json = requests.get('http://lyrics.wikia.com/api.php',
                              {'action': 'lyrics', 'artist': metadata['xesam:artist'],
                               'song': metadata['xesam:title'], 'fmt': 'json', 'func': 'getSong'})
        try:
            start = r_json.text.find("url")+6
            url = r_json.text[start:start + r_json.text[start:].find("'")]
            r_html = requests.get(url)
            parser = BeautifulSoup(r_html.text)
            html_text = parser.body.find('div', attrs={'class': 'lyricbox'}).prettify()
            start = html_text.find('>')+1
            end = start + html_text.find('<div class="lyricsb')-22
            html_lyric = html_text[start:end]
            lyric_arr = html_lyric.replace('&#', '').replace('\n', '').split('<br />')

            lyric_arr = [[y for y in x.split(';') if y != ''] for x in lyric_arr]
            for i, _ in enumerate(lyric_arr):
                lyric_arr[i] = [chr(int(x)) for x in lyric_arr[i]]
            lyric_arr = [''.join(x) for x in lyric_arr]
            terminal_cols = os.popen('tput cols').read()
            title = '[\033[4m' + metadata['xesam:artist'][0].title() + '/' + \
                metadata['xesam:title'] + '\033[0m]'
            print title.center(int(terminal_cols)+10)
            print '\033[1m',
            print '\n'.join([x.center(int(terminal_cols)) for x in lyric_arr])
            print '\033[0m'
        except Exception:
            print '[', metadata['xesam:artist'][0].title(), '/', metadata['xesam:title'], ']'
            print '----'

    time.sleep(1)
