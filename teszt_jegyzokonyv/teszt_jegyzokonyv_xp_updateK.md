# HomePage XP Update Teszt Jegyzőkönyv  
**Készítette:** Kovács Kinga Kendra  
**Dátum:** 2025.11.29  
**Projekt:** AI Fitness Coach Frontend  

---

## 1. Teszt célja  

Ez a **frontend integration/component teszt** a `HomePage` komponens helyes működését ellenőrzi **React Testing Library + Jest** használatával.  
A teszt célja annak igazolása, hogy:  

- Az XP és Level értékek helyesen jelennek meg a felhasználó számára.  
- A backend API hívások (mockolt `fetch`) helyesen kezelődnek a komponensben.  
- A felhasználói tevékenységek (plan update) megfelelően frissítik az XP értékeket.  
- A teszt teljesen izoláltan fut, nem érinti az éles adatbázist.  

---

## 2. Tesztforgatókönyvek  

| **Teszt ID** | **Teszt neve**                             | **Cél** | **Bemenet / művelet** | **Várt eredmény** | **Tényleges eredmény** | **Státusz** |
|---------------|--------------------------------------------|---------|-----------------------|------------------|------------------------|-------------|
| TC01 | `HomePage renders correctly`               | Ellenőrizni, hogy a HomePage betöltődik | Render: `<HomePage />` MemoryRouter-rel | Komponens renderelve, statikus UI elemek láthatók | Komponens megjelenik a DOM-ban | Sikeres |
| TC02 | `Mock ThemeSwitcher displays`              | Ellenőrizni, hogy a ThemeSwitcher mock működik | Render: `<HomePage />` | `data-testid="theme-switcher-mock"` elem látható | Megjelenik a mock div | Sikeres |
| TC03 | `Mock GoalsComponent displays`             | Ellenőrizni, hogy a GoalsComponent mock működik | Render: `<HomePage />` | `data-testid="goals-mock"` elem látható | Megjelenik a mock div | Sikeres |
| TC04 | `Mock StatComponent displays XP and Level` | Ellenőrizni, hogy a StatComponent mock XP és Level értékeket mutat | Render: `<HomePage />` | `data-testid="stat-mock"` elem tartalmazza a Level és XP értékeket | Megjelenik a Level: 2 és XP: 50 | Sikeres |
| TC05 | `XP fetch from backend`                    | Ellenőrizni, hogy a mock backend XP értékek helyesen jelennek meg | Mock fetch `/api/xp/status` → `{ xp: 50, level: 2 }` | UI mutatja: "Level: 2", "XP: 50" | Megjelenik a helyes XP és Level | Sikeres |
| TC06 | `XP updates after plan change`             | Ellenőrizni, hogy a XP változik plan update után | Mock fetch `/api/xp/status` → `{ xp: 20, level: 1 }` | UI mutatja: "Level: 1", "XP: 20" | Megjelenik a frissített XP és Level | Sikeres |
| TC07 | `LocalStorage mock works`                  | Ellenőrizni, hogy a token kezelés mock működik | window.localStorage.getItem | Mock token visszaadva | "fake-token" érték visszaadva | Sikeres |

---

## 3. Technikai megjegyzések  

- Teszt keretrendszer: **React Testing Library + Jest**  
- Minden teszt **mockolt API válaszokkal** fut (`fetch` mockolt).  
- Minden külső komponens (`ThemeSwitcher`, `GoalsComponent`, `StatComponent`) mockolt.  
- Tesztek lefedik:  
  - HomePage komponens renderelését  
  - XP és Level értékek helyes megjelenését  
  - Plan update hatására történő XP frissítést  
  - LocalStorage kezelését  
- Tesztek izoláltan futnak, **nem módosítják az éles backend adatokat**  

---

## 4. Következtetés  

- A HomePage UI stabil, az XP és Level értékek helyesen jelennek meg mockolt adatokkal.  
- Mockolt backend API hívások helyesen kezelődnek.  
- A plan update szimulációja után az XP frissítés megfelelően jelenik meg a UI-n.  
- A teszt teljesen izolált, az éles adatbázist nem érinti.  
- A teszt lefedi a HomePage XP update fő funkcióját, a komponens stabilitását biztosítva.
