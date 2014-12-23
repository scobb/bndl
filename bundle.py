__author__ = 'scobb'

class Bundle(object):
    def __init__(self):
        self.vals = {}

    def get_header_as_string(self):
        ret_str = ""
        for key, val in sorted(self.vals.iteritems()):
            ret_str += "%s: %s\n" % (key, str(val))
        return ret_str

    def set_value(self, key, val):
        self.vals[key] = str(val)

    def get_value(self, key):
        return self.vals[key]

    def keys(self):
        return self.vals.keys()

    def assimilate(self, other):
        self.vals.update(other.vals)

if __name__ == '__main__':
    bnd1 = Bundle()
    bnd1.set_value('1', 1)
    bnd2 = Bundle()
    bnd2.set_value('2', 2)
    bnd1.assimilate(bnd2)
    print '%d' % bnd1.get_value('2')
