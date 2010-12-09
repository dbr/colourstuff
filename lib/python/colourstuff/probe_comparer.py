#!/usr/bin/python

import os
import sys
import signal
from PyQt4 import QtGui
from PyQt4 import QtCore

import pyspotread
import common


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

        probe_names = pyspotread.list_probes()

        self.number_probes = len(probe_names)

        self.probe_meta = {}

        all_patches = QtGui.QHBoxLayout()
        for probenum in range(1, self.number_probes+1):
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

            self.probe_meta[probenum] = {
                'patch': patch,
                'info': info,
                'title': title}

            all_patches.addLayout(patch_col)


        # Patch-colour dropdown and Sample button row
        sample_button = QtGui.QPushButton('Sample', self)
        self.connect(sample_button, QtCore.SIGNAL('clicked()'), self.do_sample)


        self.patch_colours = common.ODict()
        self.patch_colours["Black"] = (0, 0, 0)
        self.patch_colours["Grey"] = (0.5, 0.5, 0.5)
        self.patch_colours["White"] = (1, 1, 1)
        self.patch_colours["Red"] = (1, 0, 0)
        self.patch_colours["Green"] = (0, 1, 0)
        self.patch_colours["Blue"] = (0, 0, 1)

        colour_dropdown = QtGui.QComboBox(self)
        for k in self.patch_colours:
            colour_dropdown.addItem(k)

        self.connect(colour_dropdown, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_patches)

        button_cols = QtGui.QHBoxLayout()
        button_cols.addWidget(colour_dropdown)
        button_cols.addWidget(sample_button)


        # First row is patches, second row is buttons
        patch_and_button_rows = QtGui.QVBoxLayout()
        patch_and_button_rows.addLayout(all_patches)
        patch_and_button_rows.addLayout(button_cols)

        self.setLayout(patch_and_button_rows)

        self.center()

        self.probes = {}
        for probenum in range(1, self.number_probes+1):
            self.probes[probenum] = pyspotread.Spotread(
                port = probenum,
                lcd = True)

            name = probe_names[probenum]
            self.probe_meta[probenum]['title'].setText(
                "Probe %s (%s)" % (probenum, name))

        self.last_readings = {}

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def sampler_done(self, patchnum, X, Y, Z):
        print "Sample %s is done" % patchnum
        sample = pyspotread.XYZ(X, Y, Z)

        infostr = str(sample)

        self.probe_meta[patchnum]['info'].setText(infostr)

        self.last_readings[patchnum] = sample
        for otherpnum, reading in self.last_readings.items():
            if otherpnum != patchnum:
                delta = pyspotread.deltaE(reading, sample)
                print "delta from %s to %s is... %s" % (patchnum, otherpnum, delta)

    def sampler_error(self, patchnum, errstr):
        self.probe_meta[patchnum]['info'].setText(errstr)

    def do_sample(self):
        for probenum, spotread in self.probes.items():
            collector = SamplerThread(self, sampler = spotread)
            self.connect(collector, QtCore.SIGNAL("SampleOkay(int, float, float, float)"), self.sampler_done)
            self.connect(collector, QtCore.SIGNAL("SampleError(int, QString)"), self.sampler_error)
            collector.start()

    def set_reference(self, num):
        print "setting reference"

    def set_patches(self, x):
        rgb = self.patch_colours[str(x)]
        rgb = tuple(common.clamp(x*255.0, 0, 255) for x in rgb)
        for p in self.probe_meta.values():
            p['patch'].setStyleSheet("QWidget { background-color: rgb(%d, %d, %d) }" % rgb)
            p['patch'].show()
            p['patch'].setAutoFillBackground(True)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    tb = ProbeComparer()
    tb.show()
    app.exec_()
