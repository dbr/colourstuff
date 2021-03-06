"""CIE 1931 Standard Colorimetric Observer colour matching functions
"""

def from_txt_to_python(angle = "2"):
    """Parses the files from http://www.cie.co.at/main/freepubs.html

    Prints a chunk of copy-and-pastable Python code containing a dict
    of wavelengths->values, which can be used to implement the
    colour-matching functions without parsing text files
    """
    def load_txt(f):
        f.readline()
        mapping = {}
        for line in f:
            if line.startswith("Sum"): continue
            wavelen_nm, value = line.split()
            mapping[int(wavelen_nm)] = int(value.replace(",", ""))
        return mapping

    def get_data_file(fname):
        import os
        data_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "cie1931_data",
            fname)
        return data_dir

    cie1931_standard_observer_2deg = {}
    cie1931_standard_observer_2deg['x'] = load_txt(open(get_data_file('x%s.txt' % angle)))
    cie1931_standard_observer_2deg['y'] = load_txt(open(get_data_file('y%s.txt' % angle)))
    cie1931_standard_observer_2deg['z'] = load_txt(open(get_data_file('z%s.txt' % angle)))


    print "cie1931_standard_observer_%sdeg = {" % angle
    for chan in ('x', 'y', 'z'):
        print "    %r: {" % chan
        for wavelen, value in sorted(cie1931_standard_observer_2deg[chan].items()):
            print "        %s: %s," % (wavelen, value)
        print "    },"
    print "}"


def cie1931_standard_observer_rawdata(two_degree = False, ten_degree = False):
    """Returns dictionary with three keys: x, y and z. Each key contains
    a dictionary mapping wavelength to value
    
    Created using the from_txt_to_python function
    """

    if not any([two_degree, ten_degree]) or all([two_degree, ten_degree]):
        raise ValueError("Specify either two_degree or ten_degree")

    cie1931_standard_observer_2deg = {
        'x': {
            380: 1368,
            385: 2236,
            390: 4243,
            395: 7650,
            400: 14310,
            405: 23190,
            410: 43510,
            415: 77630,
            420: 134380,
            425: 214770,
            430: 283900,
            435: 328500,
            440: 348280,
            445: 348060,
            450: 336200,
            455: 318700,
            460: 290800,
            465: 251100,
            470: 195360,
            475: 142100,
            480: 95640,
            485: 57950,
            490: 32010,
            495: 14700,
            500: 4900,
            505: 2400,
            510: 9300,
            515: 29100,
            520: 63270,
            525: 109600,
            530: 165500,
            535: 225750,
            540: 290400,
            545: 359700,
            550: 433450,
            555: 512050,
            560: 594500,
            565: 678400,
            570: 762100,
            575: 842500,
            580: 916300,
            585: 978600,
            590: 1026300,
            595: 1056700,
            600: 1062200,
            605: 1045600,
            610: 1002600,
            615: 938400,
            620: 854450,
            625: 751400,
            630: 642400,
            635: 541900,
            640: 447900,
            645: 360800,
            650: 283500,
            655: 218700,
            660: 164900,
            665: 121200,
            670: 87400,
            675: 63600,
            680: 46770,
            685: 32900,
            690: 22700,
            695: 15840,
            700: 11359,
            705: 8111,
            710: 5790,
            715: 4109,
            720: 2899,
            725: 2049,
            730: 1440,
            735: 1000,
            740: 690,
            745: 476,
            750: 332,
            755: 235,
            760: 166,
            765: 117,
            770: 83,
            775: 59,
            780: 42,
        },
    'y': {
            380: 39,
            385: 64,
            390: 120,
            395: 217,
            400: 396,
            405: 640,
            410: 1210,
            415: 2180,
            420: 4000,
            425: 7300,
            430: 11600,
            435: 16840,
            440: 23000,
            445: 29800,
            450: 38000,
            455: 48000,
            460: 60000,
            465: 73900,
            470: 90980,
            475: 112600,
            480: 139020,
            485: 169300,
            490: 208020,
            495: 258600,
            500: 323000,
            505: 407300,
            510: 503000,
            515: 608200,
            520: 710000,
            525: 793200,
            530: 862000,
            535: 914850,
            540: 954000,
            545: 980300,
            550: 994950,
            555: 1000000,
            560: 995000,
            565: 978600,
            570: 952000,
            575: 915400,
            580: 870000,
            585: 816300,
            590: 757000,
            595: 694900,
            600: 631000,
            605: 566800,
            610: 503000,
            615: 441200,
            620: 381000,
            625: 321000,
            630: 265000,
            635: 217000,
            640: 175000,
            645: 138200,
            650: 107000,
            655: 81600,
            660: 61000,
            665: 44580,
            670: 32000,
            675: 23200,
            680: 17000,
            685: 11920,
            690: 8210,
            695: 5723,
            700: 4102,
            705: 2929,
            710: 2091,
            715: 1484,
            720: 1047,
            725: 740,
            730: 520,
            735: 361,
            740: 249,
            745: 172,
            750: 120,
            755: 85,
            760: 60,
            765: 42,
            770: 30,
            775: 21,
            780: 15,
            },
        'z': {
            380: 6450,
            385: 10550,
            390: 20050,
            395: 36210,
            400: 67850,
            405: 110200,
            410: 207400,
            415: 371300,
            420: 645600,
            425: 1039050,
            430: 1385600,
            435: 1622960,
            440: 1747060,
            445: 1782600,
            450: 1772110,
            455: 1744100,
            460: 1669200,
            465: 1528100,
            470: 1287640,
            475: 1041900,
            480: 812950,
            485: 616200,
            490: 465180,
            495: 353300,
            500: 272000,
            505: 212300,
            510: 158200,
            515: 111700,
            520: 78250,
            525: 57250,
            530: 42160,
            535: 29840,
            540: 20300,
            545: 13400,
            550: 8750,
            555: 5750,
            560: 3900,
            565: 2750,
            570: 2100,
            575: 1800,
            580: 1650,
            585: 1400,
            590: 1100,
            595: 1000,
            600: 800,
            605: 600,
            610: 340,
            615: 240,
            620: 190,
            625: 100,
            630: 50,
            635: 30,
            640: 20,
            645: 10,
            650: 0,
            655: 0,
            660: 0,
            665: 0,
            670: 0,
            675: 0,
            680: 0,
            685: 0,
            690: 0,
            695: 0,
            700: 0,
            705: 0,
            710: 0,
            715: 0,
            720: 0,
            725: 0,
            730: 0,
            735: 0,
            740: 0,
            745: 0,
            750: 0,
            755: 0,
            760: 0,
            765: 0,
            770: 0,
            775: 0,
            780: 0,
        },
    }

    cie1931_standard_observer_10deg = {
        'x': {
            380: 160,
            385: 662,
            390: 2362,
            395: 7242,
            400: 19110,
            405: 43400,
            410: 84736,
            415: 140638,
            420: 204492,
            425: 264737,
            430: 314679,
            435: 357719,
            440: 383734,
            445: 386726,
            450: 370702,
            455: 342957,
            460: 302273,
            465: 254085,
            470: 195618,
            475: 132349,
            480: 80507,
            485: 41072,
            490: 16172,
            495: 5132,
            500: 3816,
            505: 15444,
            510: 37465,
            515: 71358,
            520: 117749,
            525: 172953,
            530: 236491,
            535: 304213,
            540: 376772,
            545: 451584,
            550: 529826,
            555: 616053,
            560: 705224,
            565: 793832,
            570: 878655,
            575: 951162,
            580: 1014160,
            585: 1074300,
            590: 1118520,
            595: 1134300,
            600: 1123990,
            605: 1089100,
            610: 1030480,
            615: 950740,
            620: 856297,
            625: 754930,
            630: 647467,
            635: 535110,
            640: 431567,
            645: 343690,
            650: 268329,
            655: 204300,
            660: 152568,
            665: 112210,
            670: 81261,
            675: 57930,
            680: 40851,
            685: 28623,
            690: 19941,
            695: 13842,
            700: 9577,
            705: 6605,
            710: 4553,
            715: 3145,
            720: 2175,
            725: 1506,
            730: 1045,
            735: 727,
            740: 508,
            745: 356,
            750: 251,
            755: 178,
            760: 126,
            765: 90,
            770: 65,
            775: 46,
            780: 33,
        },
        'y': {
            380: 17,
            385: 72,
            390: 253,
            395: 769,
            400: 2004,
            405: 4509,
            410: 8756,
            415: 14456,
            420: 21391,
            425: 29497,
            430: 38676,
            435: 49602,
            440: 62077,
            445: 74704,
            450: 89456,
            455: 106256,
            460: 128201,
            465: 152761,
            470: 185190,
            475: 219940,
            480: 253589,
            485: 297665,
            490: 339133,
            495: 395379,
            500: 460777,
            505: 531360,
            510: 606741,
            515: 685660,
            520: 761757,
            525: 823330,
            530: 875211,
            535: 923810,
            540: 961988,
            545: 982200,
            550: 991761,
            555: 999110,
            560: 997340,
            565: 982380,
            570: 955552,
            575: 915175,
            580: 868934,
            585: 825623,
            590: 777405,
            595: 720353,
            600: 658341,
            605: 593878,
            610: 527963,
            615: 461834,
            620: 398057,
            625: 339554,
            630: 283493,
            635: 228254,
            640: 179828,
            645: 140211,
            650: 107633,
            655: 81187,
            660: 60281,
            665: 44096,
            670: 31800,
            675: 22602,
            680: 15905,
            685: 11130,
            690: 7749,
            695: 5375,
            700: 3718,
            705: 2565,
            710: 1768,
            715: 1222,
            720: 846,
            725: 586,
            730: 407,
            735: 284,
            740: 199,
            745: 140,
            750: 98,
            755: 70,
            760: 50,
            765: 36,
            770: 25,
            775: 18,
            780: 13,
        },
        'z': {
            380: 705,
            385: 2928,
            390: 10482,
            395: 32344,
            400: 86011,
            405: 197120,
            410: 389366,
            415: 656760,
            420: 972542,
            425: 1282500,
            430: 1553480,
            435: 1798500,
            440: 1967280,
            445: 2027300,
            450: 1994800,
            455: 1900700,
            460: 1745370,
            465: 1554900,
            470: 1317560,
            475: 1030200,
            480: 772125,
            485: 570060,
            490: 415254,
            495: 302356,
            500: 218502,
            505: 159249,
            510: 112044,
            515: 82248,
            520: 60709,
            525: 43050,
            530: 30451,
            535: 20584,
            540: 13676,
            545: 7918,
            550: 3988,
            555: 1091,
            560: 0,
            565: 0,
            570: 0,
            575: 0,
            580: 0,
            585: 0,
            590: 0,
            595: 0,
            600: 0,
            605: 0,
            610: 0,
            615: 0,
            620: 0,
            625: 0,
            630: 0,
            635: 0,
            640: 0,
            645: 0,
            650: 0,
            655: 0,
            660: 0,
            665: 0,
            670: 0,
            675: 0,
            680: 0,
            685: 0,
            690: 0,
            695: 0,
            700: 0,
            705: 0,
            710: 0,
            715: 0,
            720: 0,
            725: 0,
            730: 0,
            735: 0,
            740: 0,
            745: 0,
            750: 0,
            755: 0,
            760: 0,
            765: 0,
            770: 0,
            775: 0,
            780: 0,
        },
    }

    if two_degree:
        return cie1931_standard_observer_2deg
    else:
        return cie1931_standard_observer_10deg


from math import exp
def analytic_two_degree_x(wave):
    t1 = (wave-442.0)*((wave<442.0) and 0.0624 or 0.0374)
    t2 = (wave-599.8)*((wave<599.8) and 0.0264 or 0.0323)
    t3 = (wave-501.1)*((wave<501.1) and 0.0490 or 0.0382)
    return 0.362*exp(-0.5*t1*t1) + 1.056*exp(-0.5*t2*t2) - 0.065*exp(-0.5*t3*t3)

def analytic_two_degree_y(wave):
    t1 = (wave-568.8)*((wave<568.8) and 0.0213 or 0.0247);
    t2 = (wave-530.9)*((wave<530.9) and 0.0613 or 0.0322);
    return 0.821*exp(-0.5*t1*t1) + 0.286*exp(-0.5*t2*t2);

def analytic_two_degree_z(wave):
    t1 = (wave-437.0)*((wave<437.0) and 0.0845 or 0.0278)
    t2 = (wave-459.0)*((wave<459.0) and 0.0385 or 0.0725)
    return 1.217*exp(-0.5*t1*t1) + 0.681*exp(-0.5*t2*t2);


def get_colour_matching_functions(two_degree = False, ten_degree = False, analytic=False):
    """Get the three colour matching functions, based of the CIE 1931 Standard
    Colorimetric Observer (either the 2 or 10 degree observers)
    
    With analytic=False, the functions are based on the 5nm tabulated
    data, linearly interpolates between samples.

    With analytic=True, the functions use the analytic approximation
    of the colour matching curves from
    http://jcgt.org/published/0002/02/01/
    
    Returned as a tuple of three callables, which take a wavelength in
    nanometres, and return the reading.
    """

    if two_degree and analytic:
        return (analytic_two_degree_x, analytic_two_degree_y, analytic_two_degree_z)
    elif ten_degree and analytic:
        raise ValueError("Analytic ten degree curves not implemented")

    # Load the raw data
    data = cie1931_standard_observer_rawdata(two_degree = two_degree, ten_degree = ten_degree)

    # The outer function defines the channel, to prevent duplicating the
    # function three times.
    def getfunc(channel):
        # The inner function uses the channel variable, and does the
        # actual interpolation
        def colour_matcher(value):
            def lerp(a, b, mix):
                return b*mix + a*(1-mix)
            samples = sorted(data[channel])
            if value < min(samples):
                raise ValueError("Value %s below minimum sample: %s" % (value, min(samples)))
            if value > max(samples):
                raise ValueError("Value %s above minimum sample: %s" % (value, max(samples)))

            deltas = [abs(a - value) for a in samples]
            smallest = deltas.index(min(deltas))

            ka, kb = samples[smallest-1], samples[smallest]
            va, vb = data[channel][ka], data[channel][kb]
            interpolant = (float(value) - ka) / (kb - ka)
            return lerp(va, vb, interpolant)

        colour_matcher.__doc__ = "Colour matching function for %r" % channel
        return colour_matcher

    return (getfunc("x"), getfunc("y"), getfunc("z"))


if __name__ == '__main__':
    x, y, z = get_colour_matching_functions(two_degree = True)


    xes = [x(i) for i in range(380, 780)]
    yes = [y(i) for i in range(380, 780)]
    zes = [z(i) for i in range(380, 780)]

    # Normalise
    xes = [i/max(xes) for i in xes]
    yes = [i/max(yes) for i in yes]
    zes = [i/max(zes) for i in zes]

    for a in xes:
        print "*"*int(a*70)
    for a in yes:
        print "*"*int(a*70)
    for a in zes:
        print "*"*int(a*70)
