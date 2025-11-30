# Backend Utility & Auth Decorator Egységteszt Jegyzőkönyv
**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.28  
**Projekt:** Fitness / Goal Tracking Backend  

---

## 1. Teszt célja
Az egységtesztek célja a backend utility modulok és az auth_decorator működésének ellenőrzése izolált környezetben.  
Fő célok:

- A `mock_data.get_mock_plan` helyes adatstruktúrákat ad vissza a különböző plan típusokra.  
- A `score_utils.calculate_mock_score` a megfelelő pontszámot adja a plan típus alapján.  
- A `token_blacklist` modul helyesen kezeli a tokenek blacklist-re tételét és ellenőrzését.  
- A `auth_decorator.token_required` helyesen ellenőrzi:
  - hiányzó tokeneket  
  - érvénytelen vagy lejárt tokeneket  
  - blacklisted tokeneket  
  - nem létező felhasználó esetét  
  - sikeres hozzáférést  
- Minden teszt egy külön tesztadatbázist használ, így az éles adatbázist nem érinti.

---

## 2. Tesztforgatókönyvek

| Teszt ID | Teszt neve | Modul | Cél | Bemenet / művelet | Várt eredmény | Tényleges eredmény | Státusz |
|----------|------------|-------|-----|-----------------|---------------|------------------|---------|
| TC01 | test_get_mock_plan_workout | mock_data | Workout plan lekérdezés | get_mock_plan("workout") | 7 napos edzésterv, "Push-ups" első napon | 7 napos edzésterv, "Push-ups" első napon | Sikeres |
| TC02 | test_get_mock_plan_diet | mock_data | Diet plan lekérdezés | get_mock_plan("diet") | 7 napos étkezési terv, első nap reggeli "Oatmeal + Banana" | 7 napos étkezési terv, első nap reggeli "Oatmeal + Banana" | Sikeres |
| TC03 | test_get_mock_plan_generic | mock_data | Ismeretlen plan típus | get_mock_plan("unknown_type") | Generic Fitness Plan visszaadása | Generic Fitness Plan visszaadása | Sikeres |
| TC04 | test_calculate_mock_score_workout | score_utils | Workout pontszám | calculate_mock_score("workout") | 80 | 80 | Sikeres |
| TC05 | test_calculate_mock_score_diet | score_utils | Diet pontszám | calculate_mock_score("diet") | 90 | 90 | Sikeres |
| TC06 | test_calculate_mock_score_other | score_utils | Ismeretlen plan pontszám | calculate_mock_score("other") | 70 | 70 | Sikeres |
| TC07 | test_add_token_to_blacklist_true | token_blacklist | Token hozzáadása blacklist-re | add_token_to_blacklist("mocktoken") | True, token adatbázisban | True, token adatbázisban | Sikeres |
| TC08 | test_add_token_to_blacklist_false | token_blacklist | Null token hozzáadás | add_token_to_blacklist(None) | False | False | Sikeres |
| TC09 | test_is_token_blacklisted | token_blacklist | Token ellenőrzés | add_token_to_blacklist("checktoken"), majd is_token_blacklisted("checktoken") és ("notoken") | True / False | True / False | Sikeres |
| TC10 | test_token_missing | auth_decorator | Hiányzó token | GET /protected, nincs Authorization header | 401, "Token is missing" | 401, "Token is missing" | Sikeres |
| TC11 | test_token_blacklisted | auth_decorator | Blacklisted token | GET /protected, blacklisted token | 401, "Token has been revoked" | 401, "Token has been revoked" | Sikeres |
| TC12 | test_token_invalid | auth_decorator | Érvénytelen token | GET /protected, decode_auth_token None | 401, "Token is invalid or expired" | 401, "Token is invalid or expired" | Sikeres |
| TC13 | test_user_not_found | auth_decorator | Nem létező felhasználó | GET /protected, token valid de user nem létezik | 404, "User not found" | 404, "User not found" | Sikeres |
| TC14 | test_successful_access | auth_decorator | Sikeres hozzáférés | GET /protected, token valid, user létezik | 200, "Hello {username}" | 200, "Hello testuser" | Sikeres |

---

## 3. Technikai megjegyzések
- A tesztek **pytest** keretrendszerrel futnak Flask alkalmazáskörnyezetben.  
- Minden token_blacklist és auth_decorator teszt egy külön PostgreSQL tesztadatbázist használ.  
- A `mock_data` és `score_utils` modul tesztjei teljesen izoláltak, nem érintik az adatbázist.  
- A `monkeypatch` használata lehetővé teszi a token dekódolás és blacklist viselkedés szimulálását.

---

## 4. Következtetés
- Az összes utility modul és auth decorator teljes körűen tesztelve van, beleértve a sikeres és hibás eseteket is.  
- A mock planok, score számítások és token kezelés helyesek.  
- A tesztek izolált környezetben futnak, így az éles adatbázis biztonságban van.  
- A coverage lefedi az összes fő logikai útvonalat a utility modulokban és auth decoratorban.
