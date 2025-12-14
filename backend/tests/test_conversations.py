"""Tests for conversations API endpoints."""
import uuid
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import (
    Conversation,
    ConversationStatus,
    InstagramAccount,
    InstagramUser,
    Message,
    MessageDirection,
    MessageType,
    User,
)
from src.auth.service import get_password_hash


async def create_test_user(db: AsyncSession, email: str = "test@example.com") -> User:
    """Helper to create a test user."""
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_test_instagram_account(
    db: AsyncSession, user_id: str, page_id: str = "12345"
) -> InstagramAccount:
    """Helper to create a test Instagram account."""
    account = InstagramAccount(
        id=str(uuid.uuid4()),
        user_id=user_id,
        instagram_page_id=page_id,
        access_token="test_token",
        is_active=True,
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


async def create_test_instagram_user(
    db: AsyncSession, instagram_user_id: str = "user_123"
) -> InstagramUser:
    """Helper to create a test Instagram user."""
    ig_user = InstagramUser(
        id=str(uuid.uuid4()),
        instagram_user_id=instagram_user_id,
        username="testuser",
        name="Test Instagram User",
        profile_picture_url="https://example.com/avatar.jpg",
    )
    db.add(ig_user)
    await db.commit()
    await db.refresh(ig_user)
    return ig_user


async def create_test_conversation(
    db: AsyncSession,
    instagram_account_id: str,
    instagram_user_id: str,
    status: ConversationStatus = ConversationStatus.ACTIVE,
    unread_count: int = 0,
) -> Conversation:
    """Helper to create a test conversation."""
    conv = Conversation(
        id=str(uuid.uuid4()),
        instagram_account_id=instagram_account_id,
        instagram_user_id=instagram_user_id,
        status=status,
        unread_count=unread_count,
        last_message_at=datetime.now(timezone.utc),
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


async def create_test_message(
    db: AsyncSession,
    conversation_id: str,
    content: str = "Hello",
    direction: MessageDirection = MessageDirection.INBOUND,
    is_ai_generated: bool = False,
) -> Message:
    """Helper to create a test message."""
    msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        instagram_message_id=f"mid_{uuid.uuid4().hex[:10]}",
        direction=direction,
        message_type=MessageType.TEXT,
        content=content,
        is_ai_generated=is_ai_generated,
        instagram_timestamp=datetime.now(timezone.utc),
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def get_auth_token(client: AsyncClient, email: str = "test@example.com") -> str:
    """Helper to get auth token for a user."""
    response = await client.post(
        "/auth/login",
        data={"username": email, "password": "testpassword123"},
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_list_conversations_success(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test listing conversations for authenticated user."""
    # Create test data
    user = await create_test_user(db_session, "conv_list@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_list")
    ig_user = await create_test_instagram_user(db_session, "ig_user_list")
    await create_test_conversation(db_session, ig_account.id, ig_user.id)

    # Get auth token
    token = await get_auth_token(client, "conv_list@example.com")

    # List conversations
    response = await client.get(
        "/api/conversations",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "meta" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["instagram_user"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_list_conversations_unauthenticated(client: AsyncClient) -> None:
    """Test listing conversations without authentication."""
    response = await client.get("/api/conversations")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_conversations_empty(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test listing conversations when none exist."""
    # Create user without any conversations
    await create_test_user(db_session, "no_convs@example.com")
    token = await get_auth_token(client, "no_convs@example.com")

    response = await client.get(
        "/api/conversations",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["meta"]["total"] == 0


@pytest.mark.asyncio
async def test_list_conversations_pagination(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test pagination of conversations."""
    # Create user with multiple conversations
    user = await create_test_user(db_session, "pagination@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_pag")

    # Create 5 conversations
    for i in range(5):
        ig_user = await create_test_instagram_user(db_session, f"ig_user_pag_{i}")
        await create_test_conversation(db_session, ig_account.id, ig_user.id)

    token = await get_auth_token(client, "pagination@example.com")

    # Get first page with page_size=2
    response = await client.get(
        "/api/conversations?page=1&page_size=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["meta"]["total"] == 5
    assert data["meta"]["has_next"] is True
    assert data["meta"]["has_previous"] is False


@pytest.mark.asyncio
async def test_get_conversation_success(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test getting a single conversation."""
    user = await create_test_user(db_session, "get_conv@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_get")
    ig_user = await create_test_instagram_user(db_session, "ig_user_get")
    conv = await create_test_conversation(db_session, ig_account.id, ig_user.id)

    token = await get_auth_token(client, "get_conv@example.com")

    response = await client.get(
        f"/api/conversations/{conv.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conv.id
    assert data["instagram_user"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_conversation_not_found(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test getting a non-existent conversation."""
    await create_test_user(db_session, "not_found@example.com")
    token = await get_auth_token(client, "not_found@example.com")

    fake_id = str(uuid.uuid4())
    response = await client.get(
        f"/api/conversations/{fake_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_conversation_wrong_user(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test that users cannot access other users' conversations."""
    # Create first user with a conversation
    user1 = await create_test_user(db_session, "user1@example.com")
    ig_account = await create_test_instagram_account(db_session, user1.id, "page_u1")
    ig_user = await create_test_instagram_user(db_session, "ig_user_u1")
    conv = await create_test_conversation(db_session, ig_account.id, ig_user.id)

    # Create second user
    await create_test_user(db_session, "user2@example.com")
    token2 = await get_auth_token(client, "user2@example.com")

    # Try to access user1's conversation
    response = await client.get(
        f"/api/conversations/{conv.id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_messages_success(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test getting messages for a conversation."""
    user = await create_test_user(db_session, "messages@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_msg")
    ig_user = await create_test_instagram_user(db_session, "ig_user_msg")
    conv = await create_test_conversation(db_session, ig_account.id, ig_user.id)

    # Create messages
    await create_test_message(
        db_session, conv.id, "Hello!", MessageDirection.INBOUND
    )
    await create_test_message(
        db_session, conv.id, "Hi there!", MessageDirection.OUTBOUND, is_ai_generated=True
    )

    token = await get_auth_token(client, "messages@example.com")

    response = await client.get(
        f"/api/conversations/{conv.id}/messages",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["meta"]["total"] == 2


@pytest.mark.asyncio
async def test_get_messages_pagination(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test message pagination."""
    user = await create_test_user(db_session, "msg_pag@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_mpag")
    ig_user = await create_test_instagram_user(db_session, "ig_user_mpag")
    conv = await create_test_conversation(db_session, ig_account.id, ig_user.id)

    # Create 10 messages
    for i in range(10):
        direction = MessageDirection.INBOUND if i % 2 == 0 else MessageDirection.OUTBOUND
        await create_test_message(db_session, conv.id, f"Message {i}", direction)

    token = await get_auth_token(client, "msg_pag@example.com")

    response = await client.get(
        f"/api/conversations/{conv.id}/messages?page=1&page_size=5",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["meta"]["total"] == 10
    assert data["meta"]["has_next"] is True


@pytest.mark.asyncio
async def test_update_conversation_status(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test updating conversation status."""
    user = await create_test_user(db_session, "status@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_st")
    ig_user = await create_test_instagram_user(db_session, "ig_user_st")
    conv = await create_test_conversation(
        db_session, ig_account.id, ig_user.id, ConversationStatus.ACTIVE
    )

    token = await get_auth_token(client, "status@example.com")

    response = await client.patch(
        f"/api/conversations/{conv.id}/status",
        json={"status": "archived"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "archived"


@pytest.mark.asyncio
async def test_mark_conversation_as_read(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test marking conversation as read."""
    user = await create_test_user(db_session, "read@example.com")
    ig_account = await create_test_instagram_account(db_session, user.id, "page_rd")
    ig_user = await create_test_instagram_user(db_session, "ig_user_rd")
    conv = await create_test_conversation(
        db_session, ig_account.id, ig_user.id, unread_count=5
    )

    token = await get_auth_token(client, "read@example.com")

    response = await client.post(
        f"/api/conversations/{conv.id}/read",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["unread_count"] == 0


@pytest.mark.asyncio
async def test_only_own_conversations_visible(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Test that users only see their own conversations."""
    # Create two users with their own conversations
    user1 = await create_test_user(db_session, "owner1@example.com")
    user2 = await create_test_user(db_session, "owner2@example.com")

    ig_account1 = await create_test_instagram_account(db_session, user1.id, "page_o1")
    ig_account2 = await create_test_instagram_account(db_session, user2.id, "page_o2")

    ig_user1 = await create_test_instagram_user(db_session, "ig_user_o1")
    ig_user2 = await create_test_instagram_user(db_session, "ig_user_o2")

    await create_test_conversation(db_session, ig_account1.id, ig_user1.id)
    await create_test_conversation(db_session, ig_account2.id, ig_user2.id)

    # User1 should only see their conversation
    token1 = await get_auth_token(client, "owner1@example.com")
    response1 = await client.get(
        "/api/conversations",
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1["items"]) == 1

    # User2 should only see their conversation
    token2 = await get_auth_token(client, "owner2@example.com")
    response2 = await client.get(
        "/api/conversations",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2["items"]) == 1
