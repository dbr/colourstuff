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


def plotify():
    from pngcanvas import PNGCanvas
    c = PNGCanvas(512, 512)

    def clamp(a, lower, upper):
        return max(min(a, upper), lower)

    def eightbitify(a):
        return clamp(int(round(a*255)), lower = 0, upper = 255)

    for xcoord in range(1, 512):
        for ycoord in range(1,512):
            x, y = xcoord/511.0, ycoord/511.0

            Y = 0.5
            X = Y/y * x
            Z = Y/y * (1-x-y)

            r = X*0.4124564 + Y*0.3575761 + Z*0.1804375
            g = X*0.2126729 + Y*0.7151522 + Z*0.0721750
            b = X*0.0193339 + Y*0.1191920 + Z*0.9503041

            r = clamp(r, lower = 0, upper = 1)/sum([r,g,b])
            g = clamp(g, lower = 0, upper = 1)/sum([r,g,b])
            b = clamp(b, lower = 0, upper = 1)/sum([r,g,b])

            r = r**(1/2.2)
            g = g**(1/2.2)
            b = b**(1/2.2)

            c.point(xcoord, ycoord, color = (eightbitify(r), eightbitify(g), eightbitify(b), 255))

    for T in range(1667, 25000, 10):
        try:
            x, y = planckian_locus_approx(T)
            c.point(int(x*512), int(y*512), color = (0,0,0,255))
        except ValueError, e:
            print e

    f = open("planckian_locus_approx.png", "wb")
    f.write(c.dump())
    f.close()

if __name__ == '__main__':
    plotify()