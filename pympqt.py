import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import youtube_dl
import time


test_url = 'https://www.youtube.com/watch?v=YgGzAKP_HuM'


# class MyLogger(qtc.QRunnable):
#     status = qtc.pyqtSignal(str)
#     def run(self):
#         pass

#     def debug(self, msg):
#         self.status.emit(msg)
#         # pass

#     def warning(self, msg):
#         pass

#     def error(self, msg):
#         self.status.emit(msg)
#         # pass


# def my_hook(d):
#     if d['status'] == 'finished':
#         mw.change_status("Download complete, now converting...")
#     elif d['status'] == 'downloading':
#         mw.statusBar().showMessage("Downloading...", d['_percent_str'])
# #     pass


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PYMP')
        self.setFixedSize(300, 175)
        self.setCentralWidget(MainWidget())
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction('Import Bookmarks')
        file_menu.addSeparator()
        file_menu.addAction('Quit', self.close)
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction('Help')
        help_menu.addAction('About')
        self.statusBar().showMessage('Ready')

        # self.threadpool = qtc.QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.show()

    @qtc.pyqtSlot()
    def change_status(self, msg):
        self.statusBar().showMessage(msg)


class MainWidget(qtw.QWidget):
    radio = ''
    status_signal = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.elements()
        self.show()

    def elements(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        label = qtw.QLabel('Paste URL here:')
        self.paste_field = qtw.QLineEdit()
        self.dld_btn = qtw.QPushButton('Download')
        self.dld_btn.clicked.connect(self.download)
        self.mp3_radio = qtw.QRadioButton('MP3')
        self.mp3_radio.toggled.connect(self.FormatSelector)
        self.mp4_radio = qtw.QRadioButton('MP4')
        self.mp4_radio.toggled.connect(self.FormatSelector)
        self.status_signal.connect(MainWindow.change_status)

        container.layout().addWidget(label, 0,0,1,3)
        container.layout().addWidget(self.paste_field,1,0,1,5)
        container.layout().addWidget(self.dld_btn,3,0,1,5)
        container.layout().addWidget(self.mp3_radio,2,0,1,2)
        container.layout().addWidget(self.mp4_radio,2,2,1,2)
        self.layout().addWidget(container)


    def FormatSelector(self):
        radioBtn = self.sender()

        if radioBtn.isChecked():
            self.radio = radioBtn.text()

            if self.radio == 'MP3':
                mw.change_status('MP3 selected')

            elif self.radio == 'MP4':
                mw.change_status('MP4 selected')

    def paster(self):
        self.url = self.paste_field.text()
        return self.url



    def download(self):
        # worker = MyLogger()
        # mw.threadpool.start(worker)
        ydl_opts_mp3 = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192', 
                    }],
                # 'logger': MyLogger(),
                # 'progress_hooks': [my_hook],
            }

        ydl_opts_mp4 = {
                'format': 'best[ext=mp4]',
                # 'logger': MyLogger(),
                # 'progress_hooks': [my_hook],
            }

        url = self.paster()
        print(url)

        if self.radio == 'MP3':
            with youtube_dl.YoutubeDL(ydl_opts_mp3) as ydl:
                try:
                    ydl.download([url])
                    # mw.statusBar().showMessage('Ready')
                    mw.change_status('Ready')
                except:
                    mw.change_status('Error')
                    
        elif self.radio == 'MP4':
            mw.change_status('Starting Download...')
            with youtube_dl.YoutubeDL(ydl_opts_mp4) as ydl:
                try:
                    ydl.download([url])
                    mw.change_status('Ready')
                except:
                    mw.change_status('Error')


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
