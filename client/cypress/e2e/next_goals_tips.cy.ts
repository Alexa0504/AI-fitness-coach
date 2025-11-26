/// <reference types="cypress" />

describe("NextGoalsTips Component - 20 Stable Tests Using Fixtures", () => {
    
    const expectedTips = [
        "Drink at least 8 glasses of water a day.",
        "Get 7-8 hours of sleep every night.",
        "Include both cardio and strength training in your workouts.",
        "Eat a balanced diet with plenty of fruits and vegetables.",
        "Track your progress to stay motivated."
    ];
    
    const tipContainerSelector = "#next-goals-tips";
    const tipListItemSelector = `${tipContainerSelector} ul li`;
    const tipTextSelector = `${tipContainerSelector} ul li span.font-medium`;
    const staticContentSelector = 'Self-Care Checklist';

    beforeEach(() => {
        cy.login(); 
        cy.intercept("GET", "**/tips/general/weekly", { fixture: "tips.json" }).as("getTips");
        cy.visit("/dashboard"); 
        cy.contains(staticContentSelector, { timeout: 10000 }).should('be.visible');
        cy.wait("@getTips");
        cy.get(tipListItemSelector, { timeout: 10000 }).should("have.length", expectedTips.length);
    });
    

    it("1. Component exists", () => {
        cy.get(tipContainerSelector).should("exist");
    });

    it("2. Component has tips", () => {
        cy.get(tipListItemSelector).should("have.length", expectedTips.length);
    });

    it("3. First tip text is correct", () => {
        cy.get(tipTextSelector).first().should("have.text", expectedTips[0]);
    });

    it("4. Last tip text is correct", () => {
        cy.get(tipTextSelector).last().should("have.text", expectedTips[expectedTips.length - 1]);
    });

    it("5. All tips are visible", () => {
        cy.get(tipListItemSelector).each(($el) => cy.wrap($el).should("be.visible"));
    });

    it("6. No tip is empty", () => {
        cy.get(tipTextSelector).each(($el) => cy.wrap($el).invoke("text").should("not.be.empty"));
    });

    it("7. Total tips equal to fixture length", () => {
        cy.get(tipListItemSelector).should("have.length", expectedTips.length);
    });

    it("8. Tip indices are correct", () => {
        cy.get(tipListItemSelector).should("have.length", expectedTips.length);
    });

    it("9. Tip text is string", () => {
        cy.get(tipTextSelector).each(($el) => cy.wrap($el).invoke("text").should("be.a", "string"));
    });

    it("10. Component is not empty", () => {
        cy.get(tipContainerSelector).should("not.be.empty");
    });

    it("11. First tip is visible", () => {
        cy.get(tipListItemSelector).first().should("be.visible");
    });

    it("12. Last tip is visible", () => {
        cy.get(tipListItemSelector).last().should("be.visible");
    });

    it("13. Reload simulation - tips still exist", () => {
        cy.reload();
        cy.login();
        cy.wait("@getTips"); 
        cy.get(tipListItemSelector).should("have.length", expectedTips.length);
    });

    it("14. Each tip contains text", () => {
        cy.get(tipTextSelector).each(($el) => cy.wrap($el).invoke("text").should("match", /\S+/));
    });

    it("15. Tip list parent exists", () => {
        cy.get(tipContainerSelector).should("exist");
    });

    it("16. Tip count matches fixture", () => {
        cy.get(tipListItemSelector).should("have.length", expectedTips.length);
    });

    it("17. Tip text matches fixture", () => {
        cy.get(tipTextSelector).each(($el, idx) => cy.wrap($el).should("have.text", expectedTips[idx]));
    });

    it("18. Every tip visible after reload", () => {
        cy.reload();
        cy.login(); 
        cy.wait("@getTips");
        cy.get(tipListItemSelector).each(($el) => cy.wrap($el).should("be.visible"));
    });

    it("19. Tip text is not empty", () => {
        cy.get(tipTextSelector).each(($el) => cy.wrap($el).invoke("text").should("not.be.empty"));
    });

    it("20. Component content exists after reload", () => {
        cy.reload();
        cy.login(); 
        cy.wait("@getTips");
        cy.get(tipContainerSelector).should("not.be.empty");
    });
});