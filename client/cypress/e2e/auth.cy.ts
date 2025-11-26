/// <reference types="cypress" />

describe("Auth Pages - Register & Login", () => {
  const uniqueSuffix = Date.now();
  const username = `testuser${uniqueSuffix}`;
  const email = `test${uniqueSuffix}@example.com`;
  const password = "Password123";

  // Reset localStorage before each test
  beforeEach(() => {
    cy.clearLocalStorage();
  });

  it("1. Navigate to register page", () => {
    cy.visit("/register");
    cy.contains("Create Your Account").should("exist");
  });

  it("2. Show validation errors on empty registration form", () => {
    cy.visit("/register");
    cy.get('input[name="password"]').type("123456");
    cy.get('input[name="confirmPassword"]').type("654321");
    cy.get('input[name="email"]').type("invalid-email");
    cy.get("form").submit();
    cy.contains("Passwords do not match!").should("exist");
    cy.contains("Invalid email address").should("exist");
    cy.contains("Password must be at least 6 characters long").should("not.exist"); // optional
  });

  it("3. Show email format error", () => {
    cy.visit("/register");
    cy.get('input[name="email"]').type("invalid-email");
    cy.get("form").submit();
    cy.contains("Invalid email address").should("exist");
  });

  it("4. Show password length error", () => {
    cy.visit("/register");
    cy.get('input[name="password"]').type("123");
    cy.get('input[name="confirmPassword"]').type("123");
    cy.get("form").submit();
    cy.contains("Password must be at least 6 characters long").should("exist");
  });

  it("5. Show password mismatch error", () => {
    cy.visit("/register");
    cy.get('input[name="password"]').type("Password123");
    cy.get('input[name="confirmPassword"]').type("Password321");
    cy.get("form").submit();
    cy.contains("Passwords do not match!").should("exist");
  });

  it("6. Successfully register a new user", () => {
    cy.visit("/register");
    cy.get('input[name="username"]').type(username);
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get('input[name="confirmPassword"]').type(password);
    cy.get("form").submit();

    // Should navigate to login page with success message
    cy.url().should("include", "/login");
    cy.contains("Registration successful! You can now log in.").should("exist");
  });

  it("7. Navigate to login page", () => {
    cy.visit("/login");
    cy.contains("Welcome Back 👋").should("exist");
  });

  it("8. Show login error for invalid credentials", () => {
    cy.intercept("POST", "http://localhost:5000/api/auth/login", {
      statusCode: 401,
      body: { message: "User not found or credentials do not match" },
    });

    cy.visit("/login");
    cy.get('input[name="identifier"]').type("wronguser@example.com");
    cy.get('input[name="password"]').type("WrongPassword");
    cy.get("form").submit();
    cy.contains("User not found or credentials do not match").should("exist");
  });

  it("9. Successfully login with registered user", () => {
    cy.visit("/login");
    cy.get('input[name="identifier"]').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get("form").submit();

    // Should redirect to profile page
    cy.url().should("include", "/profile");
    cy.window().then((win) => {
      const token = win.localStorage.getItem("authToken");
      expect(token).to.exist;
    });
  });

  it("10. Navigate from login to register page", () => {
    cy.visit("/login");
    cy.contains("Register").click();
    cy.url().should("include", "/register");
  });
});
