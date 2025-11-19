# XP Service Test Report

**Author:** Tóth Tamás
**Date:** 2025-11-19  
**Module:** `xp_service`

| Test Name | Description | Expected Result | Actual Result | Status |
|-----------|-------------|----------------|---------------|--------|
| `test_update_weekly_xp_no_goals` | Update weekly XP when user has no goals | `success=False`, `message="No weekly goals completed."` | `success=False`, `message="No weekly goals completed."` | Passed |
| `test_update_weekly_xp_with_completed_goal` | Update weekly XP when user has one completed goal | `success=True`, `message="XP updated."` | `success=True`, `message="XP updated."` | Passed |
| `test_check_level_up_exact_level` | Check level up when XP is exactly at level threshold | `leveled_up=True`, `level=2`, `xp=0` | `leveled_up=True`, `level=2`, `xp=0` | Passed |
| `test_check_level_up_multiple_levels` | Check level up when XP exceeds multiple levels | `leveled_up=True`, `level=3`, `xp=100` | `leveled_up=True`, `level=3`, `xp=100` | Passed |
| `test_check_level_up_no_level` | Check level up when XP is below level threshold | `leveled_up=False`, `level=1`, `xp=500` | `leveled_up=False`, `level=1`, `xp=500` | Passed |
| `test_get_xp_status` | Get XP status for a user | `xp=100`, `level=2`, `xp_to_next_level=1100` | `xp=100`, `level=2`, `xp_to_next_level=1100` | Passed |
| `test_update_weekly_xp_multiple_goals` | Update weekly XP when multiple goals are completed | `success=True`, `message="XP updated."` | `success=True`, `message="XP updated."` | Passed |
| `test_update_weekly_xp_level_up` | Update weekly XP that triggers a level up | `success=True`, `level=2` | `success=True`, `level=2` | Passed |
| `test_get_xp_status_after_level_up` | Get XP status after leveling up | `level=2`, `xp_to_next_level=1200 - xp` | `level=2`, `xp_to_next_level=1200 - xp` | Passed |
| `test_update_weekly_xp_rollback_on_error` | Ensure rollback occurs if DB commit fails | Exception raised | Exception raised | Passed |

**Summary:**  

- Total Tests: 10  
- Passed: 10  
- Failed: 0  
- Pass Rate: 100%  
