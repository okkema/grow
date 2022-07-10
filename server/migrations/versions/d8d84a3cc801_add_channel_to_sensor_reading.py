"""Add channel to sensor reading

Revision ID: d8d84a3cc801
Revises: dad098d3229e
Create Date: 2022-07-10 04:46:30.549204+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d8d84a3cc801"
down_revision = "dad098d3229e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sensor_readings",
        sa.Column("channel", sa.String(length=32), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sensor_readings", "channel")
    # ### end Alembic commands ###