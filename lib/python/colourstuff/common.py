def lerp(a, b, mix):
    return (b * mix) + a * (1-mix)

def clamp(a, tomin, tomax):
    return max(min(a, tomax), tomin)
