"""Bridge migration - placeholder for legacy revision

This migration exists to bridge a gap between a database that was
previously migrated with revision 'e8f4b3c5d2a1' and the current
migration chain that starts at '001'.

Revision ID: e8f4b3c5d2a1
Revises:
Create Date: 2024-01-01

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'e8f4b3c5d2a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op - this revision already exists in the database."""
    pass


def downgrade() -> None:
    """No-op - this is a placeholder revision."""
    pass
