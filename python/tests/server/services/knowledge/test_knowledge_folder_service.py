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
    mock.single = MagicMock(return_value=mock)
    mock.execute = MagicMock()  # Synchronous, not async
    return mock


@pytest.fixture
def folder_service(mock_supabase):
    """Create KnowledgeFolderService with mocked Supabase client."""
    service = KnowledgeFolderService(mock_supabase)
    return service


class TestListProjectFolders:
    """Tests for list_project_folders method."""

    @pytest.mark.asyncio
    async def test_list_project_folders_success(self, folder_service, mock_supabase):
        """Should return list of folders for a project."""
        project_id = str(uuid4())
        folder_id_1 = str(uuid4())
        folder_id_2 = str(uuid4())
        mock_folders = [
            {
                "id": folder_id_1,
                "project_id": project_id,
                "folder_name": "Authentication",
                "description": "Auth docs",
                "color_hex": "#6366f1",
                "icon_name": "lock",
                "sort_order": 0,
            },
            {
                "id": folder_id_2,
                "project_id": project_id,
                "folder_name": "API",
                "description": "API docs",
                "color_hex": "#10b981",
                "icon_name": "code",
                "sort_order": 1,
            },
        ]

        # Mock the folder query
        mock_supabase.execute.return_value = MagicMock(data=mock_folders)

        # Mock the source count queries (returns count attribute)
        count_result = MagicMock()
        count_result.count = 5

        # Create a side effect that returns folder data first, then count results
        def execute_side_effect():
            if mock_supabase.execute.call_count == 1:
                return MagicMock(data=mock_folders)
            else:
                return count_result

        mock_supabase.execute.side_effect = execute_side_effect

        result = await folder_service.list_project_folders(project_id)

        # Check that folders were returned with source_count added
        assert len(result) == 2
        assert result[0]["folder_name"] == "Authentication"
        assert "source_count" in result[0]
        assert result[1]["folder_name"] == "API"
        assert "source_count" in result[1]

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
        mock_supabase.execute.return_value = MagicMock(data=mock_folder)

        result = await folder_service.get_folder(folder_id)

        assert result == mock_folder
        mock_supabase.from_.assert_called_once_with("archon_project_knowledge_folders")
        mock_supabase.eq.assert_called_once_with("id", folder_id)

    @pytest.mark.asyncio
    async def test_get_folder_not_found(self, folder_service, mock_supabase):
        """Should return None when folder not found."""
        folder_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=None)

        result = await folder_service.get_folder(folder_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_folder_error(self, folder_service, mock_supabase):
        """Should return None and log warning on database error."""
        folder_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        result = await folder_service.get_folder(folder_id)

        # get_folder catches exceptions and returns None
        assert result is None


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

        updates = {
            "folder_name": "Updated Name",
            "description": "Updated description",
            "color_hex": "#10b981",
        }
        result = await folder_service.update_folder(folder_id, updates)

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

        updates = {"folder_name": "New Name"}
        result = await folder_service.update_folder(folder_id, updates)

        assert result == updated_folder

    @pytest.mark.asyncio
    async def test_update_folder_not_found(self, folder_service, mock_supabase):
        """Should raise exception when folder not found."""
        folder_id = str(uuid4())
        mock_supabase.execute.return_value = MagicMock(data=[])

        updates = {"folder_name": "New Name"}
        with pytest.raises(Exception, match="not found"):
            await folder_service.update_folder(folder_id, updates)

    @pytest.mark.asyncio
    async def test_update_folder_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        folder_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        updates = {"folder_name": "New Name"}
        with pytest.raises(Exception, match="Database error"):
            await folder_service.update_folder(folder_id, updates)


class TestDeleteFolder:
    """Tests for delete_folder method."""

    @pytest.mark.asyncio
    async def test_delete_folder_success(self, folder_service, mock_supabase):
        """Should delete folder successfully."""
        folder_id = str(uuid4())
        # Mock both the source count query and the delete query
        count_result = MagicMock()
        count_result.count = 3
        delete_result = MagicMock(data=[{"id": folder_id}])

        # First call returns count, second returns delete result
        mock_supabase.execute.side_effect = [count_result, delete_result]

        result = await folder_service.delete_folder(folder_id)

        assert result is True

    @pytest.mark.asyncio
    async def test_delete_folder_always_returns_true(self, folder_service, mock_supabase):
        """Should return True even if folder doesn't exist (idempotent)."""
        folder_id = str(uuid4())
        # Mock both queries
        count_result = MagicMock()
        count_result.count = 0
        delete_result = MagicMock(data=[])

        mock_supabase.execute.side_effect = [count_result, delete_result]

        result = await folder_service.delete_folder(folder_id)

        # delete_folder always returns True or raises
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_folder_error(self, folder_service, mock_supabase):
        """Should raise exception on database error."""
        folder_id = str(uuid4())
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await folder_service.delete_folder(folder_id)
