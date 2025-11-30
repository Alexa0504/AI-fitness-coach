# Backend Adatbázis Egységteszt Jegyzőkönyv  
**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.28  
**Projekt:** Fitness / Goal Tracking Backend  

---

## 1. Teszt célja  

Az egységtesztek célja az adatbázis-modellek és a seedelési logika helyes működésének ellenőrzése **biztonságos, külön teszt PostgreSQL adatbázisban**.  
A tesztek fő célja annak igazolása, hogy:

- A `User`, `Goal`, `Plan`, `UserGoal`, `Tip` és `TokenBlacklist` modellek létrehozhatók, lekérdezhetők és helyesen működnek.  
- A `User` és `Goal` / `Plan` kapcsolatok megfelelően működnek.  
- A `seed_data()` függvény megfelelően tölti fel a tesztadatokat.  
- A tesztek **külön tesztadatbázist** használnak, így az éles adatbázist nem érintik.  

---

## 2. Tesztforgatókönyvek  

| **Teszt ID** | **Teszt neve**                      | **Cél** | **Bemenet / művelet** | **Várt eredmény** | **Tényleges eredmény** | **Státusz** |
|---------------|-------------------------------------|----------|------------------------|--------------------|------------------------|---------|
| TC01 | `test_create_user_in_mock_db`       | Ellenőrizni, hogy a `User` rekord létrehozható és lekérdezhető a tesztadatbázisban. | Létrehozás: `User(username="mockuser", email="mock@example.com")`. | A felhasználó elmentve, helyes e-mail címmel lekérdezhető. | A várt eredmény szerint. | Sikeres |
| TC02 | `test_goal_and_plan_relations`      | A `User`, `Goal` és `Plan` közötti kapcsolat tesztelése. | Létrehozás: egy felhasználó, egy cél, egy terv. | A felhasználóhoz 1 cél és 1 terv tartozik. | A várt eredmény szerint. | Sikeres |
| TC03 | `test_token_blacklist_entry`        | A `TokenBlacklist` tábla működésének ellenőrzése. | Token hozzáadása: `"abc123"`. | A token lekérdezhető a DB-ből. | A várt eredmény szerint. | Sikeres |
| TC04 | `test_progress_state_json`          | Ellenőrizni, hogy a `User` progress_state mező JSON-ként tárolható és lekérdezhető. | `user.set_progress_state({"steps": 1000})` | Lekérdezve a felhasználó JSON állapota egyezik a beállítottal. | A várt eredmény szerint. | Sikeres |
| TC05 | `test_user_goal_creation`           | `UserGoal` létrehozás és lekérdezés. | Létrehozás: `UserGoal(user_id=user.id, goal_name="Run 5km")` | A rekord elmentve és helyesen lekérdezhető. | A várt eredmény szerint. | Sikeres |
| TC06 | `test_tip_creation`                 | `Tip` létrehozás és lekérdezés. | Létrehozás: `Tip(category="nutrition", text="Drink water")` | A rekord elmentve és helyesen lekérdezhető. | A várt eredmény szerint. | Sikeres |
| TC07 | `test_to_dict_methods`              | Ellenőrizni, hogy minden modell `to_dict` metódusa működik. | Létrehozás: `User`, `Goal`, `Plan`, `TokenBlacklist` | Mindegyik objektum `to_dict()` metódusa dict típust ad vissza, TokenBlacklist `__repr__` string | A várt eredmény szerint. | Sikeres |
| TC08 | `test_seed_data_works_with_mock_db` | A `seed_data()` függvény helyes működésének ellenőrzése. | `seed_data(app)` futtatása a tesztadatbázison. | Legalább 3 felhasználó, 3 cél és 2 terv található. | A várt eredmény szerint. | Sikeres |


---

## 3. Technikai megjegyzések  

- A tesztek **pytest** keretrendszerrel futnak, **Flask alkalmazáskörnyezetben**.  
- Az adatbázis típusa: PostgreSQL tesztadatbázis (`postgresql://<fitness_db_test>`), így az éles adatbázis teljesen érintetlen marad.  
- Minden teszt **izolált tranzakcióban** fut, és a végén **rollback** történik, így az adatok nem maradnak meg.  
- A tesztek lefedik:  
  - CRUD műveleteket a `User`, `Goal`, `Plan`, `UserGoal`, `Tip`, `TokenBlacklist` modelleken  
  - JSON és `to_dict()` konverziókat  
  - Kapcsolati logikát `User` ↔ `Goal`/`Plan`  
  - Seed adat feltöltés és ellenőrzés  

---

## 4. Következtetés  

- Az adatbázis-réteg stabil és a vártnak megfelelően működik PostgreSQL tesztadatbázisban.  
- A `User`, `Goal`, `Plan`, `UserGoal`, `Tip`, `TokenBlacklist` entitások közötti kapcsolatok helyesek.  
- A `seed_data()` biztonságosan fut és a tesztadatbázisban megfelelő mennyiségű adatot generál.  
- A tesztek teljesen izolált környezetben futnak, az éles adatbázis érintetlen.  
- A modellek `to_dict()` metódusai és JSON mezői helyesen működnek.  

---
