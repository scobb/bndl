__author__ = 'scobb'

from bundleable import Bundleable

class NavMessage(Bundleable):

    def __init__(self, lat, lon, depth, altitude):
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.altitude = altitude

        #self.my_dict = dict()
        #self.my_dict['key1'] = "val1"
        #self.my_dict['key2'] = "val2"

    def __eq__(self, other):
        if isinstance(other, NavMessage):
            return (self.lat == other.lat and
                    self.lon == other.lon and
                    self.depth == other.depth and
                    self.altitude == other.altitude)
        else:
            return NotImplemented

if __name__ == '__main__':
    nav_msg = NavMessage(1, 2, 3, 4)
    bnd = nav_msg.to_bundle('nav.')
    print bnd.get_header_as_string()
    nav2 = NavMessage.from_bundle(bnd, prefix='nav.')
