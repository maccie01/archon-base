"""
Unit tests for KnowledgeFolderService

Tests folder CRUD operations and error handling.

Created: 2025-10-14
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.server.services.knowledge.knowledge_folder_service import KnowledgeFolderService


@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    mock = MagicMock()
    mock.from_ = MagicMock(return_value=mock)
    mock.select = MagicMock(return_value=mock)
    mock.insert = MagicMock(return_value=mock)
    mock.update = MagicMock(return_value=mock)
    mock.delete = MagicMock(return_value=mock)
    mock.eq = MagicMock(return_value=mock)
    mock.order = MagicMock(return_value=mock)
    mock.execute = AsyncMock()
    return mock


@pytest.fixture
def folder_service(mock_supabase):
    """Create KnowledgeFolderService with mocked Supabase client."""
    with patch("src.server.services.knowledge.knowledge_folder_service.get_supabase_client", return_value=mock_supabase):
        service = KnowledgeFolderService()
        service.supabase = mock_supabase
        return service


class TestListProjectFolders:
    """Tests for list_project_folders method."""

    @pytest.mark.asyncio
    async def test_list_project_folders_success(self, folder_service, mock_supabase):
        """Should return list of folders for a project."""
        project_id = str(uuid4())
        mock_folders = [
            {
                "id": str(uuid4()),
                "project_id": project_id,
                "folder_name": "Authentication",
                "description": "Auth docs",
                "color_hex": "#6366f1",
                "icon_name": "lock",
                "sort_order": 0,
            },
            {
                "id": str(uuid4()),
                "project_id": project_id,
                "folder_name": "API",
                "description": "API docs",
                "color_hex": "#10b981",
                "icon_name": "code",
                "sort_order": 1,
            },
        ]
        mock_supabase.execute.return_value = MagicMock(data=mock_folders)

        result = await folder_service.list_project_folders(project_id)

        assert result == mock_folders
        mock_supabase.from_.assert_called_once_with("archon_project_knowledge_folders")
        mock_supabase.eq.assert_called_once_with("project_id", project_id)
        mock_supabase.order.assert_called_once_with("sort_order")

    @pytest.mark.asyncio
    async def test_list_project_folders_empty(self, folder_service, mock_supabase):
        """Should return empty list when no folders exist."""
        project_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await folder_service.list_project_folders(project_id)

        assert result == []

    @pytest.mark.asyncio
    async def test_list_project_folders_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        project_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await folder_service.list_project_folders(project_id)


class TestGetFolder:
    """Tests for get_folder method."""

    @pytest.mark.asyncio
    async def test_get_folder_success(self, folder_service, mock_supabase):
        """Should return folder by ID."""
        folder_id = str(uuid4())
        mock_folder = {
            "id": folder_id,
            "project_id": str(uuid4()),
            "folder_name": "Authentication",
            "description": "Auth docs",
            "color_hex": "#6366f1",
            "icon_name": "lock",
            "sort_order": 0,
        }
        mock_supabase.execute.return_value = MagicMock(data=[mock_folder])

        result = await folder_service.get_folder(folder_id)

        assert result == mock_folder
        mock_supabase.from_.assert_called_once_with("archon_project_knowledge_folders")
        mock_supabase.eq.assert_called_once_with("id", folder_id)

    @pytest.mark.asyncio
    async def test_get_folder_not_found(self, folder_service, mock_supabase):
        """Should return empty dict when folder not found."""
        folder_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await folder_service.get_folder(folder_id)

        assert result == {}

    @pytest.mark.asyncio
    async def test_get_folder_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        folder_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await folder_service.get_folder(folder_id)


class TestCreateFolder:
    """Tests for create_folder method."""

    @pytest.mark.asyncio
    async def test_create_folder_success(self, folder_service, mock_supabase):
        """Should create folder with all fields."""
        project_id = str(uuid4())
        folder_id = str(uuid4())
        mock_folder = {
            "id": folder_id,
            "project_id": project_id,
            "folder_name": "Authentication",
            "description": "Auth docs",
            "color_hex": "#6366f1",
            "icon_name": "lock",
            "sort_order": 0,
        }
        mock_supabase.execute.return_value = MagicMock(data=[mock_folder])

        result = await folder_service.create_folder(
            project_id=project_id,
            folder_name="Authentication",
            description="Auth docs",
            color_hex="#6366f1",
            icon_name="lock",
        )

        assert result == mock_folder
        mock_supabase.from_.assert_called_once_with("archon_project_knowledge_folders")
        mock_supabase.insert.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_folder_with_defaults(self, folder_service, mock_supabase):
        """Should create folder with default color and icon."""
        project_id = str(uuid4())
        folder_id = str(uuid4())
        mock_folder = {
            "id": folder_id,
            "project_id": project_id,
            "folder_name": "API",
            "description": None,
            "color_hex": "#6366f1",
            "icon_name": "folder",
            "sort_order": 0,
        }
        mock_supabase.execute.return_value = MagicMock(data=[mock_folder])

        result = await folder_service.create_folder(
            project_id=project_id,
            folder_name="API",
        )

        assert result == mock_folder

    @pytest.mark.asyncio
    async def test_create_folder_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        project_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await folder_service.create_folder(
                project_id=project_id,
                folder_name="Authentication",
            )


class TestUpdateFolder:
    """Tests for update_folder method."""

    @pytest.mark.asyncio
    async def test_update_folder_success(self, folder_service, mock_supabase):
        """Should update folder fields."""
        folder_id = str(uuid4())
        updated_folder = {
            "id": folder_id,
            "folder_name": "Updated Name",
            "description": "Updated description",
            "color_hex": "#10b981",
        }
        mock_supabase.execute.return_value = MagicMock(data=[updated_folder])

        result = await folder_service.update_folder(
            folder_id=folder_id,
            folder_name="Updated Name",
            description="Updated description",
            color_hex="#10b981",
        )

        assert result == updated_folder
        mock_supabase.from_.assert_called_once_with("archon_project_knowledge_folders")
        mock_supabase.eq.assert_called_once_with("id", folder_id)
        mock_supabase.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_folder_partial(self, folder_service, mock_supabase):
        """Should update only provided fields."""
        folder_id = str(uuid4())
        updated_folder = {
            "id": folder_id,
            "folder_name": "New Name",
        }
        mock_supabase.execute.return_value = MagicMock(data=[updated_folder])

        result = await folder_service.update_folder(
            folder_id=folder_id,
            folder_name="New Name",
        )

        assert result == updated_folder

    @pytest.mark.asyncio
    async def test_update_folder_not_found(self, folder_service, mock_supabase):
        """Should return empty dict when folder not found."""
        folder_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await folder_service.update_folder(
            folder_id=folder_id,
            folder_name="New Name",
        )

        assert result == {}

    @pytest.mark.asyncio
    async def test_update_folder_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        folder_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await folder_service.update_folder(
                folder_id=folder_id,
                folder_name="New Name",
            )


class TestDeleteFolder:
    """Tests for delete_folder method."""

    @pytest.mark.asyncio
    async def test_delete_folder_success(self, folder_service, mock_supabase):
        """Should delete folder successfully."""
        folder_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=[{"id": folder_id}])

        result = await folder_service.delete_folder(folder_id)

        assert result is True
        mock_supabase.from_.assert_called_once_with("archon_project_knowledge_folders")
        mock_supabase.eq.assert_called_once_with("id", folder_id)
        mock_supabase.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_folder_not_found(self, folder_service, mock_supabase):
        """Should return False when folder not found."""
        folder_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await folder_service.delete_folder(folder_id)

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_folder_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        folder_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await folder_service.delete_folder(folder_id)
