#!/usr/bin/python

# togglebutton.py

import os
import sys
import signal
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QThread

import pyspotread
from common import clamp


class Worker(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)

    def run(self):
        print "blah"

class ProbeComparer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ProbeComparer, self).__init__(parent)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        self.setWindowTitle('Probe Comparer')

        self.setGeometry(500, 400, 800, 600)

        # Swatches for probes

        self.patch1 = QtGui.QWidget(self)
        self.patch2 = QtGui.QWidget(self)
        self.patch3 = QtGui.QWidget(self)

        self.patch1.setMinimumWidth(300)
        self.patch2.setMinimumWidth(300)
        self.patch3.setMinimumWidth(300)

        self.patch1.setMinimumHeight(300)
        self.patch2.setMinimumHeight(300)
        self.patch3.setMinimumHeight(300)

        self.patch1.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")
        self.patch2.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")
        self.patch3.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")


        # Titles
        self.title1 = QtGui.QLabel('Probe 1')
        self.title2 = QtGui.QLabel('Probe 2')
        self.title3 = QtGui.QLabel('Probe 3')

        self.title1.setMaximumHeight(25)
        self.title2.setMaximumHeight(25)
        self.title3.setMaximumHeight(25)

        self.info1 = QtGui.QTextEdit()
        self.info2 = QtGui.QTextEdit()
        self.info3 = QtGui.QTextEdit()

        # Create each column
        row1 = QtGui.QVBoxLayout()
        row1.addWidget(self.title1)
        row1.addWidget(self.patch1)
        row1.addWidget(self.info1)

        row2 = QtGui.QVBoxLayout()
        row2.addWidget(self.title2)
        row2.addWidget(self.patch2)
        row2.addWidget(self.info3)

        row3 = QtGui.QVBoxLayout()
        row3.addWidget(self.title3)
        row3.addWidget(self.patch3)
        row3.addWidget(self.info3)


        # Create columns for each row
        patch_cols = QtGui.QHBoxLayout()
        patch_cols.addStretch(1)
        patch_cols.addLayout(row1)
        patch_cols.addLayout(row2)
        patch_cols.addLayout(row3)
        patch_cols.addStretch(10)

        self.sample = QtGui.QPushButton('Sample', self)
        self.connect(self.sample, QtCore.SIGNAL('clicked()'), self.do_sample)

        button_cols = QtGui.QHBoxLayout()
        button_cols.addWidget(self.sample)

        patch_and_button_rows = QtGui.QVBoxLayout()

        patch_and_button_rows.addLayout(patch_cols)
        patch_and_button_rows.addLayout(button_cols)

        self.setLayout(patch_and_button_rows)

        self.center()

        self.spotread = pyspotread.Spotread(
            cmd = os.path.expanduser("~/Applications/Media/Argyll_V1.3.2/bin/spotread"),
            port = 1,
            lcd = True)

    """
    def keyPressEvent(self, event):
        key = event.key()
        keys = [getattr(QtCore.Qt, "Key_%d" % x) for x in (1, 2, 3)]
        if key in keys:
            number = keys.index(key)+1
            self.do_sample(number)
    """

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def do_sample(self):
        sample = self.spotread.sample()
        r, g, b = sample.to_srgb()
        self.set_colour(r, g, b)

    def set_colour(self, r, g, b):
        print r, g, b
        r, g, b = [clamp(x*255, 0, 255) for x in (r, g, b)]
        self.patch1.setStyleSheet("QWidget { background-color: rgb(%d, %d, %d) }" % (r, g, b))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    tb = ProbeComparer()
    tb.show()
    app.exec_()
