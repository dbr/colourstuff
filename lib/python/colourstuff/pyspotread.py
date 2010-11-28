"""Tools to get colour readings from a monitor probe.

Primarily an interface to ArgyllCMS's spotread command, using pexpect.

Requires http://www.argyllcms.com (was developed with version 1.3.2)
"""

import os
import sys
import math
from decimal import Decimal

import pexpect

from colour_temp import correlated_colour_temp


class XYZ(object):
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def __repr__(self):
        return "XYZ(%s, %s, %s)" % tuple(str(a) for a in (self.X, self.Y, self.Z))

    def to_xyY(self):
        """
        http://en.wikipedia.org/wiki/CIE_1931_color_space#The_CIE_xy_chromaticity_diagram_and_the_CIE_xyY_color_space
        """
        X, Y, Z = self.X, self.Y, self.Z
        x = X / (X+Y+Z)
        y = Y / (X+Y+Z)
        return (x, y, Y)

    def cct(self):
        return correlated_colour_temp(self.X, self.Y, self.Z)


class Spotread(object):
    """Wrapper for the ArgyllCMS spotread command, which allows reading of
    values from various monitor probes.
    """
    def __init__(self, cmd = "spotread", port = 1, lcd = False, crt = False):
        if not (lcd or crt) and not (lcd and crt):
            raise ValueError("Either lcd or crt must be True")

        if lcd:
            display_type = "l"
        elif crt:
            display_type = "c"

        self.cmd = "%s -y %s -c %s" % (cmd, display_type, port)
        self.proc = pexpect.spawn(self.cmd)

    def sample(self):
        self.proc.expect(".*any other key to take a reading:")
        self.proc.send(" ")
        self.proc.expect("Result is XYZ: (\d+\.\d+) (\d+\.\d+) (\d+\.\d+),")
        X, Y, Z = [float(x) for x in self.proc.match.groups()]
        return XYZ(X, Y, Z)

    def quit(self):
        self.proc.expect(".*any other key to take a reading:")
        self.proc.send("q")
        self.proc.send("q")


if __name__ == '__main__':
    sr = Spotread(
        cmd = os.path.expanduser("~/Applications/Media/Argyll_V1.3.2/bin/spotread"),
        port = 1,
        lcd = True)

    sample = sr.sample()
    sr.quit()

    X, Y, Z = sample.X, sample.Y, sample.Z
    x, y, _ = sample.to_xyY()
    cct = sample.cct()

    def format_float(a):
        return ("%.04f" % a).rjust(7)

    print "X, Y, Z : %s, %s, %s" % tuple(format_float(a) for a in (X, Y, Z))
    print "x, y, Y : %s, %s, %s" % tuple(format_float(a) for a in (x, y, Y))
    print "CCT (K) : %s" % cct
