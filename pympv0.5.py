import tkinter as tk
import youtube_dl
import time
import threading
import json
import re

# test url (shorter): https://www.youtube.com/watch?v=Jh9PxxggpI4
# test url (longer): https://www.youtube.com/watch?v=jrTMMG0zJyI

error = "Error!"
help_text = 'Convert any video or playlist to MP3/MP4! Videos will download to the same directory as the executable. ' \
            'You can paste in another URL once conversion is complete. Longer videos will (obviously?) take longer ' \
            'to convert after downloading. Playlists will be downloaded and converted in sequence automatically. ' \
            ' You can import bookmarks in json format to batch download MP3s. Enter the name of the file saved in '\
            'the same directory e.g. "bookmarks.json" ' + '''
            
Troubleshooting:
- Is FFmpeg installed?
ubuntu - $ sudo apt install ffmpeg
windows - google "install ffmpeg"

bitcoin: bc1qrrpd7dzmcf2gcdpld986mjmr9tnz8a9dpae7pg'''
disclaimer = "PYMP is intended solely for the temporary download of audio or video resources " \
             "for their offline use in contexts such as education. The developers do not condone " \
             "the illegal copying, distribution and/or otherwise profiting from " \
             "the misuse of intellectual property."


# youtube_dl console output:
class MyLogger(object):
    def debug(self, msg):
        Pymp.status_bar.set(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        Pymp.status_bar.set(msg)
        Pymp.var1.set(error)
        wait(1)
        Pymp.var2.set('')


# hook: gui display
def my_hook(d):
    if d['status'] == 'finished':
        readout = "Download complete, now converting..."
        Pymp.var1.set(readout)
    elif d['status'] == 'downloading':
        readout = ("Downloading...", d['_percent_str'])
        Pymp.var1.set(readout)


# json parsing:
def extract_urls(json_file):
    with open(json_file) as f:
        x = json.load(f)
        x_dict = json.dumps(x)
        return re.findall(r'(ht\S+youtu\S+)",', x_dict)


# wait function
def wait(secs):
    time.sleep(secs)


LARGE_FONT = 'Verdana 14 bold'
MEDIUM_FONT = 'Verdana 10'
SMALL_FONT = 'Verdana 8'
title = 'PYMPv0.5'
TITLE_FONT = 'Courier 54 bold'


class Pymp(tk.Tk):

    var1 = None
    var2 = None
    url = None
    status_bar = None

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, title)
        self.geometry('500x330')
        self.resizable(False, False)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        str_var1 = tk.StringVar()
        str_var2 = tk.StringVar()
        str_var3 = tk.StringVar()
        Pymp.var1 = str_var1
        Pymp.var1.set('')
        Pymp.var2 = str_var2
        Pymp.var2.set('')
        Pymp.status_bar = str_var3
        Pymp.status_bar.set('Ready')

        self.frames = {}

        for F in (Disclaimer, MenuWindow, Pymp3, Pymp4, BatchConvert):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Disclaimer)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class Disclaimer(tk.Frame):

    def __init__(self, parent, controller):
        disclaimer_label = tk.StringVar()
        disclaimer_label.set(disclaimer)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Disclaimer:", font=LARGE_FONT)
        label.pack(pady=20, padx=10)
        label2 = tk.Label(self, textvariable=disclaimer_label, font=MEDIUM_FONT,
                          width=60, wraplength=400, anchor='center', justify='center')
        label2.pack(pady=40, padx=10)

        button_frame = tk.Frame(self, height=100)
        button_frame.pack(side="bottom", pady=10, fill='x')

        button1 = tk.Button(button_frame, text="OK!", anchor='s',
                            command=lambda: controller.show_frame(MenuWindow))
        button1.pack(padx=10)


class MenuWindow(tk.Frame):
        
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to PYMP!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        label2 = tk.Label(self, text=help_text, font=SMALL_FONT, justify='left', wraplength=400)
        label2.pack()

        status = tk.Label(self, textvariable=Pymp.status_bar, bd=1, relief="sunken",
                          font='Verdana 8', height=1, anchor='sw')
        status.pack(side="bottom", fill='x')

        button_frame = tk.Frame(self, height=100)
        button_frame.pack(side='bottom', pady=5, fill='x')
        button1 = tk.Button(button_frame, text="PYMP3", anchor='s',
                            command=lambda: controller.show_frame(Pymp3))
        button1.pack(side='left', padx=49)
        button2 = tk.Button(button_frame, text="PYMP4", anchor='s',
                            command=lambda: controller.show_frame(Pymp4))
        button2.pack(side='right', padx=49)
        button3 = tk.Button(button_frame, text="Import Bookmarks", anchor='s',
                            command=lambda: controller.show_frame(BatchConvert))
        button3.pack()


class Pymp3(tk.Frame):
    url = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleframe = tk.Frame(self, bg='red', height=70, width=500)
        titleframe.pack(fill='x')
        titlelabel = tk.Label(titleframe, text="PYMP3", fg='white', bg='red', font=TITLE_FONT)
        titlelabel.place(relx=0.1, rely=0.1, relheight=1.1, relwidth=0.8)
        topframe = tk.Frame(self, bg="gray", height=60, width=500)
        topframe.pack(fill='x')
        instruction = tk.Label(topframe, text="Paste URL here:", fg="green")
        instruction.place(relx=0.1, rely=0.15, relheight=0.7, relwidth=0.3)
        self.paste_field = tk.Entry(topframe, bg="white", text=Pymp.var2)
        self.paste_field.place(relx=0.4, rely=0.15, relheight=0.7, relwidth=0.5)
        middleframe = tk.Frame(self, bg="gray", height=40)
        middleframe.pack(fill='x')
        label = tk.Label(middleframe, textvariable=Pymp.var1, bg="black", fg="green")
        label.place(relx=0.1, rely=0, relheight=1, relwidth=0.8)
        bottomframe = tk.Frame(self, bg="gray", height=100)
        bottomframe.pack(fill='x')
        button3 = tk.Button(bottomframe, text="Download MP3!", fg='green',
                            command=lambda: self.refresh_threads())
        button3.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

        status = tk.Label(self, textvariable=Pymp.status_bar, bd=1, relief="sunken",
                          font='Verdana 8', height=1, anchor='sw')
        status.pack(side="bottom", fill='x')
        button_frame = tk.Frame(self, height=100)
        button_frame.pack(side='bottom', pady=5, fill='x')
        button1 = tk.Button(button_frame, text="Home", anchor='s',
                            command=lambda: controller.show_frame(MenuWindow))
        button1.pack(side='left', padx=49)
        button2 = tk.Button(button_frame, text="PYMP4", anchor='s',
                            command=lambda: controller.show_frame(Pymp4))
        button2.pack(side='right', padx=49)
        button3 = tk.Button(button_frame, text="Import Bookmarks", anchor='s',
                            command=lambda: controller.show_frame(BatchConvert))
        button3.pack()

    def copy_url(self):
        self.url = self.paste_field.get()
        return self.url
    
    def download(self):
        ydl_options = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'logger': MyLogger(),
                        'progress_hooks': [my_hook],
                        }
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            ydl.add_default_info_extractors()
            # ydl.add_progress_hook(self.hook)
            try:
                ydl.download([self.copy_url()])
                Pymp.var1.set('Ready')
                wait(1)
                Pymp.status_bar.set('Ready')
                Pymp.var2.set('')
            except:
                Pymp.var1.set(error)
                wait(1)
                Pymp.var2.set('')


    def refresh_threads(self):
        self.t1 = threading.Thread(target=self.download)
        self.t1.start()


class Pymp4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleframe = tk.Frame(self, bg='green', height=70, width=500)
        titleframe.pack(fill='x')
        titlelabel = tk.Label(titleframe, text="PYMP4", fg='white', bg='green', font=TITLE_FONT)
        titlelabel.place(relx=0.1, rely=0.1, relheight=1.1, relwidth=0.8)
        topframe = tk.Frame(self, bg="gray", height=60, width=500)
        topframe.pack(fill='x')
        instruction = tk.Label(topframe, text="Paste URL here:", fg="green")
        instruction.place(relx=0.1, rely=0.15, relheight=0.7, relwidth=0.3)
        self.paste_field = tk.Entry(topframe, bg="white", text=Pymp.var2)
        self.paste_field.place(relx=0.4, rely=0.15, relheight=0.7, relwidth=0.5)
        middleframe = tk.Frame(self, bg="gray", height=40)
        middleframe.pack(fill='x')
        label = tk.Label(middleframe, textvariable=Pymp.var1, bg="black", fg="green")
        label.place(relx=0.1, rely=0, relheight=1, relwidth=0.8)
        bottomframe = tk.Frame(self, bg="gray", height=100)
        bottomframe.pack(fill='x')
        button3 = tk.Button(bottomframe, text="Download MP4!", fg='green',
                            command=lambda: self.refresh_threads())
        button3.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

        status = tk.Label(self, textvariable=Pymp.status_bar, bd=1, relief="sunken",
        				  font='Verdana 8', height=1, anchor='sw')
        status.pack(side="bottom", fill='x')
        button_frame = tk.Frame(self, height=100)
        button_frame.pack(side='bottom', pady=5, fill='x')
        button1 = tk.Button(button_frame, text="Home", anchor='s',
                            command=lambda: controller.show_frame(MenuWindow))
        button1.pack(side='left', padx=49)
        button2 = tk.Button(button_frame, text="PYMP3", anchor='s',
                            command=lambda: controller.show_frame(Pymp3))
        button2.pack(side='right', padx=49)
        button3 = tk.Button(button_frame, text="Import Bookmarks", anchor='s',
                            command=lambda: controller.show_frame(BatchConvert))
        button3.pack()

    def copy_url(self):
        self.url = self.paste_field.get()
        return self.url

    def download(self):
        ydl_options = {
            'format': 'best[ext=mp4]',
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            ydl.add_default_info_extractors()
            # ydl.add_progress_hook(self.hook)
            try:
                ydl.download([self.copy_url()])
                Pymp.var1.set('Ready')
                Pymp.var2.set('')
                wait(1)
                Pymp.status_bar.set('Ready')
            except:
                Pymp.var1.set(error)
                Pymp.var2.set('')

    def refresh_threads(self):
        self.t2 = threading.Thread(target=self.download)
        self.t2.start()

class BatchConvert(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleframe = tk.Frame(self, bg='yellow', height=70, width=500)
        titleframe.pack(fill='x')
        titlelabel = tk.Label(titleframe, text="PYMPson", fg='white', bg='yellow', font=TITLE_FONT)
        titlelabel.place(relx=0.1, rely=0.1, relheight=1.1, relwidth=0.8)
        topframe = tk.Frame(self, bg="gray", height=60, width=500)
        topframe.pack(fill='x')
        instruction = tk.Label(topframe, text="Bookmarks file:", fg="green")
        instruction.place(relx=0.1, rely=0.15, relheight=0.7, relwidth=0.3)
        self.paste_field = tk.Entry(topframe, bg="white", text=Pymp.var2)
        self.paste_field.place(relx=0.4, rely=0.15, relheight=0.7, relwidth=0.5)
        middleframe = tk.Frame(self, bg="gray", height=40)
        middleframe.pack(fill='x')
        label = tk.Label(middleframe, textvariable=Pymp.var1, bg="black", fg="green")
        label.place(relx=0.1, rely=0, relheight=1, relwidth=0.8)
        bottomframe = tk.Frame(self, bg="gray", height=100)
        bottomframe.pack(fill='x')
        button3 = tk.Button(bottomframe, text="Batch Download MP3s!", fg='green',
                            command=lambda: self.refresh_threads())
        button3.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
        status = tk.Label(self, textvariable=Pymp.status_bar, bd=1, relief="sunken",
                          font='Verdana 8', height=1, anchor='sw')
        status.pack(side="bottom", fill='x')
        button_frame = tk.Frame(self, height=100)
        button_frame.pack(side='bottom', pady=5, fill='x')
        button1 = tk.Button(button_frame, text="Home", anchor='s',
                            command=lambda: controller.show_frame(MenuWindow))
        button1.pack(side='left', padx=49)
        button2 = tk.Button(button_frame, text="PYMP3", anchor='s',
                            command=lambda: controller.show_frame(Pymp3))
        button2.pack(side='right', padx=49)
        button3 = tk.Button(button_frame, text="PYMP4", anchor='s',
                            command=lambda: controller.show_frame(Pymp4))
        button3.pack()

    def import_json(self):
        json_file = self.paste_field.get()
        return json_file

    def batch_download(self):
        ydl_options = {
                        'format': 'bestaudio/best',
                        # 'nooverwrites': True,
                        'noplaylist': True,
                        'ignoreerrors': True,
                        # 'download_archive': 'downloads.csv',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'logger': MyLogger(),
                        'progress_hooks': [my_hook],
                        }
        url_iter = iter(extract_urls(self.import_json()))
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            for url in url_iter:
                ydl.download([url])
                Pymp.var1.set('Ready')
                wait(1)
                Pymp.status_bar.set('Ready')
            Pymp.var2.set('')
                # try:    
                #     ydl.download([url])
                #     Pymp.var1.set('Ready')
                #     wait(1)
                #     Pymp.status_bar.set('Ready')
                # except:
                #     continue
                # else:
                #     Pymp.var2.set('')
                #     Pymp.var1.set('Ready')
                #     wait(1)
                #     Pymp.status_bar.set('Ready')

    def refresh_threads(self):
        self.t3 = threading.Thread(target=self.batch_download)
        self.t3.start()




app = Pymp()
app.mainloop()
