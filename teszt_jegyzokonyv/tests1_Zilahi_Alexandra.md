# Backend Unit Test Report

**Author:** Zilahi Alexandra  
**Date:** 2025.11.18  
**Project:** AI Fitness Coach Backend

---

## 1. Security / Token & Password Tests

| Test ID | Test Name                                  | Module         | Purpose                     | Input / Action                   | Expected Result                      | Actual Result                        | Status |
|---------|--------------------------------------------|----------------|-----------------------------|----------------------------------|--------------------------------------|--------------------------------------|--------|
| S01     | test_hash_and_check_password_success       | security_utils | Password hashing & check    | password = "MySecurePassword123" | hashed password, check_password True | hashed password, check_password True | Passed |
| S02     | test_hash_and_check_password_failure       | security_utils | Wrong password check        | password, wrong_password         | check_password False                 | check_password False                 | Passed |
| S03     | test_hash_is_unique                        | security_utils | Salted hash uniqueness      | same password twice              | different hashes                     | different hashes                     | Passed |
| S04     | test_token_generation_and_decoding_success | security_utils | Token generation & decoding | user_id = "test-user-123"        | decoded_user_id = user_id            | decoded_user_id = user_id            | Passed |
| S05     | test_token_expiration_failure              | security_utils | Expired token               | expired token                    | decode_auth_token None               | decode_auth_token None               | Passed |
| S06     | test_token_invalid_signature_failure       | security_utils | Invalid secret key          | token signed with wrong key      | decode_auth_token None               | decode_auth_token None               | Passed |

---

## 2. Performance / Weekly Goals Tests

| Test ID | Test Name                      | Module             | Purpose                     | Input / Action                | Expected Result  | Actual Result | Status |
|---------|--------------------------------|--------------------|-----------------------------|-------------------------------|------------------|---------------|--------|
| P01     | test_no_goals                  | PerformanceService | No goals                    | empty goals list              | 0.0% performance | 0.0%          | Passed |
| P02     | test_all_goals_completed       | PerformanceService | All completed               | all goals completed           | 100%             | 100%          | Passed |
| P03     | test_partial_goals_completed   | PerformanceService | Some goals completed        | 2/5 goals completed           | 40%              | 40%           | Passed |
| P04     | test_rounding_performance      | PerformanceService | Round calculation           | 1/4 goals completed           | 25%              | 25%           | Passed |
| P05     | test_single_goal_completed     | PerformanceService | Single goal complete        | 1 goal completed              | 100%             | 100%          | Passed |
| P06     | test_single_goal_not_completed | PerformanceService | Single goal not completed   | 1 goal incomplete             | 0%               | 0%            | Passed |
| P07     | test_all_goals_not_completed   | PerformanceService | All goals incomplete        | all goals incomplete          | 0%               | 0%            | Passed |
| P08     | test_fractional_performance    | PerformanceService | Partial completion fraction | 3/10 goals completed          | 30%              | 30%           | Passed |
| P09     | test_large_number_of_goals     | PerformanceService | Large dataset               | 100 completed / 50 incomplete | 66.67%           | 66.67%        | Passed |
| P10     | test_mixed_goals_rounding      | PerformanceService | Rounding check              | 7 completed / 3 incomplete    | 70%              | 70%           | Passed |

---

## 3. Tips Endpoints Tests

| Test ID | Test Name                                | Module | Purpose                 | Input / Action               | Expected Result                | Actual Result                  | Status |
|---------|------------------------------------------|--------|-------------------------|------------------------------|--------------------------------|--------------------------------|--------|
| T01     | test_tips_returned                       | /tips  | Check any tips returned | GET /tips/general/weekly     | status 200, >0 tips            | status 200, >0 tips            | Passed |
| T02     | test_tips_max_three                      | /tips  | Max 3 tips              | GET /tips/general/weekly     | ≤3 tips                        | ≤3 tips                        | Passed |
| T03     | test_tips_random_selection               | /tips  | Random selection        | GET twice                    | responses differ               | responses differ               | Passed |
| T04     | test_tips_empty_category                 | /tips  | Nonexistent category    | GET /tips/nonexistent/weekly | status 200, empty list         | status 200, empty list         | Passed |
| T05     | test_tips_structure                      | /tips  | Check tip structure     | GET /tips/general/weekly     | keys id, category, text        | keys id, category, text        | Passed |
| T06     | test_tips_specific_text                  | /tips  | Tip exists              | query DB                     | tip found                      | tip found                      | Passed |
| T07     | test_less_than_three_tips                | /tips  | Single tip edge         | delete all, add 1 tip        | 1 tip returned                 | 1 tip returned                 | Passed |
| T08     | test_multiple_categories                 | /tips  | Category validation     | GET /tips/general/weekly     | category in allowed list       | category in allowed list       | Passed |
| T09     | test_tips_json_format                    | /tips  | JSON response           | GET /tips/general/weekly     | Content-Type: application/json | Content-Type: application/json | Passed |
| T10     | test_tips_randomness_over_multiple_calls | /tips  | Randomness              | 5 GET requests               | not all identical if >1 tip    | not all identical if >1 tip    | Passed |

---
