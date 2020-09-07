from __future__ import unicode_literals
import tkinter as tk
import youtube_dl
import time
import threading
import json
import re

# test url (shorter): https://www.youtube.com/watch?v=Jh9PxxggpI4
# test url (longer): https://www.youtube.com/watch?v=jrTMMG0zJyI

welcome = "Welcome to pymp3 v0.3!"
error = "Error! Did you paste the URL correctly?"
help_text = '''Welcome to PYMP3! - Convert any video
or playlist to MP3(s)! Videos will download to the
same directory as the executable. You can paste in
another track once conversion is complete. Longer
videos will (obviously?) take longer to convert
after downloading. Playlists will be downloaded
and converted in sequence automatically, but the
process will be interrupted if any of the videos
is not available...


Coming soon:
-batch convert bookmarks in json/html formats
-set download folder
-IDtagging


bitcoin: bc1qrrpd7dzmcf2gcdpld986mjmr9tnz8a9dpae7pg'''


# youtube_dl settings:
class MyLogger(object):
    def debug(self, msg):
        status_logger.set(msg)


    def warning(self, msg):
        pass

    def error(self, msg):
        var_1.set(error)
        status_logger.set('Error! Try again!')
        wait(1)
        paste_another.set('')


def my_hook(d):
    if d['status'] == 'finished':
        var_1.set("Download complete, converting to mp3...")
    elif d['status'] == 'downloading':
        status = ("Downloading...", d['_percent_str'])
        var_1.set(status)

ydl_opts = {
    'progress_hooks': [my_hook],
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
}


# Download function:
def mp3down():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([app.return_text()])
            wait(1)
            paste_another.set('')
            var_1.set(welcome)
            wait(3)
            status_logger.set('Ready')
        except:
            wait(5)
            var_1.set(welcome)
            status_logger.set('Ready')


# Threading
def refresh_threads():
    t1 = threading.Thread(target=mp3down)
    t1.start()


# json parsing:
def extract_urls(json_file):
    with open(json_file) as f:
        x = json.load(f)
    x_dict = json.dumps(x)
    youtube_links = re.findall(r'(ht\S+youtu\S+)"}', x_dict)
    return youtube_links


def wait(secs):
    time.sleep(secs)


class Window1:
    def __init__(self, master):
        self.master = master
        self.master.geometry('600x420')
        self.master.title("pymp3 v0.3.1 (Run inside the directory you want to download to...)")
        self.master.resizable(width=False, height=False)
        # self.icon = tk.PhotoImage(file="mp3tub3.png")
        # self.master.iconphoto(False, self.icon)
        self.frame = tk.Frame(self.master, bg="red")
        self.heading = tk.Label(self.frame, text='PYMP3', bg="red", fg="white", font=("Verdana 48 bold"), width='600')
        self.heading.pack()
        self.topframe = tk.Frame(self.frame, height='80', width='600', bg="gray")
        self.topframe.pack()
        self.middleframe = tk.Frame(self.frame, bg="black", width='600', height='50')
        self.middleframe.pack()
        self.bottomframe = tk.Frame(self.frame, bg="gray", width='600', height='150')
        self.bottomframe.pack()
        self.instruction = tk.Label(self.topframe, text="Paste video/playlist URL:", fg="green")
        self.instruction.place(relx=0.1, rely=0.25, relheight=0.5, relwidth=0.3)
        self.paste_field = tk.Entry(self.topframe, textvariable=paste_another, bg="white")
        self.paste_field.place(relx=0.4, rely=0.25, relheight=0.5, relwidth=0.5)
        self.download = tk.Button(self.bottomframe,
                            text="Download MP3",
                            fg="green",
                            command=lambda: refresh_threads())
        self.download.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
        self.label = tk.Label(self.middleframe,
                            textvariable=var_1,
                            bg="black",
                            fg="green")
        self.label.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.new_button('Help', HelpWindow)
        self.status = tk.Label(self.master, textvariable=status_logger, bd=1, relief="sunken", font='Verdana 8', anchor='w')
        self.status.pack(side="bottom", fill='x')
        self.frame.pack()

    def new_button(self, text, _class):
        tk.Button(self.frame, text=text, command=lambda: self.new_window(_class)).pack(pady=5)

    def new_window(self, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new)

    def set_text(self, text):
        self.text = text
        var_1.set(text)

    def return_text(self):
        return self.paste_field.get()


class HelpWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry('450x400')
        self.master.title('Help')
        self.frame = tk.Frame(self.master)
        self.quit = tk.Button(self.frame, text=f"Close", command=self.close_window)
        self.label = tk.Label(self.frame, text=help_text, font=('Verdana 10'))
        self.label.pack(pady=20)
        self.quit.pack(side="bottom")
        self.frame.pack()


    def close_window(self):
        self.master.destroy()


root = tk.Tk()

var_1 = tk.StringVar()
var_1.set("Welcome to pymp3!")

paste_another = tk.StringVar()
paste_another.set("")

status_logger = tk.StringVar()
status_logger.set("Ready")

app = Window1(root)
root.mainloop()
