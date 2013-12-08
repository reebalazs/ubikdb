
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
    for segment in split_path(path):
        if segment:
            root = next
            if segment in root:
                next = root[segment]
            else:
                if set:
                    print 'getset', root, segment
                    next = root[segment] = {}
                else:
                    return None
    if set:
        root[segment] = value
    else:
        return next

def traverse_get(root, path):
    return traverse_getset(root, path)

def traverse_set(root, path, value):
    traverse_getset(root, path, value, set=True)
