from uuid import uuid1

import pytest
from invenio_pidstore.models import PersistentIdentifier
from marshmallow import ValidationError

from invenio_oarepo_invenio_model.marshmallow import InvenioRecordSchemaV1Mixin
from tests.helpers import marshmallow_load


def test_load_no_id():
    with pytest.raises(ValidationError):
        marshmallow_load(InvenioRecordSchemaV1Mixin(), {})


def test_load_no_id_in_context():
    with pytest.raises(ValidationError):
        marshmallow_load(InvenioRecordSchemaV1Mixin(), {'id': '1'})


def test_load_id_in_context():
    pid = PersistentIdentifier(object_uuid=uuid1())
    assert marshmallow_load(InvenioRecordSchemaV1Mixin(context={
        'pid': pid
    }), {}) == {
               'id': str(pid.object_uuid)
           }


def test_load_files():
    pid = PersistentIdentifier(object_uuid=uuid1())
    assert marshmallow_load(InvenioRecordSchemaV1Mixin(context={
        'pid': pid
    }), {'_files': []}) == {
               'id': str(pid.object_uuid)
           }
