from backend.utils import score_utils

def test_calculate_mock_score_workout():
    assert score_utils.calculate_mock_score("workout") == 80

def test_calculate_mock_score_diet():
    assert score_utils.calculate_mock_score("diet") == 90

def test_calculate_mock_score_other():
    assert score_utils.calculate_mock_score("other") == 70
