from contextlib import contextmanager

import flask
from flask import current_app
from flask_principal import Identity, identity_changed
from invenio_access import authenticated_user
from invenio_records_draft.proxies import current_drafts
from invenio_records_rest.utils import allow_all
from marshmallow import ValidationError
from marshmallow import __version_info__ as marshmallow_version


@contextmanager
def disable_test_authenticated():
    stored_drafts = {}
    stored_published = {}
    for prefix, endpoint in current_drafts.draft_endpoints.items():
        stored_drafts[prefix] = {**endpoint}
        endpoint['publish_permission_factory'] = allow_all
        endpoint['unpublish_permission_factory'] = allow_all
        endpoint['edit_permission_factory'] = allow_all
    for prefix, endpoint in current_drafts.published_endpoints.items():
        stored_published[prefix] = {**endpoint}
        endpoint['publish_permission_factory'] = allow_all
        endpoint['unpublish_permission_factory'] = allow_all
        endpoint['edit_permission_factory'] = allow_all
    try:
        yield
    finally:
        for prefix in current_drafts.draft_endpoints:
            current_drafts.draft_endpoints[prefix] = stored_drafts[prefix]
        for prefix in current_drafts.published_endpoints:
            current_drafts.published_endpoints[prefix] = stored_published[prefix]

def set_identity(u):
    """Sets identity in flask.g to the user."""
    identity = Identity(u.id)
    identity.provides.add(authenticated_user)
    identity_changed.send(current_app._get_current_object(), identity=identity)
    assert flask.g.identity.id == u.id

def marshmallow_load(schema, data):
    ret = schema.load(data)
    if marshmallow_version[0] >= 3:
        return ret
    if ret[1] != {}:
        raise ValidationError(message=ret[1])
    return ret[0]
