"""
Integration tests for Knowledge Folders API endpoints

Tests folder CRUD operations through the API layer.

Created: 2025-10-14
"""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.server.main import app


@pytest.fixture
def mock_folder_service():
    """Mock KnowledgeFolderService."""
    with patch("src.server.api_routes.knowledge_folders_api.KnowledgeFolderService") as mock:
        service_instance = mock.return_value
        service_instance.list_project_folders = AsyncMock()
        service_instance.get_folder = AsyncMock()
        service_instance.create_folder = AsyncMock()
        service_instance.update_folder = AsyncMock()
        service_instance.delete_folder = AsyncMock()
        yield service_instance


@pytest.mark.asyncio
class TestListProjectFolders:
    """Tests for GET /api/knowledge/folders endpoint."""

    async def test_list_folders_success(self, mock_folder_service):
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
        mock_folder_service.list_project_folders.return_value = mock_folders

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/knowledge/folders?project_id={project_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["folders"] == mock_folders
        mock_folder_service.list_project_folders.assert_called_once_with(project_id)

    async def test_list_folders_missing_project_id(self, mock_folder_service):
        """Should return 422 when project_id is missing."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/folders")

        assert response.status_code == 422

    async def test_list_folders_service_error(self, mock_folder_service):
        """Should return 500 on service error."""
        project_id = str(uuid4())
        mock_folder_service.list_project_folders.side_effect = Exception("Database error")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/knowledge/folders?project_id={project_id}")

        assert response.status_code == 500
        data = response.json()
        assert "Database error" in data["detail"]


@pytest.mark.asyncio
class TestGetFolder:
    """Tests for GET /api/knowledge/folders/{folder_id} endpoint."""

    async def test_get_folder_success(self, mock_folder_service):
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
        mock_folder_service.get_folder.return_value = mock_folder

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/knowledge/folders/{folder_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["folder"] == mock_folder
        mock_folder_service.get_folder.assert_called_once_with(folder_id)

    async def test_get_folder_not_found(self, mock_folder_service):
        """Should return 404 when folder not found."""
        folder_id = str(uuid4())
        mock_folder_service.get_folder.return_value = {}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/knowledge/folders/{folder_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Folder not found"

    async def test_get_folder_service_error(self, mock_folder_service):
        """Should return 500 on service error."""
        folder_id = str(uuid4())
        mock_folder_service.get_folder.side_effect = Exception("Database error")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/knowledge/folders/{folder_id}")

        assert response.status_code == 500


@pytest.mark.asyncio
class TestCreateFolder:
    """Tests for POST /api/knowledge/folders endpoint."""

    async def test_create_folder_success(self, mock_folder_service):
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
        mock_folder_service.create_folder.return_value = mock_folder

        payload = {
            "project_id": project_id,
            "folder_name": "Authentication",
            "description": "Auth docs",
            "color_hex": "#6366f1",
            "icon_name": "lock",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/folders", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["folder"] == mock_folder
        mock_folder_service.create_folder.assert_called_once()

    async def test_create_folder_with_defaults(self, mock_folder_service):
        """Should create folder with default values."""
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
        mock_folder_service.create_folder.return_value = mock_folder

        payload = {
            "project_id": project_id,
            "folder_name": "API",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/folders", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["folder"]["folder_name"] == "API"

    async def test_create_folder_missing_required_fields(self, mock_folder_service):
        """Should return 422 when required fields are missing."""
        payload = {
            "folder_name": "Authentication",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/folders", json=payload)

        assert response.status_code == 422

    async def test_create_folder_service_error(self, mock_folder_service):
        """Should return 500 on service error."""
        mock_folder_service.create_folder.side_effect = Exception("Database error")

        payload = {
            "project_id": str(uuid4()),
            "folder_name": "Authentication",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/folders", json=payload)

        assert response.status_code == 500


@pytest.mark.asyncio
class TestUpdateFolder:
    """Tests for PUT /api/knowledge/folders/{folder_id} endpoint."""

    async def test_update_folder_success(self, mock_folder_service):
        """Should update folder fields."""
        folder_id = str(uuid4())
        updated_folder = {
            "id": folder_id,
            "folder_name": "Updated Name",
            "description": "Updated description",
            "color_hex": "#10b981",
        }
        mock_folder_service.update_folder.return_value = updated_folder

        payload = {
            "folder_name": "Updated Name",
            "description": "Updated description",
            "color_hex": "#10b981",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(f"/api/knowledge/folders/{folder_id}", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["folder"] == updated_folder
        mock_folder_service.update_folder.assert_called_once()

    async def test_update_folder_partial(self, mock_folder_service):
        """Should update only provided fields."""
        folder_id = str(uuid4())
        updated_folder = {
            "id": folder_id,
            "folder_name": "New Name",
        }
        mock_folder_service.update_folder.return_value = updated_folder

        payload = {
            "folder_name": "New Name",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(f"/api/knowledge/folders/{folder_id}", json=payload)

        assert response.status_code == 200

    async def test_update_folder_not_found(self, mock_folder_service):
        """Should return 404 when folder not found."""
        folder_id = str(uuid4())
        mock_folder_service.update_folder.return_value = {}

        payload = {
            "folder_name": "New Name",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(f"/api/knowledge/folders/{folder_id}", json=payload)

        assert response.status_code == 404

    async def test_update_folder_service_error(self, mock_folder_service):
        """Should return 500 on service error."""
        folder_id = str(uuid4())
        mock_folder_service.update_folder.side_effect = Exception("Database error")

        payload = {
            "folder_name": "New Name",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(f"/api/knowledge/folders/{folder_id}", json=payload)

        assert response.status_code == 500


@pytest.mark.asyncio
class TestDeleteFolder:
    """Tests for DELETE /api/knowledge/folders/{folder_id} endpoint."""

    async def test_delete_folder_success(self, mock_folder_service):
        """Should delete folder successfully."""
        folder_id = str(uuid4())
        mock_folder_service.delete_folder.return_value = True

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(f"/api/knowledge/folders/{folder_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        mock_folder_service.delete_folder.assert_called_once_with(folder_id)

    async def test_delete_folder_not_found(self, mock_folder_service):
        """Should return 404 when folder not found."""
        folder_id = str(uuid4())
        mock_folder_service.delete_folder.return_value = False

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(f"/api/knowledge/folders/{folder_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Folder not found"

    async def test_delete_folder_service_error(self, mock_folder_service):
        """Should return 500 on service error."""
        folder_id = str(uuid4())
        mock_folder_service.delete_folder.side_effect = Exception("Database error")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(f"/api/knowledge/folders/{folder_id}")

        assert response.status_code == 500
