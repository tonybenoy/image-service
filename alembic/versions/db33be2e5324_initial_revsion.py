"""Initial revsion

Revision ID: db33be2e5324
Revises:
Create Date: 2023-02-09 00:36:26.052707

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "db33be2e5324"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("processed", sa.Integer(), nullable=True),
        sa.Column("processed_key", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("images")
    # ### end Alembic commands ###
