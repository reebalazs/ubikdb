import colander
import deform.widget

from persistent import Persistent

from zope.interface import (
    Interface,
    implementer,
    )

from substanced.content import content
from substanced.property import PropertySheet
from substanced.objectmap import multireference_sourceid_property
from substanced.schema import (
    Schema,
    NameSchemaNode,
    )
from substanced.util import (
    renamer,
    find_catalog,
    )
from substanced.interfaces import ReferenceType
from substanced.folder import Folder
from substanced.objectmap import find_objectmap

def context_is_a_binder(context, request):
    return request.registry.content.istype(context, 'Binder')

def context_is_a_document(context, request):
    return request.registry.content.istype(context, 'Document')

class SomeMappingSchema(Schema):
    foo = colander.SchemaNode(
        colander.String()
        )
    bar = colander.SchemaNode(
        colander.String()
        )

@colander.deferred
def deferred_objectrefs(node, kw):
    context = kw['context']
    L = []
    maximum = 50
    current = 0
    for name, obj in context.items():
        oid = obj.__oid__
        L.append((oid, name))
        current+=1
        if current >= maximum:
            break
    return deform.widget.Select2Widget(values=L)

class ReferenceSequence(colander.SequenceSchema):
    refid = colander.SchemaNode(
        colander.Int(),
        widget=deferred_objectrefs,
        preparer=int,
        )

class BinderSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_binder,
        )
    title = colander.SchemaNode(
        colander.String(),
        )
    submapping = SomeMappingSchema()
    related = ReferenceSequence(
        widget = deform.widget.SequenceWidget(orderable=True)
        )

class DocumentSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_document,
    )
    title = colander.SchemaNode(
        colander.String(),
    )
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )


class DocumentPropertySheet(PropertySheet):
    schema = DocumentSchema()

class BinderPropertySheet(PropertySheet):
    schema = BinderSchema()
    def get(self):
        result = PropertySheet.get(self)
        return result
        
    def set(self, appstruct):
        result = PropertySheet.set(self, appstruct)
        return result
    
class IDemoContent(Interface):
    pass

def find_index(context, catalog_name, index_name):
    catalog = find_catalog(context, catalog_name)
    return catalog[index_name]

def binder_columns(folder, subobject, request, default_columnspec):
    subobject_name = getattr(subobject, '__name__', str(subobject))
    objectmap = find_objectmap(folder)
    user_oid = getattr(subobject, '__creator__', None)
    created = getattr(subobject, '__created__', None)
    modified = getattr(subobject, '__modified__', None)
    if user_oid is not None:
        user = objectmap.object_for(user_oid)
        user_name = getattr(user, '__name__', 'anonymous')
    else:
        user_name = 'anonymous'
    if created is not None:
        created = created.isoformat()
    if modified is not None:
        modified = modified.isoformat()

    def make_sorter(index_name):
        def sorter(folder, resultset, limit=None, reverse=False):
            index = find_index(folder, 'sdidemo', index_name)
            if index is None:
                return resultset
            return resultset.sort(index, limit=limit, reverse=reverse)
        return sorter

    return default_columnspec + [
        {'name': 'Title',
        'value': getattr(subobject, 'title', subobject_name),
        'sorter': make_sorter('title'),
        },
        {'name': 'Modified Date',
        'value': modified,
        'sorter':make_sorter('modified'),
        'formatter': 'date',
        },
        {'name': 'Creator',
        'value': user_name,
        }
        ]

class AnotherPropertySheet(PropertySheet):
    schema = BinderSchema()

class BinderToRelated(ReferenceType):
    pass
    

@content(
    'Binder',
    icon='glyphicon glyphicon-book',
    add_view='add_binder',
    propertysheets = (
        ('Basic', BinderPropertySheet),
        ('Another', AnotherPropertySheet),
        ),
    columns=binder_columns,
    )
@implementer(IDemoContent)
class Binder(Folder):

    name = renamer()
    related = multireference_sourceid_property(BinderToRelated, ordered=True)
    
    def __init__(self, title):
        super(Binder, self).__init__()
        self.title = title

@content(
    'Document',
    icon='glyphicon glyphicon-align-left',
    add_view='add_document',
    propertysheets=(
        ('Basic', DocumentPropertySheet),
        ),
    )
@implementer(IDemoContent)
class Document(Persistent):
    name = renamer()

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def after_create(self, inst, registry):
        pass

