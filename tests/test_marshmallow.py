from uuid import uuid1

import pytest
from invenio_pidstore.models import PersistentIdentifier
from marshmallow import ValidationError

from oarepo_invenio_model.marshmallow import InvenioRecordMetadataSchemaV1Mixin, InvenioRecordMetadataFilesMixin
from tests.helpers import marshmallow_load


# def test_load_no_id():
#     with pytest.raises(ValidationError):
#         marshmallow_load(InvenioRecordSchemaV1Mixin(), {})


def test_load_no_id_in_context():
    marshmallow_load(InvenioRecordMetadataSchemaV1Mixin(), {'id': '1'}) == {}


def test_load_id_in_context():
    pid = PersistentIdentifier(object_uuid=uuid1(), pid_value='1')
    assert marshmallow_load(InvenioRecordMetadataSchemaV1Mixin(context={
        'pid': pid
    }), {}) == {
               'id': pid.pid_value
           }


def test_load_files():
    pid = PersistentIdentifier(object_uuid=uuid1(), pid_value='1')
    assert marshmallow_load(InvenioRecordMetadataSchemaV1Mixin(context={
        'pid': pid
    }), {'_files': []}) == {
               'id': pid.pid_value
           }


def test_metadata():
    marshmallow_load(InvenioRecordMetadataSchemaV1Mixin(), {'$schema': 'http://blah'})


def test_files_mixin():
    schema = type('SchemaWithFiles', (InvenioRecordMetadataSchemaV1Mixin, InvenioRecordMetadataFilesMixin), {})
    data = {
        '$schema': 'http://blah',
        '_bucket': '123',
        '_files': [
            {
                'key': 'test.json'
            }
        ]
    }
    loaded = marshmallow_load(schema(), data)
    assert loaded == data
