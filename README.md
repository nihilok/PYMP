# PYMP
experiments with building a GUI for youtube-dl

latest version 0.5 includes:

Download MP4
Download MP3 (ffmpeg or avconv required)
Import bookmarks (JSON file)

Coming in future releases:
Import HTML bookmarks

How to run: You can run the script (from the same dir) using python, which will bring up the GUI (you will need the correct libraries installed: youtube-dl is the only non standard one I believe. $ pip3 install youtube-dl)

$ python3 pympv0.5.py

Or you can run the linux executable, but you will first need to make the file executable:

$ chmod +x pympv0.5

And finally, a Windows executable will also be included with this release! Windows defender will probably think it's a virus - just tell it to 'allow on this device'.

1. Run the program from inside download folder to automatically download to that folder.
2. Paste the link of a video or playlist and click "Download MP3/MP4!"
2. Sit back and enjoy!

There will be a problem with mp3 conversion if you don't have FFMpeg / avconv installed. -- Linux: $ sudo apt install ffmpeg
or on Windows: https://www.wikihow.com/Install-FFmpeg-on-Windows

Import Bookmarks:

1. save the .json file with bookmarks in the same folder
2. input the name e.g "bookmarks.json" in the paste field
3. Click 'Batch Download'

Occasionally the process may run slowly and seem to freeze but it will keep going. I think this is on the communication with video host.
