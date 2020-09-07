from __future__ import unicode_literals
import tkinter as tk
import youtube_dl
# import multiprocessing
import threading
import time

#def wait function
def wait(x):
    time.sleep(x)

# youtube_dl settings:
def my_hook(d):
    if d['status'] == 'finished':
        var_1.set("Download Complete!")
        wait(3)
        var_1.set("Welcome to mp3tub3!")
    elif d['status'] == 'downloading':
        status = ("Downloading...", d['_percent_str'])
        var_1.set(status)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        wait(2)
        var_1.set("Error! Did you paste the URL correctly?!")


ydl_opts = {
    'progress_hooks': [my_hook],
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
}


# Download funtion:
def mp3down():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([paste_field.get()])
# test url: https://www.youtube.com/watch?v=Jh9PxxggpI4


def empty():
    if len(paste_field.get()) <= 0:
        var_1.set("You forgot to paste the URL!")
    else:
        pass


# threading
def refresh_threads():
    t1 = threading.Thread(target=mp3down)
    t2 = threading.Thread(target=empty)
    t1.start()
    t2.start()


# multiprocessing
# p1 = multiprocessing.Process(target=mp3down)
# p2 = multiprocessing.Process(target=empty)
#
#
# def start():
#     p1.start()
#     p2.start()


HEIGHT = 400
WIDTH = 600

root = tk.Tk()
root.title("mp3tub3 v0.2 (Run inside the directory you want to download to...)")
root.resizable(width=False, height=False)
icon = tk.PhotoImage(file="mp3tub3.png")
root.iconphoto(False, icon)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="white")
canvas.pack()

topframe = tk.Frame(root, bg="gray")
topframe.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)

middleframe = tk.Frame(root, bg="black")
middleframe.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.1)

var_1 = tk.StringVar()
var_1.set("Welcome to mp3tub3!")

label = tk.Label(middleframe,
                 textvariable=var_1,
                 bg="black",
                 fg="green")
label.place(relx=0.1, rely=0, relheight=1, relwidth=0.8)

bottomframe = tk.Frame(root, bg="gray")
bottomframe.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.3)

download = tk.Button(bottomframe,
                     text="Download MP3",
                     fg="green",
                     command=lambda: refresh_threads())
download.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

instruction = tk.Label(topframe,
                       text="Paste URL here:",
                       fg="green")
instruction.place(relx=0.1, rely=0.35, relheight=0.3, relwidth=0.3)

paste_field = tk.Entry(topframe,
                       bg="white")
paste_field.place(relx=0.4, rely=0.35, relheight=0.3, relwidth=0.5)

root.mainloop()