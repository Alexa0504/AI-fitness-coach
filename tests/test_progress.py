import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
import json
from typing import Dict, Any, Tuple


@pytest.fixture
def mock_user():
    """Returns a MagicMock user object with required methods and attributes."""
    user = MagicMock()
    user.id = 123
    user.get_progress_state.return_value = {"workouts": 5, "cals_today": 2000}
    user.last_progress_update = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    user.set_progress_state.return_value = None
    return user


@pytest.fixture
def mock_db():
    """Mocks db.session and its methods (commit, rollback)."""
    db = MagicMock()
    db.session.commit = MagicMock()
    db.session.rollback = MagicMock()
    return db


@pytest.fixture
def mock_datetime_now():
    """Mocks a fixed, predictable 'now' time for testing timestamps."""
    mock_now = datetime(2025, 10, 26, 12, 30, 0, tzinfo=timezone.utc)

    mock_dt = MagicMock()
    mock_dt.now.return_value = mock_now
    mock_dt.timezone = timezone
    return mock_dt


def progress_route_logic(
        current_user: MagicMock,
        request_data: Dict[str, Any],
        mock_db: MagicMock,
        mock_datetime: MagicMock
) -> Tuple[Dict[str, Any], int]:
    """
    Simulates the actual business logic inside the Flask route function,
    isolated from Flask context and decorators.
    """
    if not request_data:
        return {"message": "No progress data sent"}, 400

    try:
        current_user.set_progress_state(request_data)

        now = mock_datetime.now(mock_datetime.timezone.utc)
        current_user.last_progress_update = now

        mock_db.session.commit()

        return {
            "message": "Progress saved successfully",
            "progress": current_user.get_progress_state(),
            "last_update": current_user.last_progress_update.isoformat()
        }, 200

    except Exception as e:
        mock_db.session.rollback()
        return {"message": "Error saving progress", "error": str(e)}, 500


def test_logic_updates_user_state(mock_user, mock_db, mock_datetime_now):
    """Test 1: Ensures the user's setter method is called with the input data."""
    test_data = {"steps": 8500, "distance_km": 6.2}
    progress_route_logic(mock_user, test_data, mock_db, mock_datetime_now)
    mock_user.set_progress_state.assert_called_once_with(test_data)


def test_logic_commits_on_success(mock_user, mock_db, mock_datetime_now):
    """Test 2: Ensures the database commit is called after successful operation."""
    test_data = {"calories": 500}
    progress_route_logic(mock_user, test_data, mock_db, mock_datetime_now)
    mock_db.session.commit.assert_called_once()
    mock_db.session.rollback.assert_not_called()


def test_logic_returns_success_status_code(mock_user, mock_db, mock_datetime_now):
    """Test 3: Checks that the success status code (200) is returned."""
    test_data = {"duration_min": 30}
    _, status = progress_route_logic(mock_user, test_data, mock_db, mock_datetime_now)
    assert status == 200


def test_logic_updates_last_progress_update(mock_user, mock_db, mock_datetime_now):
    """Test 4: Verifies the user's last_progress_update attribute is updated."""
    progress_route_logic(mock_user, {"weight_kg": 75}, mock_db, mock_datetime_now)
    assert mock_user.last_progress_update == mock_datetime_now.now.return_value


def test_logic_returns_user_state(mock_user, mock_db, mock_datetime_now):
    """Test 5: Checks that the current state from the user getter is returned in the response."""
    response, _ = progress_route_logic(mock_user, {"temp": 1}, mock_db, mock_datetime_now)
    assert response["progress"] == mock_user.get_progress_state.return_value


def test_logic_returns_correct_timestamp_format(mock_user, mock_db, mock_datetime_now):
    """Test 6: Ensures the returned timestamp is in the correct ISO format."""
    response, _ = progress_route_logic(mock_user, {"test": 1}, mock_db, mock_datetime_now)
    expected_iso = mock_datetime_now.now.return_value.isoformat()
    assert response["last_update"] == expected_iso


def test_logic_handles_empty_data_fail(mock_user, mock_db, mock_datetime_now):
    """Test 7: Ensures the logic handles an empty input dictionary correctly."""
    response, status = progress_route_logic(mock_user, {}, mock_db, mock_datetime_now)
    assert status == 400
    assert response["message"] == "No progress data sent"
    mock_db.session.commit.assert_not_called()


def test_logic_handles_exception_rollback(mock_user, mock_db, mock_datetime_now):
    """Test 8: Confirms that a rollback is called when an exception occurs."""
    mock_user.set_progress_state.side_effect = ValueError("Invalid data")

    progress_route_logic(mock_user, {"invalid": "data"}, mock_db, mock_datetime_now)

    mock_db.session.rollback.assert_called_once()
    mock_db.session.commit.assert_not_called()


def test_logic_returns_server_error_on_exception(mock_user, mock_db, mock_datetime_now):
    """Test 9: Verifies that a 500 status code and error message are returned on failure."""
    error_message = "Database is offline"
    mock_db.session.commit.side_effect = Exception(error_message)

    response, status = progress_route_logic(mock_user, {"test": 1}, mock_db, mock_datetime_now)

    assert status == 500
    assert response["message"] == "Error saving progress"
    assert error_message in response["error"]


def test_logic_accepts_mixed_data_types(mock_user, mock_db, mock_datetime_now):
    """Test 10: Ensures complex data with mixed types can be passed successfully."""
    mixed_data = {"note": "Long run done", "is_complete": True, "rating": 4.5}
    response, status = progress_route_logic(mock_user, mixed_data, mock_db, mock_datetime_now)

    assert status == 200
    mock_user.set_progress_state.assert_called_once_with(mixed_data)
    mock_db.session.commit.assert_called_once()