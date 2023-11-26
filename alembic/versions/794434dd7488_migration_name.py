"""Migration name

Revision ID: 794434dd7488
Revises: 
Create Date: 2023-11-26 16:26:30.125535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "794434dd7488"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dealers",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dealers_id"), "dealers", ["id"], unique=False)
    op.create_table(
        "products",
        sa.Column("article", sa.String(), nullable=True),
        sa.Column("ean_13", sa.BigInteger(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("cost", sa.Float(), nullable=True),
        sa.Column("recommended_price", sa.Float(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("ozon_name", sa.String(), nullable=True),
        sa.Column("name_1c", sa.String(), nullable=True),
        sa.Column("wb_name", sa.String(), nullable=True),
        sa.Column("ozon_article", sa.String(), nullable=True),
        sa.Column("wb_article", sa.String(), nullable=True),
        sa.Column("ym_article", sa.String(), nullable=True),
        sa.Column("wb_article_td", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_table(
        "dealerprices",
        sa.Column("product_key", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("product_url", sa.String(), nullable=False),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("dealer_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dealer_id"],
            ["dealers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dealerprices_id"), "dealerprices", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_dealerprices_id"), table_name="dealerprices")
    op.drop_table("dealerprices")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_dealers_id"), table_name="dealers")
    op.drop_table("dealers")
    # ### end Alembic commands ###
