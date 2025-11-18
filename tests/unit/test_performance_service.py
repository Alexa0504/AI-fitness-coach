import pytest
from unittest.mock import patch, MagicMock
from backend.services.performance_service import PerformanceService
from backend.models import UserGoal

def test_no_goals():
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = []
        assert PerformanceService.calculate_weekly_performance(1) == 0.0

def test_all_goals_completed():
    mock_goals = [MagicMock(is_completed=True) for _ in range(5)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 100.0

def test_partial_goals_completed():
    mock_goals = [MagicMock(is_completed=True) for _ in range(2)] + [MagicMock(is_completed=False) for _ in range(3)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 40.0

def test_rounding_performance():
    mock_goals = [MagicMock(is_completed=True)] + [MagicMock(is_completed=False) for _ in range(3)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 25.0

def test_single_goal_completed():
    mock_goals = [MagicMock(is_completed=True)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 100.0

def test_single_goal_not_completed():
    mock_goals = [MagicMock(is_completed=False)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 0.0

# --- 7. Több cél, mind nem teljesített ---
def test_all_goals_not_completed():
    mock_goals = [MagicMock(is_completed=False) for _ in range(4)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 0.0

# --- 8. Minden cél részben teljesített, kerekítés ---
def test_fractional_performance():
    mock_goals = [MagicMock(is_completed=True) for _ in range(3)] + [MagicMock(is_completed=False) for _ in range(7)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 30.0

# --- 9. Nagy számú cél ---
def test_large_number_of_goals():
    mock_goals = [MagicMock(is_completed=True) for _ in range(100)] + [MagicMock(is_completed=False) for _ in range(50)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 66.67

# --- 10. Vegyes teljesítés, kerekítés ---
def test_mixed_goals_rounding():
    mock_goals = [MagicMock(is_completed=True) for _ in range(7)] + [MagicMock(is_completed=False) for _ in range(3)]
    with patch("backend.models.UserGoal.query") as mock_query:
        mock_query.filter_by.return_value.all.return_value = mock_goals
        assert PerformanceService.calculate_weekly_performance(1) == 70.0