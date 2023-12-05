"""Migration name

Revision ID: 8faf41335958
Revises: b5b6d10a57d9
Create Date: 2023-12-04 21:23:03.804411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8faf41335958"
down_revision: Union[str, None] = "b5b6d10a57d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "productdealers", sa.Column("position", sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("productdealers", "position")
    # ### end Alembic commands ###
