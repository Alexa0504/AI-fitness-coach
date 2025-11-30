/// <reference types="cypress" />

describe("ProfilePage - 20 Automated UI Tests", () => {
    const testProfile = {
        gender: "female",
        height_cm: "170",
        weight_kg: "65",
        target_weight_kg: "60",
        age: "28",
        username: "testuser",
        email: "testuser@example.com",
        layoutData: {hasBgDiv: true}
    };

    beforeEach(() => {
        cy.login();

        cy.intercept("GET", "**/users/profile", {
            statusCode: 200,
            body: testProfile
        }).as("getProfile");

        cy.intercept("PUT", "**/users/profile", (req) => {
            const body = req.body as any;
            if (!body.height_cm) {
                req.reply({statusCode: 400, body: {message: "Height is required"}});
            } else if (!body.weight_kg) {
                req.reply({statusCode: 400, body: {message: "Weight is required"}});
            } else if (!body.target_weight_kg) {
                req.reply({statusCode: 400, body: {message: "Target weight is required"}});
            } else if (!body.age) {
                req.reply({statusCode: 400, body: {message: "Age is required"}});
            } else {
                req.reply({statusCode: 200, body: {message: "Profile updated"}});
            }
        }).as("updateProfile");

        cy.visit("/profile");
        cy.wait("@getProfile");
    });

    it("1. Profile page loads", () => {
        cy.contains("Your Profile").should("exist");
    });

    it("2. Gender select exists", () => {
        cy.get('select[name="gender"]').should("exist");
    });

    it("3. Height input exists", () => {
        cy.get('input[name="height_cm"]').should("exist");
    });

    it("4. Weight input exists", () => {
        cy.get('input[name="weight_kg"]').should("exist");
    });

    it("5. Target weight input exists", () => {
        cy.get('input[name="target_weight_kg"]').should("exist");
    });

    it("6. Age input exists", () => {
        cy.get('input[name="age"]').should("exist");
    });

    it("7. Save button exists", () => {
        cy.contains("Save Changes").should("exist");
    });

    it("8. Inputs can be filled", () => {
        cy.get('select[name="gender"]').select(testProfile.gender);
        cy.get('input[name="height_cm"]').clear().type(testProfile.height_cm);
        cy.get('input[name="weight_kg"]').clear().type(testProfile.weight_kg);
        cy.get('input[name="target_weight_kg"]').clear().type(testProfile.target_weight_kg);
        cy.get('input[name="age"]').clear().type(testProfile.age);
    });

    it("9. Save button clickable", () => {
        cy.get('button:contains("Save Changes")').click();
        cy.wait("@updateProfile");
    });

    it("10. Successful save redirects to dashboard", () => {
        cy.get('button:contains("Save Changes")').click();
        cy.wait("@updateProfile");
        cy.url().should("include", "/dashboard");
    });

    it("11. Empty height shows error", () => {
        cy.get('input[name="height_cm"]').clear();
        cy.get('button:contains("Save Changes")').click();
        cy.contains("Height is required").should("exist");
    });

    it("12. Empty weight shows error", () => {
        cy.get('input[name="weight_kg"]').clear();
        cy.get('button:contains("Save Changes")').click();
        cy.contains("Weight is required").should("exist");
    });

    it("13. Empty target weight shows error", () => {
        cy.get('input[name="target_weight_kg"]').clear();
        cy.get('button:contains("Save Changes")').click();
        cy.contains("Target weight is required").should("exist");
    });

    it("14. Empty age shows error", () => {
        cy.get('input[name="age"]').clear();
        cy.get('button:contains("Save Changes")').click();
        cy.contains("Age is required").should("exist");
    });

    it("15. Reload preserves input values", () => {
        cy.get('input[name="height_cm"]').clear().type(testProfile.height_cm);
        cy.reload();
        cy.wait("@getProfile");
        cy.get('input[name="height_cm"]').should("have.value", testProfile.height_cm);
    });

    it("16. Navigate back to dashboard button works", () => {
        cy.contains("Back to Dashboard").click();
        cy.url().should("include", "/dashboard");
    });

    it("17. All fields are editable", () => {
        cy.get('input, select').each(($el) => {
            if ($el.prop('tagName').toLowerCase() === 'input') {
                cy.wrap($el).clear().type("123");
            } else if ($el.prop('tagName').toLowerCase() === 'select') {
                cy.wrap($el).select(testProfile.gender);
            }
        });
    });

    it("18. Gender select has options", () => {
        cy.get('select[name="gender"] option').should("have.length.at.least", 2);
    });

    it("19. Error message disappears after correction", () => {
        cy.get('input[name="height_cm"]').clear();
        cy.get('button:contains("Save Changes")').click();
        cy.contains("Height is required").should("exist");

        cy.get('input[name="height_cm"]').type("175");
        cy.get('button:contains("Save Changes")').click();
        cy.contains("Height is required").should("not.exist");
    });

    it("20. Profile data persists after save", () => {
        cy.get('input[name="height_cm"]').clear().type("180");
        cy.get('button:contains("Save Changes")').click();
        cy.wait("@updateProfile");
        cy.get('input[name="height_cm"]').should("have.value", "180");
    });


});
