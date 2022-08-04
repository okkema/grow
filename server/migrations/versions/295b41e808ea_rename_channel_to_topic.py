"""rename channel to topic

Revision ID: 295b41e808ea
Revises: d8d84a3cc801
Create Date: 2022-08-03 04:39:24.095901+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "295b41e808ea"
down_revision = "d8d84a3cc801"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "sensor_readings",
        column_name="channel",
        new_column_name="topic",
        existing_type=sa.VARCHAR(32),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "sensor_readings",
        column_name="topic",
        new_column_name="channel",
        existing_type=sa.VARCHAR(32),
    )
    # ### end Alembic commands ###