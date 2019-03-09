# Copyright 2013-2019 CERN for the benefit of the ATLAS collaboration.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Vincent Garonne <vincent.garonne@cern.ch>, 2015-2017
# - Mario Lassnig <mario.lassnig@cern.ch>, 2019

''' add convention table and closed_at to dids '''

import datetime

import sqlalchemy as sa

from alembic import context
from alembic.op import (create_table, create_primary_key, create_foreign_key, add_column,
                        create_check_constraint, drop_column, drop_table)

from rucio.common.schema import SCOPE_LENGTH
from rucio.db.sqla.constants import KeyType


# Alembic revision identifiers
revision = '3082b8cef557'
down_revision = '269fee20dee9'


def upgrade():
    '''
    Upgrade the database to this revision
    '''

    if context.get_context().dialect.name in ['oracle', 'mysql', 'postgresql']:
        add_column('dids', sa.Column('closed_at', sa.DateTime))
        add_column('contents_history', sa.Column('deleted_at', sa.DateTime))
        create_table('naming_conventions',
                     sa.Column('scope', sa.String(SCOPE_LENGTH)),
                     sa.Column('regexp', sa.String(255)),
                     sa.Column('convention_type', KeyType.db_type(name='CVT_TYPE_CHK')),
                     sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow),
                     sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow))
        create_primary_key('NAMING_CONVENTIONS_PK', 'naming_conventions', ['scope'])
        create_foreign_key('NAMING_CONVENTIONS_SCOPE_FK', 'naming_conventions',
                           'scopes', ['scope'], ['scope'])
        create_check_constraint('NAMING_CONVENTIONS_CREATED_NN', 'naming_conventions',
                                'created_at is not null')
        create_check_constraint('NAMING_CONVENTIONS_UPDATED_NN', 'naming_conventions',
                                'updated_at is not null')

    elif context.get_context().dialect.name == 'postgresql':
        pass


def downgrade():
    '''
    Downgrade the database to the previous revision
    '''

    if context.get_context().dialect.name in ['oracle', 'mysql', 'postgresql']:
        drop_column('dids', 'closed_at')
        drop_column('contents_history', 'deleted_at')
        drop_table('naming_conventions')

    elif context.get_context().dialect.name == 'postgresql':
        pass
