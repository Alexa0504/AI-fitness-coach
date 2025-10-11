



















































































































































































## Üzleti folyamatok modellje

Az **AI Fitness Coach** rendszer célja, hogy egy intelligens, személyre szabott edzési és életmódtámogató platformot biztosítson a felhasználók számára. A folyamat középpontjában az AI-alapú tervgenerálás és a valós idejű visszajelzés áll, amely lehetővé teszi, hogy minden felhasználó saját igényeihez igazított támogatást kapjon.

A rendszer üzleti folyamata a következő lépésekre bontható:

1. **Regisztráció és profilkezelés:**  
   A felhasználó létrehozza profilját, megadja alapadatait (nem, életkor, testsúly, célok), amelyeket az adatbázisban tárol a rendszer.  
   Ezek az adatok képezik az AI ajánlásainak alapját.

2. **Célok meghatározása és adatgyűjtés:**  
   A felhasználó beállíthat konkrét célokat (pl. fogyás, izomnövelés, állóképesség javítás).  
   A rendszer naplózza a haladást, és figyeli az esetleges hiányos adatokat.

3. **AI tervgenerálás:**  
   Az alkalmazás a Gemini AI modellhez továbbítja a felhasználó adatait.  
   A modell visszaküldi az edzési és étrendi javaslatokat, amelyeket a backend feldolgoz, validál és eltárol.

4. **Terv megjelenítés és interakció:**  
   A frontend React-alapú dashboardja jeleníti meg az aktuális edzéstervet, heti összesítéseket és motivációs elemeket (pl. jelvények, fejlődés mértéke).

5. **Felhasználói naplózás és visszajelzés:**  
   A felhasználó rögzíti edzéseit és étkezéseit.  
   Ezek az adatok frissítik a statisztikákat, és az AI újraértékeli a terveket, szükség esetén módosításokat javasol.

6. **Motiváció és gamification:**  
   A rendszer pontokat, ranglistát és jelvényeket ad, hogy ösztönözze a felhasználót a rendszeres aktivitásra.

7. **Haladás és statisztika:**  
   A backend feldolgozza az adatokat, és összesített statisztikát generál, amely a felhasználó teljesítményének időbeli alakulását jeleníti meg a grafikonokon.

## Követelmények
A rendszer követelményei két nagy csoportra oszthatók: funkcionális és nem funkcionális követelmények.

### Funkcionális követelmények

- **Felhasználói profilkezelés:** regisztráció, bejelentkezés, célok beállítása, adatmódosítás.  
- **AI integráció:** a rendszer képes a Gemini API-n keresztül edzési és étrendi javaslatokat kérni és fogadni.  
- **Adatbázis-kezelés:** felhasználói, cél- és edzésadatok mentése, lekérdezése, frissítése.  
- **Dashboard megjelenítés:** a felhasználó aktuális állapotának, tervének és statisztikáinak vizuális megjelenítése.  
- **Naplózás:** napi edzések, étkezések és teljesítménymutatók rögzítése.  
- **Gamification:** pontszámítás, ranglista és jelvényrendszer működtetése.  
- **Valós idejű kommunikáció:** az AI válaszai és a felhasználói visszajelzések azonnali frissítése.  
- **Admin funkciók (opcionális):** rendszerfelügyelet, adatellenőrzés és hibajavítás.

### Nem funkcionális követelmények

- **Teljesítmény:** a dashboard frissítése valós időben, minimális késleltetéssel.  
- **Skálázhatóság:** több ezer felhasználó egyidejű kiszolgálása.  
- **Biztonság:** titkosított kommunikáció (HTTPS), jelszavak hash-elése, adatszivárgás elleni védelem.  
- **Kompatibilitás:** a rendszer működjön modern böngészőkben (Chrome, Firefox, Edge, Opera Browser).  
- **Felhasználói élmény:** letisztult, intuitív felület, reszponzív megjelenítés.  
- **Karbantarthatóság:** moduláris kódstruktúra, jól dokumentált API-k.  
- **Megbízhatóság:** hibakezelés minden rétegben (AI válaszhiba, adatbázis kapcsolat, invalid input).

## Funkcionális terv

A rendszer célja egy **interaktív és személyre szabott webes alkalmazás** létrehozása, amely segíti a felhasználókat a **saját edzési céljaik elérésében** és az egészséges életmód fenntartásában. A felhasználó naplózhatja edzéseit és étkezéseit, az AI javaslatokat ad a fejlődéshez, és a rendszer pontokat, jelvényeket és statisztikákat biztosít a motiváció fenntartására. A felület letisztult és könnyen kezelhető, hogy a felhasználó az edzésre és az egészségre tudjon koncentrálni.

### Rendszerszereplők

- **Felhasználó:** Az a személy, aki regisztrál, kitölti a profilját, követi az edzéstervét, naplózza az edzéseit és étkezéseit, és megtekinti a statisztikákat, játékos elemeket (pontok, jelvények, ranglista).  
- **Admin (opcionális):** Felügyeli a felhasználókat, ellenőrzi az adatokat, és karbantartja a rendszert.  

### Rendszerhasználati esetek és lefutásaik

- **Profil létrehozása és szerkesztése**  
A felhasználó regisztrál az alkalmazásba, megadja alapadatait (nem, életkor, testsúly, célok). A rendszer eltárolja ezeket az adatokat az adatbázisban, amelyek az AI tervgenerálás alapját képezik. A felhasználó bármikor módosíthatja a profilját és céljait.

- **Célok beállítása**  
A felhasználó kiválaszthatja az elérni kívánt célokat (pl. fogyás, izomtömeg növelés, állóképesség fejlesztés). A rendszer ezeket a célokat figyelembe veszi az AI tervgenerálás során.

- **AI terv generálása**  
A felhasználó kérheti az AI által készített edzéstervet. A backend elküldi a felhasználói adatokat az AI modellnek, amely visszaküldi a személyre szabott edzési és étrendi javaslatokat. A rendszer tárolja és frissíti ezeket a terveket.

- **Terv megjelenítése a dashboardon**  
A felhasználó a React-alapú dashboardon látja az aktuális edzéstervét, heti összesítéseket, motivációs jelvényeket, és a célokhoz viszonyított előrehaladást.

- **Edzés és étkezés naplózása**  
A felhasználó rögzíti elvégzett edzéseit és az étkezéseit. A rendszer feldolgozza ezeket az adatokat, frissíti a statisztikákat, és az AI újraértékeli a terveket, ha szükséges.

- **Játékos elemek frissítése**  
A rendszer pontokat, jelvényeket és ranglistát biztosít a felhasználói aktivitás alapján. A felhasználó folyamatos visszajelzést kap a haladásáról.

- **Statisztikák és trendek megjelenítése**  
A backend összesített statisztikákat készít a felhasználó tevékenységeiről, amelyek a dashboardon grafikonok és trendek formájában jelennek meg, így a felhasználó könnyen áttekintheti fejlődését.

### Menü-hierarchia

Az alkalmazás menüstruktúrája egyszerű és könnyen átlátható, egyértelmű navigációt biztosítva:

- **Dashboard:** A főoldal, ahol az AI által generált terv, a heti statisztikák és motivációs jelvények láthatók.  
- **Naplózás:** Itt rögzítheti a felhasználó az edzéseit és étkezéseit.  
- **Statisztikák:** Grafikonos és táblázatos formában mutatja az előrehaladást, célok teljesülését.  
- **Gamification / Ranglista:** A felhasználó megtekintheti pontjait, jelvényeit, és a többi felhasználóval összehasonlíthatja eredményeit.  
- **Profil:** A felhasználó módosíthatja személyes adatait és céljait.  
- **Beállítások / Kilépés:** Alkalmazás beállítások módosítása, kijelentkezés.

## Architekturális terv


