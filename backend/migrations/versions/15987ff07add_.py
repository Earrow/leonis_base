"""empty message

Revision ID: 15987ff07add
Revises: 5791371c4050
Create Date: 2019-11-01 14:58:24.284782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15987ff07add'
down_revision = '5791371c4050'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active_project_id', sa.Integer(), nullable=True, comment='活动项目id'))
    op.create_foreign_key(None, 'users', 'projects', ['active_project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'active_project_id')
    # ### end Alembic commands ###
