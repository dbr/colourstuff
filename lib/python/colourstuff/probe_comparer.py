#!/usr/bin/python

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
            import traceback
            estr = traceback.format_exc()
            self.emit(QtCore.SIGNAL("SampleError(int, QString)"), self.sampler.port, estr)
        else:
            X, Y, Z = XYZ.X, XYZ.Y, XYZ.Z
            self.emit(QtCore.SIGNAL("SampleOkay(int, float, float, float)"), self.sampler.port, X, Y, Z)



class ProbeComparer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ProbeComparer, self).__init__(parent)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        self.setWindowTitle('Probe Comparer')

        self.setGeometry(500, 400, 800, 600)

        all_patches = QtGui.QHBoxLayout()
        for probenum in range(2):
            patch = ClickableWidget(self)
            patch.setMinimumWidth(300)
            patch.setMinimumHeight(300)
            patch.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")
            patch.show()
            patch.setAutoFillBackground(True)

            self.connect(patch, QtCore.SIGNAL('clicked()'), lambda probenum=probenum:self.set_reference(probenum))

            title = QtGui.QLabel('Probe %d' % probenum)
            title.setMaximumHeight(25)

            info = QtGui.QTextEdit()

            patch_col = QtGui.QVBoxLayout()
            patch_col.addWidget(title)
            patch_col.addWidget(patch)
            patch_col.addWidget(info)

            all_patches.addLayout(patch_col)


        # Overall sample button
        sample_button = QtGui.QPushButton('Sample', self)
        self.connect(sample_button, QtCore.SIGNAL('clicked()'), self.do_sample)

        self.patch_colours = {
            "Black": (0, 0, 0),
            "Grey": (0.5, 0.5, 0.5),
            "White": (1, 1, 1),
            "Red": (1, 0, 0),
            "Green": (0, 1, 0),
            "Blue": (0, 0, 1),
        }

        colour_dropdown = QtGui.QComboBox(self)
        for k in self.patch_colours:
            colour_dropdown.addItem(k)

        self.connect(colour_dropdown, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_patches)

        button_cols = QtGui.QHBoxLayout()
        button_cols.addWidget(colour_dropdown)
        button_cols.addWidget(sample_button)


        patch_and_button_rows = QtGui.QVBoxLayout()

        patch_and_button_rows.addLayout(all_patches)
        patch_and_button_rows.addLayout(button_cols)

        self.setLayout(patch_and_button_rows)

        self.center()

        self.spotread1 = pyspotread.Spotread(
            port = 1,
            lcd = True)

        self.spotread2 = pyspotread.Spotread(
            port = 2,
            lcd = True)

        self.spotread3 = pyspotread.Spotread(
            port = 3,
            lcd = True)

        self.last_readings = {}

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

        infostr = str(sample)

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
