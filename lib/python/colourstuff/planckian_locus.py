def planckian_locus_approx(T):
    """http://en.wikipedia.org/wiki/Planckian_locus#Approximation
    """

    T = float(T)

    if 1667 <= T <= 4000:
        x = -0.2661239 * (10**9 / T**3) - 0.2343580 * (10**6/T**2) + 0.8776956 * (10**3/T) + 0.179910
    elif 4000 <= T <= 25000:
        x = -3.0258469 * (10**9 / T**3) + 2.107379 * (10**6/T**2) + 0.2226347*(10**3/T) + 0.240390
    else:
        raise ValueError("T out of range (should be between 1667K and 25000K)")

    if 1667 <= T <= 2222:
        y = -1.1063814 * x**3 - 1.34811020*x**2 + 2.18555832*x - 0.20219683
    elif 2222 <= T <= 4000:
        y = -0.9549476*x**3 - 1.37418593*x**2 + 2.09137015*x - 0.16748867
    elif 4000 <= T <= 25000:
        y = 3.0817580*x**3 - 5.87338670*x**2 + 3.75112997*x - 0.37001483
    else:
        raise ValueError("T out of range (should be between 1667K and 25000)")

    return (x, y)


def plancks_law(wavelen, T):
    """wavelen is in nanometres, and T is in Kelvin

    $I'(\lambda,T) =\frac{2 hc^2}{\lambda^5}\frac{1}{ e^{\frac{hc}{\lambda kT}}-1}$

    http://en.wikipedia.org/wiki/Planck%27s_law
    """

    #FIXME: Needs test cases, probably right, but maybe not

    from math import exp, pi

    nm = 10**-9 # nm to metres

    h = 6.6260689633*10**-34 # Planck constant
    k = 1.380650424*10**-23 # Boltzmann constant
    c = 299792458 # m/s (speed of light in a vacuum)
    c = 2.99792*10**8

    # Left-hand chunk of expression (that's the official maths
    # terminology, I'm sure)
    # http://www.wolframalpha.com/input/?i=%282*pi*h*c^2%29+%2F+5600nm^2
    p1 = (2*pi*h*(c**2)) / ((wavelen*nm)**5)

    # Right-hand chunk of expression
    # http://www.wolframalpha.com/input/?i=e^{%5Cfrac{%28Planck+constant%29%28speed+of+light+in+a+vacuum%29}{580nm+*+%28Boltzmann+constant%29+*+5600K}}
    p2 = 1.0 / (exp((h*c) / (wavelen*nm * k * T)) - 1)

    return p1 * p2


def integrate(f, a, b, N):
    dx = (b-a)/N
    s = 0
    for i in range(N):
        s += f(a+i*dx)
    return s * dx


def planckian_locus(T):
    """XYZ colour coordinates of a theoretical incadescent black body
    radiator at a given temperature, or something like that.

    Can be used to calculate the chromaticity coordinates of, say, a
    6500K light source

    http://en.wikipedia.org/wiki/Planckian_locus

    Argument T is in Kelvin, return value is a CIE XYZ value
    """
    samples = (780-380)/5 # values every 5 nm are stored

    from colour_matching_functions import get_colour_matching_functions
    X, Y, Z = get_colour_matching_functions(two_degree = True)

    # Integrated between 380nm and 780nm, as that is the range of
    # values contained in the colour-matching functions
    X_T = integrate(lambda wavelen: plancks_law(wavelen, T) * X(wavelen), 380, 780, samples)
    Y_T = integrate(lambda wavelen: plancks_law(wavelen, T) * Y(wavelen), 380, 780, samples)
    Z_T = integrate(lambda wavelen: plancks_law(wavelen, T) * Z(wavelen), 380, 780, samples)

    return (X_T, Y_T, Z_T)


def test_plankian_locus_against_approximation():
    """Test plankian locus non-approximation against approximation
    """
    import math
    for T in range(1667, 25000, 1000):
        approx_xy = planckian_locus_approx(T)
        X, Y, Z = planckian_locus(T)
        x = X / (X+Y+Z)
        y = Y / (X+Y+Z)
        calc_xy = x, y

        difference = math.sqrt((approx_xy[0] - calc_xy[0])**2 + (approx_xy[1] - calc_xy[1])**2)
        assert difference < 0.001, "Difference at %d of %.010f" % (T, difference)


def main():
    from matplotlib import pyplot

    # Plot CIE XYZ colour matching curves
    print "Calculating"
    from colour_matching_functions import get_colour_matching_functions
    X, Y, Z = get_colour_matching_functions(two_degree = True)
    print "Test"
    wavelens =[x for x in range(380, 780, 5)]

    sampled_x = [X(T) for T in wavelens]
    sampled_x = [x/max(sampled_x) for x in sampled_x]
    pyplot.plot(sampled_x)

    sampled_y = [Y(T) for T in wavelens]
    sampled_y = [x/max(sampled_y) for x in sampled_y]
    pyplot.plot(sampled_y)

    sampled_z = [Z(T) for T in wavelens]
    sampled_z = [x/max(sampled_z) for x in sampled_z]
    pyplot.plot(sampled_z)

    pyplot.show()


    # Plot spectral locus
    # As explained on http://www.photo-mark.com/notes/2010/sep/08/deconstructing-chromaticity/

    spectral_locus_x = []
    spectral_locus_y = []
    for x, y, z in zip(sampled_x, sampled_y, sampled_z):
        spectral_locus_x.append(
                x / (x+y+z))
        spectral_locus_y.append(
                y / (x+y+z))

    pyplot.plot(spectral_locus_x, spectral_locus_y)


    # Also plot Plankian locus
    T_and_radiance = []

    for T in range(1000, 15000, 350):
        # Calculate plankian locus
        T_and_radiance.append([T, planckian_locus(T)])

    to_plot_x, to_plot_y = [], []
    for (TT, XYZ) in T_and_radiance:
        # Calculate x,y chromaticity coordinate
        # http://en.wikipedia.org/wiki/CIE_1931_color_space#The_CIE_xy_chromaticity_diagram_and_the_CIE_xyY_color_space
        XT, YT, ZT = XYZ
        x = XT / (XT+YT+ZT)
        y = YT / (XT+YT+ZT)
        to_plot_x.append(x)
        to_plot_y.append(y)

    pyplot.plot(to_plot_x, to_plot_y)

    pyplot.axis(xmin = 0, xmax = 1, ymin = 0, ymax = 1)
    pyplot.show()

    print "Checking against approximation"
    test_plankian_locus_against_approximation()
    print "..okay"

if __name__ == '__main__':
    main()
