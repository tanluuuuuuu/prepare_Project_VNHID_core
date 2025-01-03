"""change products and users

Revision ID: 45d5786708be
Revises: c3afdc307e69
Create Date: 2024-11-19 15:33:28.270231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45d5786708be'
down_revision: Union[str, None] = 'c3afdc307e69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('price', sa.DECIMAL(precision=16, scale=4), nullable=False))
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.VARCHAR(length=3000),
               existing_nullable=True)
    op.alter_column('users', 'language_code',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'language_code',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(length=3000),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.drop_column('products', 'price')
    # ### end Alembic commands ###
