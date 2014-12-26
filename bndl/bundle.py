__author__ = 'scobb'

class Bundle(object):
    def __init__(self):
        self.vals = {}

    def get_header_as_string(self):
        """ Returns a string with all the keys and their values. """
        ret_str = ""
        for key, val in sorted(self.vals.iteritems()):
            ret_str += "%s: %s\n" % (key, str(val))
        return ret_str

    def set_value(self, key, val):
        """ Sets the value of 'key' to 'val'.

        Args:
            key: the key to set the value of
            val: value to set for 'key'
        """
        self.vals[key] = str(val)

    # TODO (lemonade512) use __getitem__ so we can access as a dict?
    def get_value(self, key):
        return self.vals[key]

    def keys(self):
        return self.vals.keys()

    def assimilate(self, other):
        """ Combines other with self. """
        self.vals.update(other.vals)

if __name__ == '__main__':
    bnd1 = Bundle()
    bnd1.set_value('1', 1)
    bnd2 = Bundle()
    bnd2.set_value('2', 2)
    bnd1.assimilate(bnd2)
    print '%d' % bnd1.get_value('2')
