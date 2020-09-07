from __future__ import unicode_literals
import tkinter as tk
import youtube_dl
import time

HEIGHT = 400
WIDTH = 600


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}
# test url: https://www.youtube.com/watch?v=Jh9PxxggpI4


def dl():
    if len(paste_field.get()) <= 0:
        var_1.set("You forgot to paste the URL")
    elif len(paste_field.get()) > 0:
        dling()


def mp3down(paste):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([paste])
        finished()


def dling():
    var_1.set("Downloading")


def finished():
    var_1.set("Download complete!")


def wait():
    time.sleep(0.5)

# I'm having trouble here with getting the "Downloading" label to show.
# I've tried a ton of things and can get it to show from inside the function but it interrupts the actual download.

# def mp3down(paste):
#     if len(paste) <= 0:
#         label.config(text="You forgot to paste the URL")
#     else:
#         label.config(text="Downloading...")
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([paste])
#     label.config(text="Download Complete!")


# def draw_frame():
#    middleframe = tk.Frame(root, bg="black")
#    middleframe.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.1)


# Trying to print song info:
# def title(paste):
#    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#        ydl.extract_info([paste], download=False)


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
var_1.set("Welcome to MP3TUB3!")
label = tk.Label(middleframe,
                 textvariable=var_1,
                 bg="black",
                 fg="green")
label.place(relx=0.1, rely=0, relheight=1, relwidth=0.8)

bottomframe = tk.Frame(root, bg="gray")
bottomframe.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.3)

download = tk.Button(bottomframe,
                     text="Download MP3",
                     command=lambda: [dl(), wait(), mp3down(paste_field.get())])
download.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

instruction = tk.Label(topframe,
                       text="Paste URL here:",
                       fg="green")
instruction.place(relx=0.1, rely=0.35, relheight=0.3, relwidth=0.3)

paste_field = tk.Entry(topframe,
                       bg="white")
paste_field.place(relx=0.4, rely=0.35, relheight=0.3, relwidth=0.5)

root.mainloop()
