














































































































































































































































































































































































































## Tesztterv (Minőségbiztosítás)

| Tesztelési Eljárás | Cél | Mérés / Validáció |
| :--- | :--- | :--- |
| **Unit Teszt** | A **Flask API** végpontok és az adatlogika stabilitása. | PyTest: API válaszok, adatlogika, CRUD műveletek a **PostgreSQL**-ben. |
| **Integrációs Teszt** | Kommunikáció: **Frontend ↔ Backend ↔ Gemini/Nutritionix**. | End-to-end (E2E) tesztelés: Adatok helyes átadása a **React** felületen a **Gemini**-nek és a terv helyes visszatérése. |
| **Kompatibilitási Teszt** | **Bootstrap** alapú felület reszponzivitása és böngészőkompatibilitás. | Ellenőrzés több böngészőben (Chrome, Firefox) és különböző képernyőméreteken a **Bootstrap** reszponzivitásának ellenőrzésére. |
| **Pontosság Teszt** | Az **AI-modell** által generált tervek és tanácsok szakmai hitelessége (**NF1**). | **Manuális Szakmai Validáció:** Szakemberrel vagy előre definiált forgatókönyvekkel történő ellenőrzés. |
| **Teljesítmény Teszt** | Az API válaszidő mérése terhelés alatt. | Terheléses teszt: Az egyidejű **Gemini API** hívások latenciájának mérése. |

### Tesztelési Folyamat Ábra

*Az ábra egy **körforgásos (iteratív) tesztelési modellt** ábrázol, amely megfelel a webalkalmazás agilis fejlesztésének.*

![Testing Process Flowchart](static/images/tesztelesi_folyamatabra.png)

## Adatbázis Terv (PostgreSQL)

Ez a fejezet az adatbázis szerkezetét részletezi, amelyet a **PostgreSQL** rendszerben valósítunk meg, az **SQLAlchemy ORM** segítségével.

### Főbb Táblák és ORM Modellek

| Tábla / ORM Modell | Fő Adatmezők | Kapcsolatok | Fókusz (Fitness Coach) |
| :--- | :--- | :--- | :--- |
| **users** | `id`, `username`, `password_hash`, `célok` (JSON), `súly`, `magasság` | `1:N` a `logs`-hoz és `plans`-hoz | Felhasználói profil adatok, a tervgenerálás alapja. |
| **plans** | `id`, `user_id` (FK), `típus` (edzés/étrend), `tartalom` (JSON/szöveg), `dátum`, `adaptáció_státusz` | `1:N` a `users`-től | Az AI (**Gemini**) által generált tervek tárolása. |
| **logs** | `id`, `user_id` (FK), `dátum`, `típus` (edzés/étkezés) | `1:N` a `users`-től | Minden felhasználói bejegyzés (naplózás). |
| **log_details** | `id`, `log_id` (FK), `kalória`, `makrók` (JSON), `gyakorlat`, `ismétlés`, `szett` | `1:N` a `logs`-tól | Részletes adatok a táplálkozásról (**Nutritionix**) és edzésről. |

## Telepítési és Karbantartási Terv

Ez a fejezet tartalmazza a rendszer tartós stabilitását és biztosítja a frissíthetőséget.

### Telepítési Terv (Szerver- és Kliensoldal)

A rendszer telepítése egy többkomponensű, háromszintű architektúrát igényel, amely magában foglalja az adatbázist, a Flask alapú szerveroldali logikát és a React alapú kliensoldali felületet.

**1. Szerveroldal és Adatbázis (Backend)**

* **Adatbázis Beállítás:** A **PostgreSQL** szerver telepítése az éles környezetben. Ezt követően a `fitness_db` adatbázis létrehozása és a sémák inicializálása migrációs eszközök (pl. Flask-Migrate) segítségével.
* **Flask Alkalmazás Beállítása:** A Python környezet előkészítése, a függőségek telepítése a `requirements.txt` fájl alapján.
* **Biztonsági Konfiguráció:** A külső szolgáltatásokhoz (Gemini, Nutritionix) szükséges **API kulcsok** környezeti változókként történő biztonságos beállítása az alkalmazás konfigurációs fájljában, a forráskódtól elkülönítve.
* **Futtatás:** Az éles környezeti szerver (pl. Gunicorn vagy uWSGI) konfigurálása és a Flask alkalmazás indítása, reverse proxy használatával az HTTPS forgalom kezelésére.

**2. Kliensoldal (Frontend)**

* **Build Folyamat:** A React forráskódjának kompilálása éles (production) módra, ami optimalizált, statikus fájlokat eredményez (HTML, CSS, JavaScript).
* **Telepítés:** A generált statikus fájlok áthelyezése a Flask alkalmazás statikus mappájába, biztosítva a zökkenőmentes elérést a szerveren keresztül. A felhasználói élmény szempontjából csak egy modern böngészőre van szükség, mivel a felület reszponzív és minden logika a szerveren fut.


![Deployment Plan](static/images/telepitesi_terv.png)


### Karbantartási Terv

A karbantartási terv biztosítja a rendszer hosszú távú stabilitását, különös tekintettel az MI-vezérelt komponensekre és az érzékeny egészségügyi adatok kezelésére.

**1. Corrective Maintenance (Hibajavítás)**

* **Hibanaplózás:** Rendszeres (heti) hibanaplózás és riasztások áttekintése.
* **Azonnali Beavatkozás:** Hibás adatbázis-inkonzisztenciák (pl. a naplózásban fellépő anomáliák) és a kritikus AI-logika hibáinak azonnali javítása.

**2. Adaptive Maintenance (Alkalmazkodás)**

* **AI-modell Frissítések:** A **Gemini API** újabb verzióinak, funkcióinak és a mögöttes AI-modellek változásainak rendszeres ellenőrzése és lekövetése, az alkalmazás kódjának adaptálása.
* **Külső API Változások:** A **Nutritionix API** interfészében, URL-jeiben vagy hitelesítési mechanizmusában bekövetkező változások azonnali lekövetése és a backend frissítése.
* **Technológiai Frissítések:** A főbb függőségek (React, Flask, PostgreSQL) kritikus biztonsági frissítéseinek beépítése.

**3. Perfective Maintenance (Fejlesztés és Optimalizálás)**

* **Teljesítmény Optimalizálás:** A kritikus API hívások (különösen a `plan/generate` Gemini hívás) sebességének és hatékonyságának rendszeres felülvizsgálata.
* **Új Funkciók:** Új, tervezett funkciók (pl. fejlettebb grafikonok, új AI chat mód) bevezetése a felhasználói visszajelzések alapján.

**4. Preventive Maintenance (Megelőző Karbantartás)**

* **Adatbázis Mentés:** Rendszeres (napi/heti) **PostgreSQL adatbázis mentés** biztosítása, különös tekintettel a felhasználói egészségügyi adatok (Health Data) biztonságos megőrzésére.
* **Kód Audit:** Időszakos kódbázis felülvizsgálat (Code Review) elvégzése a potenciális biztonsági rések és teljesítményproblémák megelőzése érdekében.

![Maintenance Plan](static/images/karbantartasi_terv.png)