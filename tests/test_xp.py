import pytest
from unittest.mock import MagicMock, patch
from backend.routes import xp, progress
from backend.services import xp_service
from datetime import datetime, timezone

class TestXPService:
    @pytest.fixture
    def mock_user(self):
        user = MagicMock()
        user.user_goals = []
        user.xp = 0
        user.level = 1
        return user

    def test_update_weekly_xp_no_goals(self, mock_user):
        success, message = xp_service.update_weekly_xp(mock_user)
        assert not success
        assert message == "No weekly goals completed."

    def test_update_weekly_xp_with_completed_goal(self, mock_user):
        mock_user.user_goals = [MagicMock(is_completed=True)]
        with patch('backend.models.db.session.commit') as commit_mock:
            success, message = xp_service.update_weekly_xp(mock_user)
            assert success
            assert message == "XP updated."
            commit_mock.assert_called_once()

    def test_check_level_up_exact_level(self, mock_user):
        mock_user.xp = 1200
        leveled_up = xp_service.check_level_up(mock_user)
        assert leveled_up
        assert mock_user.level == 2
        assert mock_user.xp == 0

    def test_check_level_up_multiple_levels(self, mock_user):
        mock_user.xp = 2500
        leveled_up = xp_service.check_level_up(mock_user)
        assert leveled_up
        assert mock_user.level == 3
        assert mock_user.xp == 100

    def test_check_level_up_no_level(self, mock_user):
        mock_user.xp = 500
        leveled_up = xp_service.check_level_up(mock_user)
        assert not leveled_up
        assert mock_user.level == 1
        assert mock_user.xp == 500

    def test_get_xp_status(self, mock_user):
        mock_user.xp = 100
        mock_user.level = 2
        status = xp_service.get_xp_status(mock_user)
        assert status['xp'] == 100
        assert status['level'] == 2
        assert status['xp_to_next_level'] == 1100

    def test_update_weekly_xp_multiple_goals(self, mock_user):
        mock_user.user_goals = [MagicMock(is_completed=True), MagicMock(is_completed=True)]
        with patch('backend.models.db.session.commit') as commit_mock:
            success, message = xp_service.update_weekly_xp(mock_user)
            assert success
            assert message == "XP updated."

    def test_update_weekly_xp_level_up(self, mock_user):
        mock_user.user_goals = [MagicMock(is_completed=True)]
        mock_user.xp = 1000
        with patch('backend.models.db.session.commit') as commit_mock:
            success, _ = xp_service.update_weekly_xp(mock_user)
            assert success
            assert mock_user.level == 2

    def test_get_xp_status_after_level_up(self, mock_user):
        mock_user.xp = 1250
        mock_user.level = 1
        xp_service.check_level_up(mock_user)
        status = xp_service.get_xp_status(mock_user)
        assert status['level'] == 2
        assert status['xp_to_next_level'] == 1200 - mock_user.xp

    def test_update_weekly_xp_rollback_on_error(self, mock_user):
        mock_user.user_goals = [MagicMock(is_completed=True)]
        with patch('backend.models.db.session.commit', side_effect=Exception("DB Error")):
            with pytest.raises(Exception):
                xp_service.update_weekly_xp(mock_user)
