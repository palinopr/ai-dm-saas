"""Create conversation and message tables

Revision ID: 002
Revises: 001
Create Date: 2024-01-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create instagram_accounts table
    op.create_table(
        'instagram_accounts',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('instagram_page_id', sa.String(255), nullable=False),
        sa.Column('instagram_username', sa.String(255), nullable=True),
        sa.Column('access_token', sa.String(500), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_instagram_accounts_user_id', 'instagram_accounts', ['user_id'])
    op.create_index('ix_instagram_accounts_instagram_page_id', 'instagram_accounts', ['instagram_page_id'], unique=True)

    # Create instagram_users table
    op.create_table(
        'instagram_users',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('instagram_user_id', sa.String(255), nullable=False),
        sa.Column('username', sa.String(255), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('profile_picture_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_instagram_users_instagram_user_id', 'instagram_users', ['instagram_user_id'], unique=True)

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('instagram_account_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('instagram_user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('status', sa.Enum('active', 'archived', 'closed', name='conversationstatus'), nullable=False, server_default='active'),
        sa.Column('last_message_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('unread_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['instagram_account_id'], ['instagram_accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['instagram_user_id'], ['instagram_users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('instagram_account_id', 'instagram_user_id', name='uq_conversations_account_user'),
    )
    op.create_index('ix_conversations_instagram_account_id', 'conversations', ['instagram_account_id'])
    op.create_index('ix_conversations_instagram_user_id', 'conversations', ['instagram_user_id'])
    op.create_index('ix_conversations_last_message_at', 'conversations', ['last_message_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('instagram_message_id', sa.String(255), nullable=True),
        sa.Column('direction', sa.Enum('inbound', 'outbound', name='messagedirection'), nullable=False),
        sa.Column('message_type', sa.Enum('text', 'image', 'video', 'audio', 'sticker', name='messagetype'), nullable=False, server_default='text'),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('intent', sa.String(50), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('is_ai_generated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('instagram_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('ix_messages_instagram_message_id', 'messages', ['instagram_message_id'], unique=True)
    op.create_index('ix_messages_direction', 'messages', ['direction'])
    op.create_index('ix_messages_created_at', 'messages', ['created_at'])


def downgrade() -> None:
    # Drop messages table
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_messages_direction', table_name='messages')
    op.drop_index('ix_messages_instagram_message_id', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    # Drop conversations table
    op.drop_index('ix_conversations_last_message_at', table_name='conversations')
    op.drop_index('ix_conversations_instagram_user_id', table_name='conversations')
    op.drop_index('ix_conversations_instagram_account_id', table_name='conversations')
    op.drop_table('conversations')

    # Drop instagram_users table
    op.drop_index('ix_instagram_users_instagram_user_id', table_name='instagram_users')
    op.drop_table('instagram_users')

    # Drop instagram_accounts table
    op.drop_index('ix_instagram_accounts_instagram_page_id', table_name='instagram_accounts')
    op.drop_index('ix_instagram_accounts_user_id', table_name='instagram_accounts')
    op.drop_table('instagram_accounts')

    # Drop enum types
    op.execute('DROP TYPE IF EXISTS messagetype')
    op.execute('DROP TYPE IF EXISTS messagedirection')
    op.execute('DROP TYPE IF EXISTS conversationstatus')
