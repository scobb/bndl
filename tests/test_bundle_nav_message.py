#!/usr/bin/env python

import unittest

from bndl.nav_message import NavMessage


class TestBundleNavMessage(unittest.TestCase):

    def test_bundle_header(self):
        msg = NavMessage(1, 2, 3, 4)
        bnd = msg.to_bundle(prefix="nav.")
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
        bnd = msg.to_bundle(prefix="nav.")
        new_msg = NavMessage.from_bundle(bnd, "nav.")

        self.assertEqual(msg, new_msg)

if __name__ == "__main__":
    unittest.main()
