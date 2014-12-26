#!/usr/bin/env python

import unittest

from bndl.nav_message import NavMessage
from bndl.nested_bundles import NavList


class TestBundleNavMessage(unittest.TestCase):

    def test_bundle_header(self):
        msg = NavMessage(1, 2, 3, 4)
        bnd = msg.to_bundle(prefix="nav")
        actual = bnd.get_header_as_string()

        expected = (
            "nav.altitude: 4\n"
            "nav.depth: 3\n"
            "nav.lat: 1\n"
            "nav.lon: 2\n"
            "nav.type: NavMessage\n")
        self.assertEqual(actual, expected)

    def test_to_from_bundle_equal(self):
        msg = NavMessage(1, 2, 3, 4)
        bnd = msg.to_bundle(prefix="nav")
        new_msg = NavMessage.from_bundle(bnd, "nav")

        self.assertEqual(msg, new_msg)

class TestBundleNavList(unittest.TestCase):

    def setUp(self):
        nav_msg_list = []
        for i in xrange(5):
            nav_msg_list.append(NavMessage(i, i, i, i))
        self.nav_list = NavList(NavMessage(1, 1, 1, 1), nav_msg_list, [i for i in xrange(5)], ['s1', 's2'])

    def test_to_from_bundle_equal(self):
        bnd = self.nav_list.to_bundle('nav_list')
        new_list = NavList.from_bundle(bnd, prefix='nav_list')
        self.assertEqual(self.nav_list, new_list)

if __name__ == "__main__":
    unittest.main()
