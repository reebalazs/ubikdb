
from ...traverse import (
    traverse_getset,
    split_path,
)

class DefaultMapper(object):

    def __init__(self, root, annotate_attr, annotate_key):
        self.root = root
        self.annotate_attr = annotate_attr
        self.annotate_key = annotate_key

    def traverse_getset(self, path, value=None, set=False):
        if not hasattr(self.root, self.annotate_attr) and set:
            annotation = {}
            setattr(self.root, self.annotate_attr, annotation)
        else:
            annotation = getattr(self.root, self.annotate_attr, {})
        if self.annotate_key not in annotation:
            root = {}
            if set:
                annotation[self.annotate_key] = root
        else:
            root = annotation[self.annotate_key]
        # Now that we have the root, let's traverse it
        # via the normal memory traverser.
        result = traverse_getset(root, path, value, set)
        return result


class AttributeMapper(object):

    allowed_attributes = ('title', );

    def __init__(self, root, allowed_attributes=None):
        self.root = root
        if allowed_attributes is not None:
            self.allowed_attributes = allowed_attributes

    def traverse_getset(self, path, value=None, set=False):
        split = [segment for segment in split_path(path) if segment]
        if len(split) > 1:
            raise RuntimeError("AttributeMapper error, tried to traverse inside a property,"
                               " not yet supported")
        if len(split) == 1:
            # a single property is get or set
            segment = split[0]
            if segment not in self.allowed_attributes:
                raise RuntimeError("AttributeMapper error, property not allowed [%s]" %
                    (segment, ))
            if set:
                print('SET', segment, value)
                setattr(self.root, segment, value)
                return
            else:
                return getattr(self.root, segment, None)
        else:
            # get/set all allowed attributes in a dict
            assert not split
            if set:
                for segment in self.allowed_attributes:
                    # right now, we set even if the value None or missing.
                    val = value.get(segment, None)
                    setattr(self.root, segment, val)
                return
            else:
                result = {}
                for segment in self.allowed_attributes:
                    if hasattr(self.root, segment):
                        result[segment] = getattr(self.root, segment)
                return result
