# ProfilePage Automated UI Teszt Jegyzőkönyv  
**Készítette:** Kovács Kinga Kendra  
**Dátum:** 2025.11.28  
**Projekt:** Fitness / Goal Tracking Frontend  

---

## 1. Teszt célja  

Az automatizált UI tesztek célja a ProfilePage helyes működésének ellenőrzése **Cypress használatával**.  
A tesztek fő célja annak igazolása, hogy:  

- A felhasználói profil adatok helyesen jelennek meg a UI-n.  
- Az űrlapmezők (gender, height, weight, target weight, age) interaktívak és módosíthatók.  
- A mentés gomb működik és a profil adatok frissíthetők.  
- Hibakezelés megfelelően jelenik meg üres mezők esetén.  
- Az API hívások (GET/PUT) mockolt válaszokkal helyesen működnek.  
- A módosítások után az adatok a UI-n és a backend válaszok alapján megmaradnak.  

---

## 2. Tesztforgatókönyvek  

| **Teszt ID** | **Teszt neve**                      | **Cél** | **Bemenet / művelet** | **Várt eredmény** | **Tényleges eredmény** | **Státusz** |
|---------------|-------------------------------------|----------|------------------------|--------------------|------------------------|---------|
| TC01 | `Profile page loads`               | Ellenőrizni, hogy a profil oldal betöltődik. | Látogatás: `/profile`. | "Your Profile" felirat látható. | Megjelenik a felirat. | Sikeres |
| TC02 | `Gender select exists`             | A gender select elem létezik. | Elem lekérdezés: `select[name="gender"]` | Létezik a select mező. | Létezik. | Sikeres |
| TC03 | `Height input exists`              | Magasság mező létezik. | Elem lekérdezés: `input[name="height_cm"]` | Létezik a mező. | Létezik. | Sikeres |
| TC04 | `Weight input exists`              | Súly mező létezik. | Elem lekérdezés: `input[name="weight_kg"]` | Létezik a mező. | Létezik. | Sikeres |
| TC05 | `Target weight input exists`       | Cél súly mező létezik. | Elem lekérdezés: `input[name="target_weight_kg"]` | Létezik a mező. | Létezik. | Sikeres |
| TC06 | `Age input exists`                 | Életkor mező létezik. | Elem lekérdezés: `input[name="age"]` | Létezik a mező. | Létezik. | Sikeres |
| TC07 | `Save button exists`               | Mentés gomb létezik. | Elem lekérdezés: `button:contains("Save Changes")` | Gomb látható. | Látható. | Sikeres |
| TC08 | `Inputs can be filled`             | A mezők kitölthetők. | Kitöltés: gender, height, weight, target weight, age | Mezők kitöltve a várt értékekkel. | Mezők kitöltve. | Sikeres |
| TC09 | `Save button clickable`            | Mentés gomb működik. | Kattintás a mentés gombra | PUT API hívás sikeres. | Sikeres PUT hívás. | Sikeres |
| TC10 | `Successful save redirects to dashboard` | Mentés után a dashboardra irányít | Kattintás a mentés gombra | URL tartalmazza: `/dashboard` | URL helyes. | Sikeres |
| TC11 | `Empty height shows error`         | Üres magasság mező hibát ad | Magasság mező törlése, mentés | "Height is required" hiba üzenet | Megjelenik a hiba | Sikeres |
| TC12 | `Empty weight shows error`         | Üres súly mező hibát ad | Súly mező törlése, mentés | "Weight is required" hiba üzenet | Megjelenik a hiba | Sikeres |
| TC13 | `Empty target weight shows error`  | Üres cél súly mező hibát ad | Cél súly törlése, mentés | "Target weight is required" hiba | Megjelenik a hiba | Sikeres |
| TC14 | `Empty age shows error`            | Üres életkor mező hibát ad | Életkor mező törlése, mentés | "Age is required" hiba | Megjelenik a hiba | Sikeres |
| TC15 | `Reload preserves input values`    | Újratöltés után az adatok megmaradnak | Input kitöltés, oldal újratöltése | Mezők értékei megmaradnak | Megmaradnak | Sikeres |
| TC16 | `Navigate back to dashboard button works` | Vissza a dashboardra működik | Kattintás: "Back to Dashboard" | URL tartalmazza `/dashboard` | URL helyes | Sikeres |
| TC17 | `All fields are editable`          | Minden mező szerkeszthető | Input és select mezők módosítása | Mezők értékei változtathatók | Sikeres | Sikeres |
| TC18 | `Gender select has options`        | Gender mező legalább 2 opcióval rendelkezik | Lekérdezés: select options | Legalább 2 opció | Megfelel | Sikeres |
| TC19 | `Error message disappears after correction` | Hibajelzés eltűnik javítás után | Üres mező → hiba → mező kitöltése → mentés | Hiba eltűnik | Hiba eltűnik | Sikeres |
| TC20 | `Profile data persists after save` | Mentett adatok megmaradnak | Mezők kitöltése, mentés, ellenőrzés | Inputok értéke a mentett adatokkal egyezik | Megfelel | Sikeres |

---

## 3. Technikai megjegyzések  

- Teszt keretrendszer: **Cypress**  
- Minden teszt **mockolt API válaszokkal** fut (`GET /users/profile`, `PUT /users/profile`)  
- A tesztek lefedik:  
  - Profil oldal betöltését  
  - Input mezők létezését és szerkeszthetőségét  
  - Hibakezelést üres mezők esetén  
  - Mentés gomb működését és a redirect logikát  
  - Input értékek megmaradását újratöltés után  
- Tesztek izoláltan futnak, nem módosítják az éles backend adatokat  

---

## 4. Következtetés  

- A ProfilePage UI stabil és az összes mező megfelelően működik.  
- Hibakezelés és validációk a vártnak megfelelően jelennek meg.  
- A mentés és az adatok megőrzése sikeresen működik mockolt API hívásokkal.  
- A Cypress automatizált UI teszt sikeresen lefedi a teljes profil oldalt.
