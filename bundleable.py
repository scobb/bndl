__author__ = 'scobb'

from bundle import Bundle
import sys


class Bundleable(object):
    def __init__(self):
        raise NotImplementedError

    def to_bundle(self, prefix=''):
        bnd = Bundle()
        count = 0
        bnd.set_value(prefix + 'type', self.__class__.__name__)
        for key, val in self.__dict__.iteritems():
            if isinstance(val, Bundleable):
                # take care of nested bundleables
                bnd.assimilate(val.to_bundle(prefix=prefix + key + '.'))
                arg_type = val.__module__ + '.' + val.__class__.__name__
                meta = BundleableMetadata(key, arg_type, prefix + key + '.')
                bnd.assimilate(meta.to_bundle(prefix + 'meta.%d.' % count))
                count += 1
            elif isinstance(val, list):
                # take care of a list
                if val:
                    if isinstance(val[0], Bundleable):
                        # list of bundleables
                        bnd.assimilate(self.encode_list(val, prefix=prefix + key + '.'))
                        arg_type = val[0].__module__ + '.' + val[0].__class__.__name__
                        meta = ListMetadata(key, arg_type, prefix + key + '.', len(val))
                        bnd.assimilate(meta.to_bundle(prefix + 'meta.%d.' % count))
                        count += 1
                    else:
                        # list of primitives
                        for i, obj in enumerate(val):
                            bnd.set_value(prefix + '%s.%d' % (key, i), obj)
                        meta = ListMetadata(key, 'prim', prefix + key + '.', len(val))
                        bnd.assimilate(meta.to_bundle(prefix + 'meta.%d.' % count))
                        count += 1
                else:
                    bnd.set_value(key, val)
            else:
                bnd.set_value(prefix + key, self.__dict__[key])
        return bnd

    @classmethod
    def from_bundle(cls, bnd, prefix=''):
        count = 0
        meta = []
        while prefix + 'meta.%d.key' % count in bnd.keys():
            meta_type = eval(bnd.get_value(prefix + 'meta.%d.type' % count))
            meta.append(meta_type.from_bundle(bnd, prefix=prefix+'meta.%d.' % count))
            count += 1
        args = {}
        for metadata in meta:
            args[metadata.key] = metadata.decode(bnd)
        for key in bnd.keys():
            args[key.replace(prefix, '')] = bnd.get_value(key)

        return cls(**args)

    def encode_list(self, item_list, prefix=''):
        bnd = Bundle()
        for i, item in enumerate(item_list):
            bnd.assimilate(item.to_bundle('%s%d.' % (prefix, i)))
        return bnd

    @classmethod
    def decode_list(cls, bnd, prefix=''):
        decoded_list = []
        i = 0
        while '%s.%d.type' % (prefix, i) in bnd.keys():
            decoded_list.append(cls.from_bundle(bnd, prefix + cls.__name__ + '.%d.' % i))
            i += 1
        return decoded_list


class BundleableMetadata(Bundleable):
    def __init__(self, key, arg_type, prefix, **kwargs):
        self.key = key
        self.arg_type = arg_type
        self.prefix = prefix

    def decode(self, bnd):
        module, imp_class = self.arg_type.split('.')
        module = __import__(module)
        module = getattr(module, imp_class)
        return module.from_bundle(bnd, prefix=self.prefix)



class ListMetadata(Bundleable):
    def __init__(self, key, arg_type, prefix, num, **kwargs):
        self.key = key
        self.arg_type = arg_type
        self.prefix = prefix
        self.num = num

    def decode(self, bnd):
        if self.arg_type == 'prim':
            # lists of primitives
            res_list = []
            for i in xrange(int(self.num)):
                res_list.append(bnd.get_value('%s%s' % (self.prefix, i)))
        else:
            # lists of bundleables
            module, imp_class = self.arg_type.split('.')
            module = __import__(module)
            module = getattr(module, imp_class)
            res_list = []
            for i in range(int(self.num)):
                res_list.append(module.from_bundle(bnd, prefix=self.prefix + '%d.' % i))
        return res_list