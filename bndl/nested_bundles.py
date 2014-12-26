__author__ = 'scobb'

from bndl.bundleable import Bundleable
from bndl.nav_message import NavMessage

class NavList(Bundleable):

    def __init__(self, nav_msg, nav_msg_list, int_list, str_list):
        self.nav_msg = nav_msg
        self.nav_msg_list = nav_msg_list
        self.int_list = int_list
        self.str_list = str_list

    def __eq__(self, other):
        if isinstance(other, NavList):
            if self.nav_msg != other.nav_msg:
                print "Nav messages unequal"
            if self.str_list != other.str_list:
                print "Str lists unequal"
                print self.str_list, other.str_list
            if self.int_list != other.int_list:
                print "int lists unequal"
                print self.int_list, other.int_list
            return (self.nav_msg == other.nav_msg and
                    self.nav_msg_list == other.nav_msg_list and
                    self.int_list == other.int_list and
                    self.str_list == other.str_list)
        else:
            return NotImplemented

    def __repr__(self):
        bnd = self.to_bundle('nav_list')
        return bnd.get_header_as_string()

def run():
    nav_msg_list = []
    for i in xrange(5):
        nav_msg_list.append(NavMessage(i, i, i, i))
    nav_list = NavList(NavMessage(1, 1, 1, 1), nav_msg_list, [i for i in xrange(5)], [])
    bnd = nav_list.to_bundle('nav_list')
    print bnd.get_header_as_string()
    nl2 = NavList.from_bundle(bnd, prefix='nav_list')
    nl2.str_list.append('hi')
    print nl2.to_bundle(prefix='nl2').get_header_as_string()
