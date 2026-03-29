from unittest.mock import Mock

from schemas.task import TaskCreate
from services.task_service import TaskService


def test_task_service_create_task_calls_repository():
    repo = Mock()
    expected_result = {"id": 1, "title": "Test"}
    repo.create_task.return_value = expected_result
    service = TaskService(task_repository=repo)

    task_data = TaskCreate(title="Test")
    result = service.create_task(task_data=task_data, owner_id=5)

    repo.create_task.assert_called_once_with(task_data=task_data, owner_id=5)
    assert result == expected_result
