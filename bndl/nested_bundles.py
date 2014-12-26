__author__ = 'scobb'

from bundleable import Bundleable
from nav_message import NavMessage

class NavList(Bundleable):
    def __init__(self, nav_msg, nav_msg_list, int_list, str_list):
        self.nav_msg = nav_msg
        self.nav_msg_list = nav_msg_list
        self.int_list = int_list
        self.str_list = str_list

def run():
    nav_msg_list = []
    for i in xrange(5):
        nav_msg_list.append(NavMessage(i, i, i, i))
    nav_list = NavList(NavMessage(1, 1, 1, 1), nav_msg_list, [i for i in xrange(5)], [])
    bnd = nav_list.to_bundle('nav_list.')
    print bnd.get_header_as_string()
    nl2 = NavList.from_bundle(bnd, prefix='nav_list.')
    nl2.str_list.append('hi')
    print nl2.to_bundle(prefix='nl2.').get_header_as_string()

    nm = NavMessage(1, 1, 1, 1)
    # TODO (lemonade512) Should we remove the need to always have a dot at the end of a prefix?
    bnd = nm.to_bundle('nav.')
    print bnd.get_header_as_string()
    nm = NavMessage.from_bundle(bnd, prefix='nav.')
    print nm
