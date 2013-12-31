

def split_path(path):
    # path can be an iterable or a single string.
    # If it's an iterable, all segments will be connected.
    if isinstance(path, basestring):
        path = (path, )
    split_path = []
    for part in path:
        split_path.extend(part.split('/'))
    return split_path

def traverse_getset(root, path, value=None, set=False):
    next = root
    last_segment = None
    for segment in split_path(path):
        if segment:
            last_segment = segment
            root = next
            if segment in root:
                next = root[segment]
                if set and not isinstance(next, dict):
                    # force this value to a dict, as we will
                    # want to set a value somewhere on a leaf.
                    next = root[segment] = {}
            else:
                if set:
                    next = root[segment] = {}
                else:
                    return None
    if set:
        if last_segment is None:
            raise RuntimeError('Cannot set the root of the database.')
        root[last_segment] = value
    else:
        return next

def traverse_get(root, path):
    return traverse_getset(root, path)

def traverse_set(root, path, value):
    traverse_getset(root, path, value, set=True)
