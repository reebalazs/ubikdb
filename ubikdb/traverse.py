
def traverse_path(data, *path):
    traverse = [dict(data=data)]
    split_path = []
    for part in path:
        split_path.extend(part.split('/'))
    for segment in split_path:
        last = traverse[-1]
        data = last['data']
        if segment:
            last['segment'] = segment
            if segment in data:
                data = data[segment]
                traverse.append(dict(data=data))
            else:
                traverse.append(dict(data=None))
                break
    return traverse

def traverse(data, *path):
    return traverse_path(data, *path)[-1]['data']
