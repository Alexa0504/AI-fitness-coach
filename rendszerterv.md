



















































































































































































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


