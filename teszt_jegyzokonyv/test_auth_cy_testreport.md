# Auth Pages — Register & Login Test Report

**Author:** Tóth Tamás  
**Date:** 2025-11-26  
**Module:** `auth.cy.ts` (Cypress E2E Tests)

| Test Name | Description | Expected Result | Actual Result | Status |
|-----------|-------------|----------------|---------------|--------|
| **1. Navigate to register page** | Verifies that the register page loads successfully | "Create Your Account" visible | "Create Your Account" visible | ✅ Passed |
| **2. Show validation errors on empty registration form** | Ensures validation errors appear when submitting invalid inputs | Errors for mismatched passwords & invalid email shown | Errors appeared as expected | ✅ Passed |
| **3. Show email format error** | Checks validation for incorrectly formatted email | "Invalid email address" shown | Error appeared as expected | ✅ Passed |
| **4. Show password length error** | Ensures password length validation works | "Password must be at least 6 characters long" shown | Error appeared as expected | ✅ Passed |
| **5. Show password mismatch error** | Ensures mismatch password validation triggers | "Passwords do not match!" shown | Error appeared as expected | ✅ Passed |
| **6. Successfully register a new user** | Tests full registration flow with a unique user | Redirect to `/login`, success message shown | Redirect occurred and message appeared | ✅ Passed |
| **7. Navigate to login page** | Validates that the login page loads properly | "Welcome Back 👋" visible | Text visible | ✅ Passed |
| **8. Show login error for invalid credentials** | Ensures backend error message shows on failed login | "User not found or credentials do not match" displayed | Message displayed after intercept mock | ✅ Passed |
| **9. Successfully login with registered user** | Tests full login flow with generated credentials | Redirect to `/profile`, token stored in localStorage | Redirect occurred and token stored | ✅ Passed |
| **10. Navigate from login to register page** | Tests navigation link from login → register | URL changes to `/register` | URL updated correctly | ✅ Passed |

---

## **Summary**

- **Total Tests:** 10  
- **Passed:** 10  
- **Failed:** 0  
- **Pass Rate:** **100%**

All authentication E2E tests passed successfully. The registration and login flows behave as expected, including validation logic, error handling, API interactions (via intercepts), and navigation between authentication pages.
