# Frontend Automated UI Test Report

**Author:** Zilahi Alexandra  
**Date:** 2025.11.26  
**Project:** AI Fitness Coach Frontend

---

## T04: Frontend: NextGoalsTips Static Content Verification (Self-Care Checklist)

**Modul:** StatsComponent.tsx / NextGoalsTips

| Test ID | Test Name | Module | Purpose | Input / Action | Expected Result | Actual Result | Status |
|---------|---------------------------------------------------------------|------------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|--------|
| T04.1 | Test: Component container exists | Structural | Ellenőrzi, hogy a fő konténer létezik-e. | DOM keresés: `#next-goals-tips` | Elem létezik | Elem létezik | Passed |
| T04.2 | Test: Component contains the exact number of tips | Content | Ellenőrzi a tippek pontos számát. | Tipp elemek száma a konténerben. | Pontosan 5 tipp elemet tartalmaz | Pontosan 5 tipp elemet tartalmaz | Passed |
| T04.3 | Test: First tip text is correct | Content | Ellenőrzi az első tipp szövegének helyességét. | Első tipp szövege egyezik a mock tartalommal. | Szöveg egyezik a mock tartalommal | Szöveg egyezik a mock tartalommal | Passed |
| T04.4 | Test: Last tip text is correct | Content | Ellenőrzi az utolsó tipp szövegének helyességét. | Utolsó tipp szövege egyezik a mock tartalommal. | Szöveg egyezik a mock tartalommal | Szöveg egyezik a mock tartalommal | Passed |
| T04.5 | Test: All tips are visible on the page | Structural | Ellenőrzi, hogy minden tipp látható-e. | Láthatósági ellenőrzés minden tipp elemen. | Minden tipp látható (`display: none` hiánya) | Minden tipp látható (`display: none` hiánya) | Passed |
| T04.6 | Test: No tip element contains empty text | Content | Ellenőrzi, hogy egyetlen tipp sem üres. | Minden tipp szövegének hossza > 0. | Egyik tipp szövege sem üres | Egyik tipp szövege sem üres | Passed |
| T04.7 | Test: Total tips count equals mock length (5) | Content | Ellenőrzi a tippek számát a forrás (mock) hosszához képest. | Tipp elemek száma egyenlő a mock tömb hosszával (5). | Elemek száma = 5 | Elemek száma = 5 | Passed |
| T04.8 | Test: Tip content matches array indices | Content | Ellenőrzi, hogy a tartalom egyezik-e a mock tömb indexeivel. | Tipp szövegek egyeznek a mock tömb elemeivel. | Minden szöveg egyezik az indexszel | Minden szöveg egyezik az indexszel | Passed |
| T04.9 | Test: Tip text data type is confirmed as a string | Content | Ellenőrzi a tipp szöveg adattípusát. | Minden tipp szöveg adattípusa String. | Adattípus String | Adattípus String | Passed |
| T04.10 | Test: The overall component container is not empty | Structural | Ellenőrzi, hogy a fő konténer tartalmaz-e tartalmat. | Konténer belső HTML hossza > 0. | Konténer nem üres | Konténer nem üres | Passed |
| T04.11 | Test: First tip element is confirmed to be visible | Structural | Ellenőrzi az első tipp láthatóságát. | Láthatósági ellenőrzés (pl. `offsetHeight > 0`). | Első tipp látható | Első tipp látható | Passed |
| T04.12 | Test: Last tip element is confirmed to be visible | Structural | Ellenőrzi az utolsó tipp láthatóságát. | Láthatósági ellenőrzés (pl. `offsetHeight > 0`). | Utolsó tipp látható | Utolsó tipp látható | Passed |
| T04.13 | Test: Tip count remains correct after simulated DOM content replacement | Structural | Ellenőrzi a számot a tartalom frissítése után. | DOM tartalom cseréje utáni elemek száma. | Tippek száma továbbra is 5 | Tippek száma továbbra is 5 | Passed |
| T04.14 | Test: Each tip contains text | Content | Ellenőrzi, hogy minden tipp tartalmaz szöveget. | Minden tipp szövegének hossza > 0. | Minden tipp tartalmaz szöveget | Minden tipp tartalmaz szöveget | Passed |
| T04.15 | Test: Tip list parent container exists | Structural | Ellenőrzi a lista szülőelemének meglétét. | DOM keresés a lista szülőkonténerére. | Szülő konténer létezik | Szülő konténer létezik | Passed |
| T04.16 | Test: Tip count matches the expected number (5) | Content | Megerősíti a tippek számát. (Duplikált ellenőrzés) | Elemek száma megegyezik 5-tel. | Elemek száma megegyezik 5-tel | Elemek száma megegyezik 5-tel | Passed |
| T04.17 | Test: Every tip element's text perfectly matches the mock content | Content | Ellenőrzi az összes tipp szövegének pontos egyezését. | Összes tipp szövege egyezik a mock tömb elemeivel. | Minden szöveg pontosan egyezik | Minden szöveg pontosan egyezik | Passed |
| T04.18 | Test: Every tip is visible after simulated DOM content replacement | Structural | Ellenőrzi a láthatóságot tartalomcsere után. | Láthatósági ellenőrzés a csere után. | Minden tipp látható maradt | Minden tipp látható maradt | Passed |
| T04.19 | Test: Tip text is confirmed to be non-empty | Content | Megerősíti a tipp szövegének nem-üres voltát. (Duplikált ellenőrzés) | Minden tipp szövegének hossza > 0. | Szöveg nem üres | Szöveg nem üres | Passed |
| T04.20 | Test: Component content exists after a page reload simulation | Structural | Ellenőrzi a tartalom megmaradását újratöltés szimulációja után. | Konténer létezik és nem üres újratöltés után. | Komponens tartalma létezik és nem üres | Komponens tartalma létezik és nem üres | Passed |

---