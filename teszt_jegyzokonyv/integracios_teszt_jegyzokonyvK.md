# Backend Végpont Integrációs Teszt Jegyzőkönyv  
**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.28  
**Projekt:** Fitness / Goal Tracking Backend  

---

## 1. Teszt célja
Az integrációs tesztek célja annak ellenőrzése, hogy a rendszer komponensei (adatbázis, modellek, végpontok, token alapú hitelesítés) megfelelően működnek együtt.  
A tesztek valós HTTP kéréseket szimulálnak a Flask `test_client()` használatával, és **különálló PostgreSQL tesztadatbázist** használnak, így **nem érintik az éles adatokat**.

**Fő ellenőrzési pontok:**
- Regisztráció, bejelentkezés, kijelentkezés folyamata
- Token validáció és védett végpontok kezelése
- Goal és Plan entitások teljes CRUD művelete
- Weekly goal toggle funkció
- Helyes hibakezelés és státuszkódok visszaadása
- Felhasználói profil frissítése
- Teljes felhasználói workflow ellenőrzése

---

## 2. Tesztforgatókönyvek

| Teszt ID | Teszt neve | Művelet | Várt eredmény | Tényleges eredmény | Státusz |
|----------|------------|---------|---------------|------------------|---------|
| IT01 | test_register_and_login | Regisztráció → Bejelentkezés | Token visszaadva mindkét lépésnél | Tokenek visszaadva | Sikeres |
| IT02 | test_register_duplicate | Duplikált felhasználó regisztráció | 409 státuszkód | 409 státuszkód visszaadva | Sikeres |
| IT03 | test_login_invalid_credentials | Hibás e-mail/jelszó | 401 státuszkód | 401 státuszkód visszaadva | Sikeres |
| IT04 | test_logout_blacklist | Kijelentkezés érvényes tokennel | Token blacklistbe kerül | Blacklist működik | Sikeres |
| IT05 | test_create_get_update_delete_goal | Goal CRUD műveletek | Minden lépés megfelelő státuszkóddal fut | CRUD folyamat hibamentes | Sikeres |
| IT06 | test_create_get_toggle_weekly_goal | Weekly goal létrehozás és toggle | Goal létrejön, toggle változtatja az `is_completed` státuszt | Goal létrejött, toggle működik | Sikeres |
| IT07 | test_create_get_update_delete_plan | Plan CRUD műveletek | Minden lépés megfelelő státuszkóddal fut, plan `days` inicializálva | CRUD folyamat hibamentes | Sikeres |
| IT08 | test_toggle_plan_invalid_type | Érvénytelen toggle típus | 400 vagy 404 státuszkód | 400/404 státuszkód visszaadva | Sikeres |
| IT09 | test_update_user_profile_invalid_age | Hibás életkor megadása | 400 státuszkód | 400 státuszkód visszaadva | Sikeres |
| IT10 | test_update_user_profile_valid | Profiladatok frissítése | Módosítások sikeresen mentve | Profiladatok frissítve | Sikeres |
| IT11 | test_protected_route_requires_token | Token nélküli védett végpont | 401 státuszkód, „Token is missing” | 401 státuszkód visszaadva | Sikeres |
| IT12 | test_full_user_workflow | Teljes felhasználói workflow (regisztráció, goal, weekly goal, plan, profil, logout) | Minden művelet sikeresen lefut, token blacklistbe kerül | Workflow hibamentes | Sikeres |

---

## 3. Technikai megjegyzések

- A tesztek **pytest** keretrendszerrel futnak.
- Az alkalmazás környezetet, adatbázist és teszt klienset fixture-ek hozzák létre (`app`, `client`, `auth_header`, `seeded_user`, `seed_tips`).
- Az adatbázis:
  - PostgreSQL tesztadatbázis (különálló, izolált környezet)
  - A tesztadatok minden tesztfutás után törlődnek
- A token blacklisting funkció működése megerősítve lett.
- Plan entitásoknál a `content` mező **dict formátumban** van, így `json.loads()` használata **nem szükséges**.
- Weekly goal toggle teszt biztosítja az `is_completed` mező váltását True/False értékek között.

---

## 4. Következtetés

Az integrációs tesztek alapján:

- A backend végpontok működése **teljes körűen stabil**.
- A hitelesítés és token kezelés **megbízható és biztonságos**.
- A Goal és Plan entitások CRUD folyamatai **hibamentesen működnek valós folyamatok közben is**.
- Weekly goal toggle funkció és plan `days` inicializálás **helyesen kezelve**.
- Felhasználói profil frissítések megfelelően mentődnek.
- A teljes felhasználói workflow (regisztráció → goal → weekly goal → plan → profil → logout) **hibamentesen végrehajtható**.
- A tesztelés **nem érinti az éles adatbázist**, minden művelet **izolált** és automatikusan visszavonódik a tesztadatbázisban.
