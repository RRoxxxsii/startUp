"""Fixed issues in relationships

Revision ID: 2ceeda8b2f15
Revises: 756aaa5e3dcc
Create Date: 2024-02-26 05:46:40.279515

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2ceeda8b2f15'
down_revision: Union[str, None] = '756aaa5e3dcc'
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