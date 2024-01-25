from alembic import op
import sqlalchemy as sa

revision = '7eee4dc5614b'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('todo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('todo')

