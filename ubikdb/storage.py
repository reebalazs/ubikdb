
from .context import ContextMixin
from .traverse import (
    traverse,
    traverse_path,
)

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
        return db_root

    @property
    def root_key(self):
        return db_root_key

    def traverse_path(self, context):
        return traverse_path(self.root, self.root_key, context)

    def traverse(self, context):
        return traverse(self.root, self.root_key, context)

    def on_get(self, context):
        value = self.traverse(context)
        print "XXX on_get", context, value
        return [value]

    def on_set(self, context, value):
        traverse = self.traverse_path(context)
        last = traverse[-2]
        last['data'][last['segment']] = value
        # notify listeners
        self.emit_in_context('set', context, value)
