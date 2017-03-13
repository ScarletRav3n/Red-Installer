from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import (QWidget, QPushButton, QMessageBox, QLineEdit,
                             QTextEdit, QRadioButton, QLabel, QApplication)
import urllib.request
import os
import sys

__author__ = "ScarletRav3n"


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.large_font = QtGui.QFont("Arial", 12)
        self.reg_font = QtGui.QFont("Arial", 10)
        self.small_font = QtGui.QFont("Arial", 8)

        self.init_ui()

    def init_ui(self):

        # v.box
        gbox = QtWidgets.QGridLayout()
        box = QtWidgets.QVBoxLayout()
        self.rbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()

        # padding/margins
        gbox.setContentsMargins(0, 0, 0, 0)
        self.rbox.setContentsMargins(0, 0, 10, 10)
        self.hbox.setContentsMargins(0, 0, 10, 10)
        box.addStretch()
        self.hbox.addStretch()
        gbox.setSpacing(10)
        box.setSpacing(0)
        self.rbox.setSpacing(5)
        self.hbox.setSpacing(0)

        image = QtGui.QImage()
        image.loadFromData(urllib.request.urlopen('http://i.imgur.com/04DUqa3.png').read())
        png = QLabel(self)
        pixmap = QtGui.QPixmap(image)
        png.setPixmap(pixmap)
        gbox.addWidget(png, 0, 0, 1, 1, Qt.AlignTop)

        box.insertSpacing(1, 10)
        self.l1 = QLabel(self)
        self.l1.setWordWrap(True)
        self.large_font.setBold(True)
        self.l1.setFont(self.large_font)
        box.addWidget(self.l1, 0, Qt.AlignTop)

        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Sunken)
        gbox.addWidget(hline, 0, 0, 1, 3, Qt.AlignBottom)

        # start form
        self.python_ui()

        self.rbox.setAlignment(Qt.AlignTop)
        box.addLayout(self.rbox, 1)
        gbox.addLayout(box, 0, 1, 1, 2)
        gbox.addLayout(self.hbox, 1, 0, 1, 3)
        self.setLayout(gbox)

        # window
        self.setFixedSize(490, 400)
        self.setWindowIcon(QtGui.QIcon('red.ico'))
        self.setWindowTitle('Red Discord Bot - Setup')
        self.show()

    def buttons_panel(self):
        self.b1 = QPushButton("Back", self)
        self.b1.setMaximumWidth(75)
        self.hbox.addWidget(self.b1, 0, Qt.AlignRight)
        self.b2 = QPushButton("Next >", self)
        self.b2.setMaximumWidth(75)
        self.hbox.addWidget(self.b2, 0, Qt.AlignRight)
        self.hbox.insertSpacing(20, 20)
        self.b3 = QPushButton("Cancel", self)
        self.b3.setMaximumWidth(75)
        self.hbox.addWidget(self.b3, 0, Qt.AlignRight)

    def python_ui(self):
        self.clear_layout(self.rbox)
        self.clear_layout(self.hbox)
        self.hbox.addStretch()
        self.l1.setText("Installing requirements")

        self.process = QProcess()
        self.output = QTextEdit()

        self.rbox.insertSpacing(1, 10)
        l2 = QLabel('La La Land')
        self.rbox.addWidget(l2, 0, Qt.AlignTop)

        b5 = QPushButton("Dialog", self)
        b5.setMaximumWidth(75)

        self.rbox.addWidget(b5)
        self.rbox.addWidget(self.output)
        self.process.readyRead.connect(self.console_data)
        self.output.hide()

        # data flow
        interpreter = None

        if sys.platform == 'linux' or sys.platform == 'linux2':
            print("linux")
        if sys.platform == 'darwin':
            print('mac')
        if sys.platform == 'win32':
            print('win')
            interpreter = "pkg\python\python-3.6.1rc1.exe"
        args = ["PrependPath=1 Include_test=0"]

        # do call
        self.process.start(interpreter, args)
        if self.process.waitForFinished(-1):
            print('done')
        # self.process.start(interpreter, args)

        # buttons
        self.buttons_panel()

        # binds
        self.b1.setEnabled(True)
        # self.b1.clicked.connect(self.req_ui)
        self.b1.clicked.connect(self.process.close)
        # self.b2.clicked.connect(self.token_ui)
        self.b3.clicked.connect(self.close_prompt)
        b5.clicked.connect(self.console_hide)

    def console_hide(self):
        if self.output.isVisible():
            self.output.hide()
        else:
            self.output.show()

    def console_data(self):
        js = str(self.process.readAll(), 'utf-8')

        cursor = self.output.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(js)
        self.output.ensureCursorVisible()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def close_prompt(self):
        cbox = self.QMessageBox.warning(self,
                                        "Info",
                                        "Are you sure you want to cancel Red setup?",
                                        QMessageBox.Yes, QMessageBox.No)
        if cbox == QMessageBox.Yes:
            self.close()
        else:
            return

    def finish_prompt(self):
        self.QMessageBox.information(self,
                                     "Done!",
                                     "Red has been configured.",
                                     QMessageBox.Ok)
        self.settings.save_settings()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
