import tkinter as tk
import youtube_dl


path = 'mp3tub3.png'

HEIGHT=500
WIDTH=600

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

def mp3down(paste):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([paste])

root = tk.Tk()
root.title("mp3tub3 v0.1 (Run inside the directory you want to download to...)")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="white")
canvas.pack()

topframe = tk.Frame(root, bg="gray")
topframe.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)

bottomframe = tk.Frame(root, bg="gray")
bottomframe.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.3)

download = tk.Button(bottomframe, text="Download MP3", fg="Green", command=lambda: mp3down(paste.get()))
download.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

instruction = tk.Label(topframe, text="Paste URL here:", fg="green")
instruction.place(relx=0.1, rely=0.35, relheight = 0.3, relwidth=0.3)

paste = tk.Entry(topframe, bg="white")
paste.place(relx=0.4, rely=0.35, relheight=0.3, relwidth=0.5)

root.mainloop()