# Backend Végpont Integrációs Teszt Jegyzőkönyv
**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.05  
**Projekt:** Fitness / Goal Tracking Backend  

---

## 1. Teszt célja
Az integrációs tesztek célja annak ellenőrzése, hogy a rendszer komponensei (adatbázis, modellek, végpontok, token alapú hitelesítés) megfelelően működnek együtt.  
A tesztek valós HTTP kéréseket szimulálnak a Flask `test_client()` használatával, azonban **in-memory SQLite adatbázist** alkalmaznak, így **nem érik el az éles adatokat**.

**Fő ellenőrzési pontok:**
- Regisztráció, bejelentkezés, kijelentkezés folyamata
- Token validáció és védett végpontok kezelése
- Goal és Plan entitások teljes CRUD művelete
- Helyes hibakezelés és státuszkódok visszaadása

---

## 2. Tesztforgatókönyvek

| Teszt ID | Teszt neve | Művelet | Várt eredmény | Tényleges eredmény | Státusz |
|----------|------------|---------|---------------|------------------|---------|
| IT01 | test_register_and_login | Regisztráció → Bejelentkezés | Token visszaadva mindkét lépésnél | Tokenek visszaadva | Sikeres |
| IT02 | test_logout_blacklist | Kijelentkezés érvényes tokennel | Token blacklistbe kerül | Blacklist működik | Sikeres |
| IT03 | test_create_get_update_delete_goal | Goal CRUD műveletek | Minden lépés megfelelő státuszkóddal fut | CRUD folyamat hibamentes | Sikeres |
| IT04 | test_create_get_update_delete_plan | Plan CRUD műveletek | Minden lépés megfelelő státuszkóddal fut | CRUD folyamat hibamentes | Sikeres |
| IT05 | test_protected_route_requires_token | Token nélküli elérés | 401: „Token is missing” | 401 hibaüzenet visszaadva | Sikeres |
| IT06 | test_create_get_toggle_weekly_goal | Weekly goal létrehozás és toggle | Goal létrejön, toggle változtatja az `is_completed` státuszt | Goal létrejött, toggle működik | Sikeres |

---

## 3. Technikai megjegyzések

- A tesztek **pytest** keretrendszerrel futnak.
- Az alkalmazás környezetet, adatbázist és teszt klienset fixture-ek hozzák létre (`app`, `client`, `auth_header`).
- Az adatbázis:
  - `sqlite:///:memory:`
  - automatikusan létrehozódik és törlődik minden tesztciklusban
- A token blacklisting funkció működése megerősítve lett.

---

## 4. Következtetés

Az integrációs tesztek alapján:

- A backend végpontok működése **teljes körűen stabil**.
- A hitelesítés és token kezelés **megbízható és biztonságos**.
- A Goal és Plan entitások CRUD folyamatai **hibamentesen működnek valós folyamatok közben is**.
- A tesztelés **nem érinti** az éles adatbázist, minden művelet **izolált** és automatikusan visszavonódik.



---
