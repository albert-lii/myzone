"""empty message

Revision ID: 5f8cfd2d583e
Revises: c2449e59a80e
Create Date: 2020-04-26 17:44:21.458031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f8cfd2d583e'
down_revision = 'c2449e59a80e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mz_article', sa.Column('body_html', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mz_article', 'body_html')
    # ### end Alembic commands ###
