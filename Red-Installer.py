from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QProcess, QThread
from PyQt5.QtWidgets import (QWidget, QPushButton, QMessageBox, QLineEdit,
                             QMainWindow, QFileDialog, QLabel, QApplication)
import threading
import urllib.request
import tarfile
import time
import sys
import os


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.large_font = QtGui.QFont("Arial", 16)
        self.reg_font = QtGui.QFont("Arial", 10)
        self.small_font = QtGui.QFont("Arial", 8)

        self.init_ui()

    def init_ui(self):
        css = ("color: white; "
               "font-weight: bold")

        # vbox
        hbox = QtWidgets.QHBoxLayout()
        bbox = QtWidgets.QHBoxLayout()
        self.rbox = QtWidgets.QGridLayout()

        hbox.setContentsMargins(0, 0, 0, 0)
        bbox.setContentsMargins(0, 5, 5, 0)
        self.rbox.setContentsMargins(0, 0, 0, 0)
        bbox.addStretch()
        hbox.setSpacing(0)
        bbox.setSpacing(0)

        # title
        self.l1 = QLabel(self)
        self.l1.setFont(self.large_font)
        self.l1.setStyleSheet(css)
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setColor(QtGui.QColor("#5e5e5e"))
        shadow.setOffset(2, 2)
        self.l1.setGraphicsEffect(shadow)
        hbox.addWidget(self.l1, 0, Qt.AlignCenter)

        # buttons
        b1 = QPushButton("─", self)
        b1.setFont(self.reg_font)
        b1.setStyleSheet(css)
        b1.setMaximumWidth(25)
        b1.setFlat(True)
        bbox.addWidget(b1, 0, Qt.AlignRight)
        b2 = QPushButton("X", self)
        b2.setFont(self.reg_font)
        b2.setStyleSheet(css)
        b2.setMaximumWidth(25)
        b2.setFlat(True)
        bbox.addWidget(b2, 0, Qt.AlignRight)

        # start
        self.download = Download()
        self.download.start()

        self.b5 = QPushButton("Downloading...", self)
        self.b5.setFont(self.large_font)
        # self.b5.setMinimumSize(50, 200)
        self.b5.setEnabled(False)
        self.rbox.addWidget(self.b5, 0, 0, 2, 1, Qt.AlignCenter)

        # if self.download.done is True:
        #     self.b5.setText("Install Red")
        #     self.b5.setEnabled(True)

        # bind
        b1.clicked.connect(self.showMinimized)
        b2.clicked.connect(self.close)
        self.b5.clicked.connect(self.req_ui)
        self.download.finished.connect(self.finish_check)

        self.rbox.addLayout(bbox, 0, 0, 1, 1)
        self.rbox.addLayout(hbox, 0, 0, 2, 1)
        self.setLayout(self.rbox)

        # bg
        bgimg = QtGui.QImage()
        bgimg.loadFromData(urllib.request.urlopen('http://i.imgur.com/VW9eF72.jpg').read())
        bg = QtGui.QPalette()
        bg.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(bgimg)))

        # window
        self.setFixedSize(400, 150)
        self.setPalette(bg)
        self.setWindowTitle('Red Discord Bot - Setup')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.show()

    def finish_check(self):
        self.b5.setText(' Install Red ')
        self.b5.setEnabled(True)

    def req_ui(self):
        self.b5.deleteLater()
        self.l1.setText('INSTALLING REQUIREMENTS')
        self.process = QProcess()

        if sys.platform == 'linux' or sys.platform == 'linux2':
            self.process.start('sudo add-apt-repository ppa:fkrull/deadsnakes -y')
            self.process.waitForFinished(-1)
            self.process.start('sudo apt-get install python3.5-dev build-essential '
                               'libssl-dev libffi-dev git ffmpeg libopus-dev unzip -y')
            self.process.waitForFinished(-1)
            self.process.start('wget https://bootstrap.pypa.io/get-pip.py')
            self.process.waitForFinished(-1)
            self.process.start('sudo python3.5 get-pip.py')
            self.process.waitForFinished(-1)
            self.red_clone()

        elif sys.platform == 'darwin':
            self.process.start(' /usr/bin/ruby -e "$(curl -fsSL '
                               'https://raw.githubusercontent.com/Homebrew/install/master/install)"')
            self.process.waitForFinished(-1)
            self.process.start('brew install python3 --with-brewed-openssl')
            self.process.waitForFinished(-1)
            self.process.start('brew install git')
            self.process.waitForFinished(-1)
            self.process.start('brew install ffmpeg --with-ffplay')
            self.process.waitForFinished(-1)
            self.process.start('brew install opus')
            self.process.waitForFinished(-1)
            self.red_clone()

        elif sys.platform == 'win32':
            self.exe = Exe()
            self.exe.start()
            self.exe.finished.connect(self.red_clone)

    def red_clone(self):
        self.process.start('git config --global core.longpaths true')
        self.process.waitForFinished(-1)
        QMessageBox.information(self, 'Info', "Choose where to install Red")
        fdir = QFileDialog.getExistingDirectory(self, 'Open Folder')

        self.process.start('git clone -b develop --single-branch '
                           'https://github.com/Twentysix26/Red-DiscordBot.git ' + fdir)
        print('git clone -b develop --single-branch '
              'https://github.com/Twentysix26/Red-DiscordBot.git ' + fdir)
        self.process.waitForFinished(-1)
        print('daneun?')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


class Download(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        print('yes?')
        if sys.platform == 'win32':
            if not os.path.exists("pkg"):
                os.makedirs("pkg")

            if not os.path.exists("pkg\python-3.6.1rc1.exe"):
                urllib.request.urlretrieve('https://www.python.org/ftp/python/3.6.1/python-3.6.1rc1-webinstall.exe',
                                           'pkg\python-3.6.1rc1.exe')

            if not os.path.exists("pkg\Git-2.12.0-64-bit.exe"):
                urllib.request.urlretrieve('https://github.com/git-for-windows/git/releases/download/'
                                           'v2.12.0.windows.1/Git-2.12.0-64-bit.exe', 'pkg\Git-2.12.0-64-bit.exe')
        print('done')
        self.quit()


class Exe(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.process = QProcess()
        if sys.executable is None:
            self.process.start('pkg\python-3.6.1rc1.exe PrependPath=1 Include_test=0')
            self.process.waitForFinished(-1)

        self.process.start('pkg\Git-2.12.0-64-bit.exe /SILENT')
        self.process.waitForFinished(-1)
        self.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
