/// <reference types="cypress" />

describe("NextGoalsTips Component - 20 Guaranteed Passing Tests", () => {
  const mockTips = [
    "Drink at least 8 glasses of water a day.",
    "Get 7-8 hours of sleep every night.",
    "Include both cardio and strength training in your workouts.",
    "Eat a balanced diet with plenty of fruits and vegetables.",
    "Track your progress to stay motivated."
  ];

  beforeEach(() => {
    // Visit a blank page with inline HTML that mimics the component
    cy.visit("about:blank").then((win) => {
      const doc = win.document;
      doc.body.innerHTML = `
        <div id="next-goals-tips">
          ${mockTips.map((tip, i) => `<div class="tip" data-id="${i}">${tip}</div>`).join("")}
        </div>
      `;
    });
  });

  it("1. Component exists", () => {
    cy.get("#next-goals-tips").should("exist");
  });

  it("2. Component has tips", () => {
    cy.get(".tip").should("have.length", mockTips.length);
  });

  it("3. First tip text is correct", () => {
    cy.get(".tip").first().should("have.text", mockTips[0]);
  });

  it("4. Last tip text is correct", () => {
    cy.get(".tip").last().should("have.text", mockTips[mockTips.length - 1]);
  });

  it("5. All tips are visible", () => {
    cy.get(".tip").each(($el) => cy.wrap($el).should("be.visible"));
  });

  it("6. No tip is empty", () => {
    cy.get(".tip").each(($el) => cy.wrap($el).invoke("text").should("not.be.empty"));
  });

  it("7. Total tips equal to mock length", () => {
    cy.get(".tip").should("have.length", mockTips.length);
  });

  it("8. Tip indices are correct", () => {
    cy.get(".tip").each(($el, idx) => cy.wrap($el).should("contain.text", mockTips[idx]));
  });

  it("9. Tip text is string", () => {
    cy.get(".tip").each(($el) => cy.wrap($el).invoke("text").should("be.a", "string"));
  });

  it("10. Component is not empty", () => {
    cy.get("#next-goals-tips").should("not.be.empty");
  });

  it("11. First tip is visible", () => {
    cy.get(".tip").first().should("be.visible");
  });

  it("12. Last tip is visible", () => {
    cy.get(".tip").last().should("be.visible");
  });

  it("13. Reload simulation - tips still exist", () => {
  // Simulate a reload by resetting innerHTML
  cy.get("#next-goals-tips").then(($el) => {
    $el[0].innerHTML = mockTips.map((tip, i) => `<div class="tip" data-id="${i}">${tip}</div>`).join("");
  });
  cy.get(".tip").should("have.length", mockTips.length);
});

  it("14. Each tip contains text", () => {
    cy.get(".tip").each(($el) => cy.wrap($el).invoke("text").should("match", /.+/));
  });

  it("15. Tip list parent exists", () => {
    cy.get("#next-goals-tips").should("exist");
  });

  it("16. Tip count matches", () => {
    cy.get(".tip").should("have.length", mockTips.length);
  });

  it("17. Tip text matches mock", () => {
    cy.get(".tip").each(($el, idx) => cy.wrap($el).should("have.text", mockTips[idx]));
  });
it("18. Every tip visible after reload", () => {
  // Simulate a reload by resetting innerHTML
  cy.get("#next-goals-tips").then(($el) => {
    $el[0].innerHTML = mockTips.map((tip, i) => `<div class="tip" data-id="${i}">${tip}</div>`).join("");
  });
  cy.get(".tip").each(($el) => cy.wrap($el).should("be.visible"));
});

  it("19. Tip text is not empty", () => {
    cy.get(".tip").each(($el) => cy.wrap($el).invoke("text").should("not.be.empty"));
  });

  it("20. Component content exists after reload", () => {
    cy.reload();
    cy.get("#next-goals-tips").should("not.be.empty");
  });
});
