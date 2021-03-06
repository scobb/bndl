__author__ = 'scobb'
import inspect
from bundle import Bundle

#TODO - maybe add dict support? Not sure it's necessary.


class Bundleable(object):
    def __init__(self):
        raise NotImplementedError

    def to_bundle(self, prefix=''):
        """ Turns an object into a serialized bundle.

        Args:
            prefix: The prefix to prepend to the keys corresponding to the
                    instance variable names

        Returns:
            A serialized bundle that can be unbundled into the same object.
        """
        bnd = Bundle()
        metacount = 0
        bnd.set_value(prefix + '.type', self.__class__.__name__)
        for key, val in self.__dict__.iteritems():
            if isinstance(val, Bundleable):
                # take care of nested bundleables
                bnd.assimilate(val.to_bundle(prefix='%s.%s' % (prefix, key)))
                arg_type = val.__module__ + '.' + val.__class__.__name__
                meta = BundleableMetadata(key, arg_type, '%s.%s' % (prefix, key))
                bnd.assimilate(meta.to_bundle('%s.meta.%d' % (prefix, metacount)))
                metacount += 1
            elif isinstance(val, list):
                # take care of a list
                if val:
                    if isinstance(val[0], Bundleable):
                        # list of bundleables
                        bnd.assimilate(self.encode_list(val, prefix='%s.%s' % (prefix, key)))
                        arg_type = val[0].__module__ + '.' + val[0].__class__.__name__
                        meta = ListMetadata(key, arg_type, '%s.%s' % (prefix, key), len(val))
                        bnd.assimilate(meta.to_bundle('%s.meta.%d' % (prefix, metacount)))
                        metacount += 1
                    else:
                        # list of primitives - anything that can be converted to/from a string
                        for i, obj in enumerate(val):
                            bnd.set_value('%s.%s.%d' % (prefix, key, i), obj)
                        #TODO the line below only works if val is not empty
                        meta = ListMetadata(key, 'prim.' + str(type(val[0]).__name__), '%s.%s' % (prefix, key), len(val))
                        bnd.assimilate(meta.to_bundle('%s.meta.%d' % (prefix, metacount)))
                        metacount += 1
                else:
                    # empty list
                    bnd.set_value('%s.%s' % (prefix, key), val)
            else:
                bnd.set_value(prefix + "." + key, self.__dict__[key])
        return bnd

    @classmethod
    def from_bundle(cls, bnd, prefix=''):
        """ Takes a bundle and turns it into an object.

        Args:
            bnd: The bundle to use to create an object
            prefix: The prefix to use to unbundle the object
        """
        count = 0
        meta = []
        while prefix + '.meta.%d.key' % count in bnd.keys():
            # grab the appropriate metadata class
            meta_type = eval(bnd.get_value(prefix + '.meta.%d.type' % count))
            meta.append(meta_type.from_bundle(bnd, prefix=prefix + '.meta.%d' % count))
            count += 1
        args = {}
        for metadata in meta:
            # use metadata to parse complex data
            args[metadata.key] = metadata.decode(bnd)
        constructor_args = inspect.getargspec(cls.__init__)[0]
        for arg_name in constructor_args:
            if arg_name != 'self' and arg_name not in args:
                # grab extra arguments we need from the bundle
                try:
                    # try to evaluate primitives back to what they are (lists, etc)
                    args[arg_name] = eval(bnd.get_value(prefix + "." + arg_name))
                except:
                    # if this doesn't work, it's probably metadata--a class name. just use the string.
                    args[arg_name] = bnd.get_value(prefix + "." + arg_name)

        return cls(**args)

    @staticmethod
    def encode_list(item_list, prefix=''):
        bnd = Bundle()
        for i, item in enumerate(item_list):
            bnd.assimilate(item.to_bundle('%s.%d' % (prefix, i)))
        return bnd

class Metadata(Bundleable):
    """
    interface - defines the metadata interface
    """
    def __init__(self):
        raise NotImplementedError

    def decode(self, bndl):
        """
        method - to be defined by all metadata. This is how we get an object back.
        """
        raise NotImplementedError


#TODO (lemonade512) Write tests to make sure the decoding import stuff works from the root directory,
#                   and down multiple levels
class BundleableMetadata(Metadata):
    """
    class - used for bundling inner classes
    """

    def __init__(self, key, arg_type, prefix):
        self.key = key
        self.arg_type = arg_type
        self.prefix = prefix

    def decode(self, bnd):
        """
        method - decodes object for self metadata from bundle
        :param bnd: bundle to decode
        :return: Bundleable object this metadata was representing
        """
        # Assumption: self.arg_type has at least 2 values when split
        root_package = self.arg_type.split('.')[0]
        path_to_module = self.arg_type.split('.')[1:-1]
        imp_class = self.arg_type.split('.')[-1]

        module = __import__(root_package)
        for name in path_to_module:
            module = module.__dict__[name]
        module = getattr(module, imp_class)
        return module.from_bundle(bnd, prefix=self.prefix)


class ListMetadata(Metadata):
    """
    class - used for bundling lists
    """
    def __init__(self, key, arg_type, prefix, num):
        self.key = key
        self.arg_type = arg_type
        self.prefix = prefix
        self.num = num

    def decode(self, bnd):
        """
        method - decodes list of objects from self metadata
        :param bnd: bundle to decode
        :return: list of objects this metadata was representing
        """
        if self.arg_type.split('.')[0] == 'prim':
            # lists of primitives
            res_list = []
            # TODO (lemonade512) using eval below is technically a security risk
            prim_type = eval(self.arg_type.split('.')[1])
            for i in xrange(int(self.num)):
                res_list.append(prim_type(bnd.get_value('%s.%s' % (self.prefix, i))))
        else:
            # lists of bundleables
            # Assumption: self.arg_type has at least 2 values when split
            root_package = self.arg_type.split('.')[0]
            path_to_module = self.arg_type.split('.')[1:-1]
            imp_class = self.arg_type.split('.')[-1]

            # import appropriate module
            module = __import__(root_package)
            for name in path_to_module:
                module = module.__dict__[name]
            module = getattr(module, imp_class)

            # unbundle the objects into our result list
            res_list = []
            for i in range(int(self.num)):
                res_list.append(module.from_bundle(bnd, prefix='%s.%d' % (self.prefix, i)))
        return res_list

