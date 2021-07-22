"""empty message

Revision ID: 950793b28294
Revises: 
Create Date: 2021-07-21 11:20:07.043246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '950793b28294'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('city_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('city_name', sa.String(), nullable=True),
    sa.Column('city_state', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('city_id')
    )
    op.create_table('attraction',
    sa.Column('attraction_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.city_id'], ),
    sa.PrimaryKeyConstraint('attraction_id')
    )
    op.create_table('col',
    sa.Column('col_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('milk_cost', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.Column('transport_ticket', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.Column('gas', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.Column('basic_utilities', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.Column('rent', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.Column('avg_monthly_salary', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.city_id'], ),
    sa.PrimaryKeyConstraint('col_id')
    )
    op.create_table('crimerate',
    sa.Column('crimerate_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('crime_index', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.Column('safety_index', sa.DECIMAL(asdecimal=False), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.city_id'], ),
    sa.PrimaryKeyConstraint('crimerate_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crimerate')
    op.drop_table('col')
    op.drop_table('attraction')
    op.drop_table('city')
    # ### end Alembic commands ###
