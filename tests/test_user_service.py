import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, Token
from app.schemas.base import BaseResponse


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_repository):
    return UserService(mock_repository)


@pytest.fixture
def sample_user():
    return UserResponse(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at="2024-01-01T00:00:00",
        updated_at=None
    )


@pytest.mark.asyncio
async def test_create_user_success(user_service, mock_repository, sample_user):
    # Arrange
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    mock_repository.get_by_username.return_value = None
    mock_repository.get_by_email.return_value = None
    mock_repository.create.return_value = sample_user

    # Act
    response = await user_service.create_user(user_data, "test-request-id")

    # Assert
    assert isinstance(response, BaseResponse)
    assert response.status == status.HTTP_200_OK
    assert response.msg == "User created successfully"
    assert response.detail == sample_user
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_username_exists(user_service, mock_repository):
    # Arrange
    user_data = UserCreate(
        username="existinguser",
        email="test@example.com",
        password="password123"
    )
    mock_repository.get_by_username.return_value = MagicMock()

    # Act
    response = await user_service.create_user(user_data, "test-request-id")

    # Assert
    assert response.status == status.HTTP_400_BAD_REQUEST
    assert "Username already registered" in response.msg
    mock_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_success(user_service, mock_repository, sample_user):
    # Arrange
    mock_repository.get_by_username.return_value = MagicMock(
        username="testuser",
        hashed_password="$2b$12$hashedpassword"
    )

    # Act
    response = await user_service.authenticate_user(
        "testuser",
        "password123",
        "test-request-id"
    )

    # Assert
    assert response.status == status.HTTP_200_OK
    assert "Authentication successful" in response.msg


@pytest.mark.asyncio
async def test_get_user_success(user_service, mock_repository, sample_user):
    # Arrange
    mock_repository.get_by_id.return_value = sample_user

    # Act
    response = await user_service.get_user(1, "test-request-id")

    # Assert
    assert response.status == status.HTTP_200_OK
    assert response.detail == sample_user


@pytest.mark.asyncio
async def test_update_user_success(user_service, mock_repository, sample_user):
    # Arrange
    update_data = UserUpdate(username="newusername")
    mock_repository.get_by_id.return_value = sample_user
    mock_repository.get_by_username.return_value = None
    mock_repository.update.return_value = sample_user

    # Act
    response = await user_service.update_user(1, update_data, "test-request-id")

    # Assert
    assert response.status == status.HTTP_200_OK
    assert "User updated successfully" in response.msg


@pytest.mark.asyncio
async def test_delete_user_success(user_service, mock_repository, sample_user):
    # Arrange
    mock_repository.get_by_id.return_value = sample_user
    mock_repository.delete.return_value = True

    # Act
    response = await user_service.delete_user(1, "test-request-id")

    # Assert
    assert response.status == status.HTTP_200_OK
    assert "User deleted successfully" in response.msg


@pytest.mark.asyncio
async def test_create_access_token_success(user_service):
    # Act
    response = await user_service.create_access_token("testuser", "test-request-id")

    # Assert
    assert response.status == status.HTTP_200_OK
    assert isinstance(response.detail, Token)
    assert response.detail.token_type == "bearer" 