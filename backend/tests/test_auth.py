"""Tests for authentication endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    """Test user registration endpoint."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    """Test that duplicate email registration fails."""
    # First registration
    await client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "securepassword123",
        },
    )
    # Second registration with same email
    response = await client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "differentpassword123",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    """Test successful login."""
    # Register user first
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "securepassword123",
        },
    )
    # Login
    response = await client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    """Test login with invalid credentials."""
    response = await client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient) -> None:
    """Test getting current user info."""
    # Register and login
    await client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "password": "securepassword123",
            "full_name": "Current User",
        },
    )
    login_response = await client.post(
        "/auth/login",
        data={
            "username": "me@example.com",
            "password": "securepassword123",
        },
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Current User"


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient) -> None:
    """Test getting current user without token."""
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_password_validation(client: AsyncClient) -> None:
    """Test password validation (minimum length)."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "short@example.com",
            "password": "short",  # Less than 8 characters
        },
    )
    assert response.status_code == 422  # Validation error
