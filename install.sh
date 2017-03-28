#!/usr/bin/bash
sudo pip2 install -r requirements.txt 
sudo chmod 755 spotify-lyric
sudo cp spotify-lyric /usr/local/bin
echo "Installation complete."
echo "spotify-lyric to show your lyrics"
