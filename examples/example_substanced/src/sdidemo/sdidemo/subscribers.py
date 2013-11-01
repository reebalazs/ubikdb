import datetime
from pyramid.compat import is_nonstr_iter

from substanced.root import Root
from substanced.event import (
    subscribe_created,
    subscribe_modified,
    )
from substanced.util import (
    find_service,
    oid_of,
    )

from .resources import IDemoContent

def add_sample_content(site, registry):
    # Give a site sdi_title
    site.sdi_title = 'Substance D Demo'
    admin_user = site['principals']['users']['admin']
    admin_oid = admin_user.__oid__
    oldacl = admin_user.__acl__
    newacl = []

    # disallow password changing for admin user (for demo)
    for (action, oid, permissions) in oldacl:
        if oid == admin_oid and action == 'Allow':
            if not is_nonstr_iter(permissions):
                permissions = (permissions,)
            permissions = set(permissions)
            if 'sdi.change-password' in permissions:
                permissions.remove('sdi.change-password')
                permissions = tuple(permissions)
        newacl.append((action, oid, permissions))

    if newacl != oldacl:
        admin_user.__acl__ = newacl

    site.__acl__.insert(
        0,
        ('Deny', admin_oid, ('sdi.change-password',))
        )
    site.__acl__.insert(
        0,
        ('Deny', admin_oid, ('sdi.manage-user-groups',))
        )
    
    for binder_num in range(1):
        binder = registry.content.create('Binder',
            'Binder %d' % binder_num)
        binder_name = 'binder_%d' % binder_num
        site[binder_name] = binder
        for doc_num in range(1000):
            doc = registry.content.create('Document',
                'Document %d Binder %d' % (doc_num, binder_num),
                'The quick brown fox jumps over the lazy dog. ' * 50)
            doc.__creator__ = oid_of(admin_user)
            doc_name = 'document_%d' % doc_num
            binder[doc_name] = doc
    binder = registry.content.create('Binder', 'Ordered Binder')
    binder_name = 'ordered_binder'
    site[binder_name] = binder
    binder_order = []
    for doc_num in range(20):
        doc = registry.content.create('Document',
            'Document %d Binder %d' % (doc_num, binder_num),
            'The quick brown fox jumps over the lazy dog. ' * 50)
        doc.__creator__ = oid_of(admin_user)
        doc_name = 'document_%d' % doc_num
        binder[doc_name] = doc
        binder_order.append(doc_name)
    binder.set_order(binder_order, reorderable=True)


@subscribe_created(Root)
def root_created(event):
    catalogs = find_service(event.object, 'catalogs')
    catalogs.add_catalog('sdidemo', update_indexes=True)
    add_sample_content(event.object, event.registry)

@subscribe_modified(IDemoContent)
def content_edited(event):
    event.object.__modified__ = datetime.datetime.utcnow()

