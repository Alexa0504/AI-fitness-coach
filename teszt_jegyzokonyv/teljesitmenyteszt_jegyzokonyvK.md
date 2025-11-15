# Backend API Teljesítményteszt Jegyzőkönyv

**Készítette:** Kovács Kinga-Kendra  
**Dátum:** 2025.11.05  
**Projekt:** Fitness / Goal Tracking Backend

---

## 1. Teszt célja

A teljesítménytesztek célja annak vizsgálata, hogy a backend API végpontjai terhelés alatt is elfogadható válaszidővel működjenek.  
A teszt **nem érinti** a frontend UI-t, sem külső API-kat (Gemini, Nutritionix).  
A tesztek **lokálisan, in-memory SQLite adatbázissal** futnak, így a valós adatbázis nincs érintve.

**Célok:**

- Ellenőrizni, hogy a legkritikusabb végpontok válaszideje meghatározott küszöbértéken belül marad.
- Szimulálni reális adatmennyiséget (pl. ~300 Goal rekord).
- Bizonyítani, hogy a rendszer kis terhelés mellett stabil és gyors.

---

## 2. Tesztkörnyezet

| Összetevő        | Leírás |
|------------------|--------|
| Keretrendszer     | Flask (Python) |
| Teszt futtató     | pytest |
| Adatbázis         | SQLite `:memory:` (izolált) |
| API hitelesítés   | Bearer Token |
| Tesztelt végpontok| `/api/auth/login`, `/api/goals/`, `/api/plans/` |

---

## 3. Tesztforgatókönyvek

| Teszt ID | Teszt neve | Cél | Bemenet / Művelet | Teljesítményküszöb | Tényleges eredmény | Státusz |
|---------|------------|-----|------------------|-------------------|-------------------|---------|
| PT01 | test_auth_login_performance | Bejelentkezési végpont válaszideje | `POST /api/auth/login` (érvényes adatok) | < 0.5 s | 0.12–0.23 s | Sikeres |
| PT02 | test_goals_list_performance | Nagy mennyiségű adat lekérése | `GET /api/goals/` (~300 rekord) | < 0.7 s | 0.25–0.48 s | Sikeres |
| PT03 | test_plan_creation_performance | Plan létrehozás válaszideje (mock AI) | `POST /api/plans/`, `plan_type="workout"` | < 0.8 s | 0.30–0.60 s | Sikeres |

---

## 4. Technikai megjegyzések

- A tesztek **nem kapcsolódnak az éles adatbázishoz** — az `sqlite:///:memory:` garantálja az izoláltságot.
- Minden futtatás előtt tiszta adatbázis-séma épül, így nincs adatmaradvány.
- A Goal lekérési teszt ~300 rekordot tölt fel, így reálisabb környezetet modellez.
- A Plan létrehozási teszt **mockolt AI generálással** fut, nem használ külső API hívást.

---

## 5. Következtetés

- A backend API végpontjai meghatározott terhelés mellett **stabilan és gyorsan működnek**.
- A válaszidők **minden esetben a kitűzött limit alatt maradtak**.
- A rendszer teljesítménye API szinten megfelelő;  
  a **frontend + valós adatbázis** teljesítményes tesztelése később ajánlott.

---
