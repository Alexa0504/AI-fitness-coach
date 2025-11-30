# Backend Végpont Egységteszt Jegyzőkönyv
**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.28  
**Projekt:** Fitness / Goal Tracking Backend  

---

## 1. Teszt célja
Az egységtesztek célja a backend végpontok (auth, goals, plans) működésének ellenőrzése izolált környezetben.  
A tesztek fő célja annak igazolása, hogy:

- A felhasználói regisztráció, bejelentkezés és kijelentkezés (auth) megfelelően működik, és a token kezelés helyes.  
- A Goal és Plan entitások létrehozása, lekérése, frissítése és törlése helyesen történik.  
- A hibakezelés (pl. hiányzó mezők, duplikált adatok, nem létező rekordok, érvénytelen token) megfelelően reagál.  
- A tesztek nem érik el az éles adatbázist, minden művelet izolált és rollback történik.

---

## 2. Tesztforgatókönyvek

| Teszt ID | Teszt neve | Cél | Bemenet / művelet | Várt eredmény | Tényleges eredmény | Státusz |
|----------|------------|-----|-----------------|---------------|------------------|---------|
| TC01     | test_register_user_success | Felhasználó regisztráció | POST /api/auth/register, érvényes adatok | 201, token és user objektum visszaadva | 201, token és user objektum visszaadva | Sikeres |
| TC02     | test_register_missing_fields | Hiányzó mezők kezelése regisztrációnál | POST /api/auth/register, üres JSON | 400, hibaüzenet | 400, hibaüzenet | Sikeres |
| TC03     | test_register_duplicate_email | Duplikált email kezelése | Két regisztráció ugyanazzal az emaillel | 409, hibaüzenet | 409, hibaüzenet | Sikeres |
| TC04     | test_register_db_commit_exception | DB commit hiba kezelése | DB commit kivétel generálása | 500, internal error üzenet | 500, internal error üzenet | Sikeres |
| TC05     | test_login_success | Sikeres bejelentkezés | POST /api/auth/login, helyes adatok | 200, token visszaadva | 200, token visszaadva | Sikeres |
| TC06     | test_login_invalid_credentials | Hibás bejelentkezés | POST /api/auth/login, rossz adatok | 401, hibaüzenet | 401, hibaüzenet | Sikeres |
| TC07     | test_login_missing_password | Hiányzó jelszó | POST /api/auth/login, hiányzó jelszó | 400, hibaüzenet | 400, hibaüzenet | Sikeres |
| TC08     | test_login_with_username | Bejelentkezés felhasználónévvel | POST /api/auth/login, username | 200, token visszaadva | 200, token visszaadva | Sikeres |
| TC09     | test_logout_success | Sikeres kijelentkezés | POST /api/auth/logout, érvényes token | 200, sikerüzenet | 200, sikerüzenet | Sikeres |
| TC10     | test_logout_missing_token | Kijelentkezés token nélkül | POST /api/auth/logout | 401, hibaüzenet | 401, hibaüzenet | Sikeres |
| TC11     | test_logout_blacklist_failure | Kijelentkezés blacklist hiba esetén | POST /api/auth/logout, token blacklist hibával | 500, hibaüzenet | 500, hibaüzenet | Sikeres |
| TC12     | test_create_goal_success | Goal létrehozása | POST /api/goals/, érvényes adatok | 201, goal objektum | 201, goal objektum | Sikeres |
| TC13     | test_create_goal_missing_field | Hiányzó mező a goal létrehozásánál | POST /api/goals/, üres JSON | 400, hibaüzenet | 400, hibaüzenet | Sikeres |
| TC14     | test_get_goals | Goal lekérése | GET /api/goals/ | 200, lista | 200, lista | Sikeres |
| TC15     | test_update_goal_success | Goal frissítése | PUT /api/goals/{id}, érvényes adatok | 200, frissített goal | 200, frissített goal | Sikeres |
| TC16     | test_update_goal_not_found | Goal frissítése nem létező ID-val | PUT /api/goals/9999 | 404, hibaüzenet | 404, hibaüzenet | Sikeres |
| TC17     | test_delete_goal_success | Goal törlése | DELETE /api/goals/{id} | 200, sikerüzenet | 200, sikerüzenet | Sikeres |
| TC18     | test_delete_goal_not_found | Goal törlése nem létező ID-val | DELETE /api/goals/9999 | 404, hibaüzenet | 404, hibaüzenet | Sikeres |
| TC19     | test_access_without_token | Goal endpoint token nélkül | GET /api/goals/ | 401, hibaüzenet | 401, hibaüzenet | Sikeres |
| TC20     | test_access_with_invalid_token | Goal endpoint érvénytelen tokennel | GET /api/goals/, invalid token | 401, hibaüzenet | 401, hibaüzenet | Sikeres |
| TC21     | test_create_plan_success | Plan létrehozása | POST /api/plans/, érvényes adatok | 201, plan objektum | 201, plan objektum | Sikeres |
| TC22     | test_get_user_plans | Plan lekérése | GET /api/plans/ | 200, lista | 200, lista | Sikeres |
| TC23     | test_get_single_plan | Egyedi plan lekérése | GET /api/plans/{id} | 200, plan objektum | 200, plan objektum | Sikeres |
| TC24     | test_get_single_plan_not_found | Plan lekérése nem létező ID-val | GET /api/plans/999999 | 404, hibaüzenet | 404, hibaüzenet | Sikeres |
| TC25     | test_update_plan_success | Plan frissítése | PUT /api/plans/{id}, új content | 200, frissített plan | 200, frissített plan | Sikeres |
| TC26     | test_update_plan_not_found | Plan frissítése nem létező ID-val | PUT /api/plans/999999 | 404, hibaüzenet | 404, hibaüzenet | Sikeres |
| TC27     | test_delete_plan_success | Plan törlése | DELETE /api/plans/{id} | 200, sikerüzenet | 200, sikerüzenet | Sikeres |
| TC28     | test_delete_plan_not_found | Plan törlése nem létező ID-val | DELETE /api/plans/999999 | 404, hibaüzenet | 404, hibaüzenet | Sikeres |
| TC29     | test_create_weekly_goal_success | Heti cél létrehozása | POST /api/goals/weekly, érvényes adatok | 201, weekly goal objektum | 201, weekly goal objektum | Sikeres |
| TC30     | test_create_weekly_goal_missing_field | Hiányzó mező heti cél létrehozásánál | POST /api/goals/weekly, üres JSON | 400, hibaüzenet | 400, hibaüzenet | Sikeres |
| TC31     | test_get_weekly_goals | Heti célok lekérése | GET /api/goals/weekly | 200, lista | 200, lista | Sikeres |
| TC32     | test_toggle_weekly_goal | Heti cél állapot váltása (toggle) | PATCH /api/goals/weekly/{id}/toggle | 200, completed/pending státusz váltás | 200, completed/pending státusz váltás | Sikeres |
| TC33     | test_toggle_weekly_goal_not_found | Heti cél toggle nem létező ID-val | PATCH /api/goals/weekly/9999/toggle | 404, hibaüzenet | 404, hibaüzenet | Sikeres |
| TC34     | test_create_plan_invalid_start_date | Érvénytelen start_date | POST /api/plans/, start_date="2025-99-99" | 400, hibaüzenet | 400, "Invalid start_date format" | Sikeres |
| TC35     | test_update_plan_invalid_start_date | Érvénytelen start_date frissítésnél | PUT /api/plans/{id}, start_date="abcd" | 400, hibaüzenet | 400, "Invalid start_date format" | Sikeres |
| TC36     | test_update_plan_type_changes_score | Plan típus módosítás score változással | PUT /api/plans/{id}, plan_type="nutrition" | 200, score változik | 200, score változott | Sikeres |
---

## 3. Technikai megjegyzések
- A tesztek **pytest** keretrendszerrel futnak Flask alkalmazáskörnyezetben.  
- Minden teszt izolált tranzakcióban fut, rollback történik a végén, így az adatok nem maradnak meg.  
- A `auth_header` fixture biztosítja a felhasználóhoz tartozó tokeneket minden teszthez.
- A Goal és Plan tesztek biztosítják az összes CRUD művelet lefedettségét.

---

## 4. Következtetés
- A backend végpontok teljes körűen tesztelve vannak, beleértve a sikeres és hibás eseteket is.  
- Az auth, goal és plan endpointok megfelelően kezelik a hibákat, tokeneket és adatokat.  
- A tesztek izolált környezetben futnak, így garantált a valós adatbázis védelme.  
- A coverage a REST API főbb funkcióit lefedi, így a backend stabilitása biztosított.
