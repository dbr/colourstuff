from UserDict import DictMixin


def lerp(a, b, mix):
    return (b * mix) + a * (1-mix)


def clamp(a, tomin, tomax):
    return max(min(a, tomax), tomin)


class ODict(DictMixin):
    """http://code.activestate.com/recipes/496761-a-more-clean-implementation-for-ordered-dictionary/
    """
    def __init__(self):
        self._keys = []
        self._data = {}

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def keys(self):
        return list(self._keys)

    def copy(self):
        copyDict = odict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict
