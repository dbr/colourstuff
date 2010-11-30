#!/usr/bin/python

# togglebutton.py

import os
import sys
import signal
from PyQt4 import QtGui
from PyQt4 import QtCore

import pyspotread


class ClickableWidget(QtGui.QWidget):
    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL("clicked()"))


class SamplerThread(QtCore.QThread):
    def __init__(self,parent=None, sampler = None):
        QtCore.QThread.__init__(self,parent)
        self.sampler = sampler

    def run(self):
        try:
            XYZ = self.sampler.sample()
        except Exception, e:
            self.emit(QtCore.SIGNAL("SampleError(int, str)"), self.sampler.port, str(e))
        else:
            X, Y, Z = XYZ.X, XYZ.Y, XYZ.Z
            self.emit(QtCore.SIGNAL("SampleOkay(int, float, float, float)"), self.sampler.port, X, Y, Z)



class ProbeComparer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ProbeComparer, self).__init__(parent)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        self.setWindowTitle('Probe Comparer')

        self.setGeometry(500, 400, 800, 600)

        # Swatches for probes
        self.patch1 = ClickableWidget(self)
        self.patch2 = ClickableWidget(self)
        self.patch3 = ClickableWidget(self)

        self.patch1.setMinimumWidth(300)
        self.patch2.setMinimumWidth(300)
        self.patch3.setMinimumWidth(300)

        self.patch1.setMinimumHeight(300)
        self.patch2.setMinimumHeight(300)
        self.patch3.setMinimumHeight(300)

        self.patch1.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")
        self.patch2.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")
        self.patch3.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")

        self.patch1.show()
        self.patch2.show()
        self.patch3.show()
        self.patch1.setAutoFillBackground(True)
        self.patch2.setAutoFillBackground(True)
        self.patch3.setAutoFillBackground(True)

        self.connect(self.patch1, QtCore.SIGNAL('clicked()'), lambda:self.set_reference(1))
        self.connect(self.patch2, QtCore.SIGNAL('clicked()'), lambda:self.set_reference(2))
        self.connect(self.patch3, QtCore.SIGNAL('clicked()'), lambda:self.set_reference(3))


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
        row2.addWidget(self.info2)

        row3 = QtGui.QVBoxLayout()
        row3.addWidget(self.title3)
        row3.addWidget(self.patch3)
        row3.addWidget(self.info3)


        # Create columns for each row
        patch_cols = QtGui.QHBoxLayout()
        patch_cols.addLayout(row1)
        patch_cols.addLayout(row2)
        patch_cols.addLayout(row3)

        self.sample = QtGui.QPushButton('Sample', self)
        self.connect(self.sample, QtCore.SIGNAL('clicked()'), self.do_sample)

        self.colour = QtGui.QComboBox(self)
        self.colour.addItem("Black")
        self.colour.addItem("Grey")
        self.colour.addItem("White")
        self.colour.addItem("Red")
        self.colour.addItem("Green")
        self.colour.addItem("Blue")

        self.connect(self.colour, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_patches)

        button_cols = QtGui.QHBoxLayout()
        button_cols.addWidget(self.colour)
        button_cols.addWidget(self.sample)

        patch_and_button_rows = QtGui.QVBoxLayout()

        patch_and_button_rows.addLayout(patch_cols)
        patch_and_button_rows.addLayout(button_cols)

        self.setLayout(patch_and_button_rows)

        self.center()

        self.spotread1 = pyspotread.Spotread(
            cmd = os.path.expanduser("~/Desktop/Argyll_V1.1.1/bin/spotread"),
            port = 1,
            lcd = True)

        self.spotread2 = pyspotread.Spotread(
            cmd = os.path.expanduser("~/Desktop/Argyll_V1.1.1/bin/spotread"),
            port = 2,
            lcd = True)

        self.spotread3 = pyspotread.Spotread(
            cmd = os.path.expanduser("~/Desktop/Argyll_V1.1.1/bin/spotread"),
            port = 3,
            lcd = True)

        self.last_readings = {}

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

    def sampler_done(self, patchnum, X, Y, Z):
        print "Sample %s is done" % patchnum
        sample = pyspotread.XYZ(X, Y, Z)
        mappy = {1: self.info1,
                 2: self.info2,
                 3: self.info3}

        try:
            infostr = str(sample)
        except ValueError, e:
            infostr = str(e)

        mappy[patchnum].setText(infostr)

        self.last_readings[patchnum] = sample

    def sampler_error(self, patchnum, errstr):
        mappy = {1: self.info1,
                 2: self.info2,
                 3: self.info3}

        mappy[patchnum].setText(errstr)



    def do_sample(self):
        if self.spotread1 is not None:
            collector1 = SamplerThread(self, sampler = self.spotread1)
            self.connect(collector1, QtCore.SIGNAL("SampleOkay(int, float, float, float)"), self.sampler_done)
            self.connect(collector1, QtCore.SIGNAL("SampleError(int, QString)"), self.sampler_error)
            collector1.start()

        if self.spotread2 is not None:
            collector2 = SamplerThread(self, sampler = self.spotread2)
            self.connect(collector2, QtCore.SIGNAL("SampleOkay(int, float, float, float)"), self.sampler_done)
            self.connect(collector2, QtCore.SIGNAL("SampleError(int, QString)"), self.sampler_error)
            collector2.start()

        if self.spotread3 is not None:
            collector3 = SamplerThread(self, sampler = self.spotread3)
            self.connect(collector3, QtCore.SIGNAL("SampleOkay(int, float, float, float)"), self.sampler_done)
            self.connect(collector3, QtCore.SIGNAL("SampleError(int, QString)"), self.sampler_error)
            collector3.start()

    def set_reference(self, num):
        print "setting reference"

    def set_patches(self, x):
        colmap = {
            'White': (255, 255, 255),
            'Grey': (128, 128, 128),
            'Black': (0, 0, 0),
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255)}

        for p in [self.patch1, self.patch2, self.patch3]:
            p.setStyleSheet("QWidget { background-color: rgb(%d, %d, %d) }" % colmap[str(x)])
            p.show()
            p.setAutoFillBackground(True)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    tb = ProbeComparer()
    tb.show()
    app.exec_()
