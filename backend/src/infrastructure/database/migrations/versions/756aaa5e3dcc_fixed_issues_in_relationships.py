"""Fixed issues in relationships

Revision ID: 756aaa5e3dcc
Revises: caf1922f29a2
Create Date: 2024-02-26 05:34:48.472406

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '756aaa5e3dcc'
down_revision: Union[str, None] = 'caf1922f29a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
