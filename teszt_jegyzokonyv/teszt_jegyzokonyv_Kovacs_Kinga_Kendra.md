# Backend Adatbázis Egységteszt Jegyzőkönyv  
**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.04  
**Projekt:** Fitness / Goal Tracking Backend  

---

## 1. Teszt célja  

Az egységtesztek célja az adatbázis-modellek és a seedelési logika helyes működésének ellenőrzése **biztonságos, memóriaalapú (mock)** környezetben.  
A tesztek fő célja annak igazolása, hogy:

- A `User`, `Goal`, `Plan` és `TokenBlacklist` modellek létrehozhatók, lekérdezhetők és helyesen működnek.  
- A `User` és `Goal` / `Plan` kapcsolatok megfelelően működnek.  
- A `seed_data()` függvény megfelelően tölti fel a tesztadatokat.  
- A tesztek soha nem érik el a valós (éles) adatbázist.  

---

## 2. Tesztforgatókönyvek  

| **Teszt ID** | **Teszt neve** | **Cél** | **Bemenet / művelet** | **Várt eredmény** | **Tényleges eredmény** | **Státusz** |
|---------------|----------------|----------|------------------------|--------------------|------------------------|---------|
| TC01 | `test_create_user_in_mock_db` | Ellenőrizni, hogy a `User` rekord létrehozható és lekérdezhető a tesztadatbázisban. | Létrehozás: `User(username="mockuser", email="mock@example.com")`. | A felhasználó elmentve, helyes e-mail címmel lekérdezhető. | A várt eredmény szerint. | Sikeres |
| TC02 | `test_goal_and_plan_relations` | A `User`, `Goal` és `Plan` közötti kapcsolat tesztelése. | Létrehozás: egy felhasználó, egy cél, egy terv. | A felhasználóhoz 1 cél és 1 terv tartozik. | A várt eredmény szerint. | Sikeres |
| TC03 | `test_token_blacklist_entry` | A `TokenBlacklist` tábla működésének ellenőrzése. | Token hozzáadása: `"abc123"`. | A token lekérdezhető a DB-ből. | A várt eredmény szerint. | Sikeres |
| TC04 | `test_seed_data_works_with_mock_db` | A `seed_data()` függvény helyes működésének ellenőrzése. | `seed_data(app)` futtatása a memóriaadatbázison. | Legalább 3 felhasználó, 3 cél és 2 terv található. | A várt eredmény szerint. | Sikeres |
| TC05 | `ensure_in_memory_db` | Biztonsági ellenőrzés, hogy a tesztek csak memóriaadatbázison futhassanak. | Ellenőrzés a DB URI-ra. | Hibaüzenet, ha nem `sqlite:///:memory:`. | Tesztelt, mock DB megerősítve. | Sikeres |

---

## 3. Technikai megjegyzések  

- A tesztek **pytest** keretrendszerrel futnak, **Flask alkalmazáskörnyezetben**.  
- Az adatbázis típusa: `sqlite:///:memory:` – minden teszt új, ideiglenes adatbázist hoz létre.  
- A `ensure_in_memory_db` fixture megakadályozza, hogy a tesztek az éles adatbázishoz csatlakozzanak.  
- Minden teszt **izolált tranzakcióban** fut, és a végén **rollback** történik, így az adatok nem maradnak meg.  

---


## 4. Következtetés  

 Az adatbázis-réteg stabil és a vártnak megfelelően működik.  
 A `User`, `Goal`, `Plan` entitások közötti kapcsolatok helyesek.  
 A `seed_data()` biztonságosan fut és a mock környezetben megfelelő mennyiségű adatot generál.  
 Az in-memory tesztkörnyezet garantálja a teljes adatbiztonságot.  


---
