
from .context import ContextMixin

# Database is kept in memory (volatile)
global db_root
db_root = {}
db_root_key = 'ubikdb'
db_root[db_root_key] = {
    'boss': 'Glen Runciter',
    'agent': 'Joe Chip'
}


class StorageMixin(ContextMixin):

    @property
    def root(self):
        return {
            'data': db_root,
            'segment': db_root_key,
        }

    def traverse_path(self, context):
        segment = self.root['segment']
        data = self.root['data'][segment]
        trunk = {
            'data': data,
            'segment': segment
        }
        traverse = [self.root, trunk]
        split_context = context.split('/')
        for segment in split_context:
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

    def traverse(self, context):
        return self.traverse_path(context)[-1]['data']

    def on_get(self, context):
        value = self.traverse(context)
        return [value]

    def on_set(self, context, value):
        traverse = self.traverse_path(context)
        last = traverse[-2]
        last['data'][last['segment']] = value
        # notify listeners
        self.emit_with_context('set', context, value, recurse=True)
