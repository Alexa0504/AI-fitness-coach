# Funkcionális Specifikáció

## Projektvízió

Az **AI-Driven Fitness Coach** projekt célja egy forradalmi, személyre szabott webalkalmazás létrehozása, amely az adatok és a gépi tanulás erejét használva optimalizálja a felhasználók edzés- és táplálkozási terveit.

**A rendszer definiálása:** egy dinamikusan adaptív, adatvezérelt fitnesz és wellness asszisztens, amely megfizethető és széles körben elérhető alternatívát kínál a tradicionális, drága személyi edzői szolgáltatásokkal szemben.

**Projektcél:** A felhasználók fitnesz céljainak (súlyvesztés, izomnövekedés, erőnlét, stb.) hatékonyabb elérése, miközben minimalizálja a sérülések kockázatát a technika és a regenerálódás precíz monitorozásával.

**Célközönség:**
**Két** fő csoport: a kezdők és az átlagfelhasználók (akik iránymutatást és motivációt igényelnek), valamint a haladók (akik optimalizálni szeretnék teljesítményüket a stagnálás elkerülése végett).

Az **AI/Gépi Tanulás** (ML) kulcsfontosságú szerepe abban rejlik, hogy képes folyamatosan elemezni az egyéni teljesítményt, a biometrikus adatokat és a visszajelzéseket, biztosítva ezzel a terv valós idejű adaptálását.

Az alkalmazás platformja elsődlegesen egy modern webes alkalmazás lesz (React alapon), amely a skálázhatóságot és az elérhetőséget helyezi előtérbe, és megalapozza a későbbi mobil (React Native) kiterjesztés lehetőségét.

A rendszernek stabil, tudományos alapot kell biztosítania minden edzési döntéshez.

## Jelenlegi helyzet (Piaci Rések)

A jelenlegi fitneszpiac több kritikus réssel küzd, amelyek indokolják az **AI-Driven Fitness Coach** rendszer szükségességét.

### A hagyományos edzés korlátai

A személyi edzői szolgáltatások magas költsége és korlátozott elérhetősége pénzügyi akadályt jelent az átlagfelhasználók számára. 
A tervek minősége gyakran szubjektív, az edző egyéni tapasztalatától függ, nem pedig nagyszámú adaton alapuló objektív elemzéstől. Nincs lehetőség a napi szintű, aprólékos biometrikus adatelemzésre.

### A statikus appok kudarca

A piacon lévő fitness appok többsége merev, előre rögzített terveket használ, amelyek nem képesek a valós idejű adaptációra. 
Ezek a tervek nem reagálnak a felhasználó aktuális állapotára (fáradtság, rossz alvás, stressz), ami túledzéshez vagy hatékonyságvesztéshez vezethet.

### Minőségellenőrzés és Adatrögzítés

A legkomolyabb probléma a mozgástechnika ellenőrzésének teljes hiánya. Ez növeli a sérülésveszélyt, mivel a rosszul végrehajtott gyakorlatokra nincs azonnali visszajelzés.
Továbbá, a táplálkozási és edzésadatok manuális rögzítése időigényes és pontatlan. 
A felhasználók gyakran kihagyják a naplózást, vagy pontatlan adatokat visznek be, ami torzítja a teljesítménykövetést és a kalóriaszámítást. 
Hiányzik az integrált, minőségi visszajelzést nyújtó rendszer.

## Követelménylista

A projekt sikeres megvalósításához elengedhetetlen a funkcionális modulok világos definiálása.  
A rendszer hét fő modulra épül (K1–K7), amelyek együtt biztosítják a személyre szabott, adatvezérelt működést.  
Az alábbi táblázat bemutatja mindegyik modul fő célját, működését és a hozzájuk tartozó logikai kapcsolatokat.

| Modul ID | Név és Kifejtés |
|-----------|-----------------|
| **K1** | **Adatkezelés és Profil**<br>A rendszer a felhasználói adatokat — például testsúly, életkor, nem, edzési célok és korábbi tevékenységek — a **PostgreSQL adatbázisban** tárolja. Az AI ezen adatok alapján készít személyre szabott javaslatokat, és ellenőrzi a célok elérését. Ha a profil hiányos, a felhasználót egy interaktív regisztrációs űrlap irányítja a kiegészítéshez, biztosítva, hogy minden releváns információ rendelkezésre álljon. |
| **K2** | **AI Tervgenerálás Logika**<br>A modul a felhasználó céljai, preferenciái és eddigi teljesítménye alapján kéri le a **Gemini API-tól** a személyre szabott edzésterveket és étrendi javaslatokat. Az algoritmus képes dinamikusan módosítani a terveket, ha a felhasználó új célokat ad meg, vagy ha az AI elemzése szerint a jelenlegi terv hatékonysága csökkenne. |
| **K3** | **Haladás Elemzés**<br>Az AI folyamatosan elemzi a felhasználó naplózott tevékenységeit és étkezési adatait. A rendszer **részletes statisztikákat**, grafikonokat és szöveges értékeléseket készít, amelyek segítik a felhasználót a fejlődés nyomon követésében. Az elemzések figyelembe veszik az adott felhasználó teljesítményét és a kitűzött célokhoz viszonyított hatékonyságot. |
| **K4** | **Felhasználói Felület**<br>A React-alapú frontend biztosítja a felhasználó számára az interaktív élményt. A felhasználó egyszerűen beviheti adatait, frissítheti profilját és céljait, valamint áttekintheti a **személyre szabott edzésterveket, étrendjavaslatokat**, és a fejlődési grafikonokat. A felület lehetővé teszi az AI Coach-al való közvetlen kommunikációt, kérdések feltételét és az edzéstervek valós idejű módosítását. Emellett motivációs jelvények, ranglisták és értesítések segítik a folyamatos aktivitás fenntartását. |
| **K5** | **Naplózó Képernyő**<br>A felhasználó manuálisan vagy külső szolgáltatások (pl. Nutritionix API) segítségével rögzítheti az étkezési és edzési adatait. A napló modul lehetőséget biztosít a részletes kalóriaszámlálásra, a tápanyagok nyomon követésére és az edzésterhelés optimalizálására, így az AI pontosabb visszajelzést tud adni. |
| **K6** | **Adatbázisba Mentés**<br>Az összes felhasználói bevitel, valamint az AI által generált tervek és tanácsok biztonságosan kerülnek mentésre a **PostgreSQL adatbázisba**. Az adatátvitel titkosított, és minden új adatrögzítés után automatikus biztonsági mentés történik, biztosítva az adatok tartósságát és integritását. |
| **K7** | **Motivációs Modul**<br>A modul a felhasználói célokat, elért eredményeket és a megszerzett **jelvényeket** kezeli. Az AI személyre szabott értesítéseket és motivációs üzeneteket küld, hogy a felhasználó folyamatosan elkötelezett maradjon. Emellett a ranglisták és kihívások vizuálisan is követhetők, elősegítve a közösségi interakciót és az egészséges versenyszellemet. |


A modulok egymással szoros logikai kapcsolatban állnak: az adatkezelés biztosítja az alapokat, az AI logika feldolgozza az információkat, majd az eredmények a felhasználói felületen jelennek meg.  
A rendszer működése ciklikus — a felhasználói adatok folyamatosan frissülnek, az AI pedig valós időben reagál a változásokra.

## Jelenlegi üzleti folyamatok modellje

A meglévő üzleti modellek folyamatai **súrlódásokat** okoznak, főleg a manuális és nem adaptív lépések miatt.

### Hagyományos edzői folyamat

A folyamat a rugalmatlan, **manuális** időpont egyeztetéssel kezdődik. 
A kezdeti adatfelvétel (célok, étrend) szubjektív és **statikus** dokumentumokban rögzül. Az edzésterv kézzel, fix ciklusokra készül, és nem módosítható automatikusan a felhasználó állapotváltozásai (pl. sérülés vagy kipihentség) szerint. 
A dietetikai követés és az étrend ellenőrzése is nehézkes, mivel a naplózás a felhasználó pontosságától függ.

### Statikus appos folyamat

A felhasználó kiválaszt egy **fix** kategóriájú tervet, amely innentől kezdve nem adaptív. 
Az edzésrögzítés csak mennyiségi adatokat (ismétlés, súly) gyűjt, de a mozgás minőségét nem ellenőrzi. 
Ha a felhasználó eltér a tervtől, a rendszer nem indít automatikus korrekciót. (pl. regenerációs nap beiktatását) 
A visszajelzések pusztán számokból állnak, hiányzik az AI által generált értelmező szöveges elemzés.

### Funkcionális követelmények törése

A funkciók hierarchikus bontása mutatja, hogyan épül fel a rendszer almodulokból.

#### I. AI-vezérelt edzéstervezés és korrekció

- **Dinamikus Tervgenerálás (K2):** Gemini API hívás, amely a felhasználói profil (K1) és a teljesítmény adatok (K6) alapján személyre szabott tervet állít elő.

- **Adaptív Logika (K2):** Az MI folyamatosan újraértékeli a tervet a napi edzés- és biometrikus adatok (K6) alapján, biztosítva a Regeneráció Kezelését (túlterhelés elkerülése).

- **Edzésnapló Rögzítése (K6):** Felület a sorozatok, ismétlések és súlyok bevitelére, a Progressziós Menedzsment (K3) adatalapja.

#### II. Táplálkozás és életmód menedzsment

- **AI Étrendtervezés (K2):** A Gemini API-n keresztül generálja az étrendet a K1 adatok és az edzési energiaigény alapján.

- **Táplálkozási Napló (K5):** Képernyő az étkezési adatok bejegyzésére. A felhasználó a bevitt ételekhez rögzíti a mennyiségeket.

- **Adatfeldolgozás és Számítás (K5, K3):** A rendszer (K5, K3) a rögzített ételek és mennyiségek alapján makrók és kalóriák becslését végzi el az AI logika (K2) utasításainak megfelelően.

#### III. Haladáskövetés és motiváció

- **Részletes Statisztikák (K4):** Grafikonok és kimutatások megjelenítése (React komponens) a fejlődésről.

- **Szöveges Elemzés (K3):** Az MI (Gemini) értelmező szöveges összefoglalót ad a heti teljesítményről, növelve a felhasználói tudatosságot.

- **Motivációs Modul (K7):** Rendszer a célok státuszának és a megszerzett jelvények kiosztására, valamint személyre szabott emlékeztetők küldésére.

#### IV. Felhasználói felület és adatintegráció

- **React Felület (K4):** Biztosítja a felhasználóbarát, moduláris felépítést és a gyors adatfrissítést.

- **Adatbázis Kapcsolat (K1, K6):** Flask backend felelős a frontend (React) és a PostgreSQL adatbázis közötti biztonságos adatátvitelért és tárolásért.

- **Gemini API Kapcsolat (K2):** Backend szerviz a Gemini hívások kezelésére.

## Igényelt üzleti folyamatok modellje

Az AI Coach működését egy dinamikus, **adatvezérelt üzleti modell** támogatja.  
A cél egy 24/7 elérhető digitális személyi edző, amely valós időben képes reagálni a felhasználó állapotára, motivációjára és teljesítményére.

A folyamat középpontjában a **felhasználói adatok elemzése és visszacsatolása** áll.  
Az AI a naplózott adatokból kiindulva javaslatokat készít, majd a felhasználó visszajelzései alapján tovább finomítja az ajánlásokat.  
Ez az interaktív körforgás biztosítja, hogy a rendszer mindig releváns, aktuális és személyre szabott legyen.

A **költséghatékonyság** kulcsfontosságú üzleti előny: a platform automatizálja a személyi edzői feladatokat, így a felhasználó jóval kedvezőbb áron kap teljes körű támogatást.  
Ezen felül a skálázható architektúra lehetővé teszi a gyors bővítést és a felhasználói szám növelését.  
A **valós idejű visszajelzés** és az **AI-alapú motiváció** versenyelőnyt biztosít a piacon, mivel a legtöbb fitneszalkalmazás nem kínál ilyen mélységű személyre szabást.

## Használati esetek

A rendszer három fő szereplő köré épül: **Felhasználó**, **AI Coach (Rendszer)** és **Admin**.  
Az alábbiakban bemutatjuk az egyes szerepkörök engedélyeit és feladatait.

- **Felhasználó:**  
  - Regisztrálhat, bejelentkezhet, megadhatja céljait és naplózhatja napi tevékenységét.  
  - Megtekintheti a fejlődését, módosíthatja az edzéstervet, és interakcióba léphet az AI Coach-al.  
  - Hozzáfér az étkezési statisztikákhoz, a motivációs modulhoz és a jutalomrendszerhez.

- **AI Coach (Rendszer):**  
  - Elemzi a felhasználói adatokat, és ezek alapján automatikusan frissíti az edzéstervet.  
  - Valós idejű kommunikációt biztosít: tanácsokat, figyelmeztetéseket és javaslatokat ad.  
  - Az AI figyeli a trendeket, például az edzésgyakoriság csökkenését, és erre motiváló üzenetekkel reagál.

- **Admin:**  
  - Felügyeli a rendszer működését, karbantartja az adatbázist, kezeli a felhasználói fiókokat.  
  - Ellenőrzi az AI által generált tartalmakat, hogy azok megfeleljenek az etikai és adatvédelmi irányelveknek.  

Ezek a szerepkörök egy jól strukturált, biztonságos és átlátható működési modellt alkotnak.

## Hogyan fedik le a használati esetek a követelményeket

A követelmények **(K1-K7)** szoros kapcsolatban állnak a felhasználási esetekkel, igazolva, hogy a tervezett funkciók valóban megoldják a jelenlegi üzleti hiányosságokat.

#### Probléma: Sérülésveszély és Statikus Tervek

- **Megoldás (K2, K3):** A K2 (AI Logika) és a K3 (Elemzés) fedezi az Edzés Technika Elemzése használati esetet. Az MI feldolgozza a mozgás adatokat, és szöveges korrekciós visszajelzést ad, ami a sérülésmegelőzés és a statikus appok legnagyobb hibája ellen hat.

- **Megoldás (K2, K6):** A K2 és K6 (Adatbázis mentés) fedezi a Dinamikus Terv Módosítás használati esetet. A K6 tárolt valós idejű adatok alapján a K2 automatikusan optimalizálja a terhelést, megszüntetve a statikus tervezés problémáját.

#### Probléma: Pontatlan Adatrögzítés és Alacsony Megtartás

- **Megoldás (K5):** A K5 (Naplózó Képernyő) fedezi a Pontos Étrend Naplózás használati esetet. A K5 lehetővé teszi a felhasználó számára, hogy részletes adatokat adjon meg az elfogyasztott ételekről, amelyeket a K2/K3 logika elemzésre használ fel ahelyett, hogy külső API-ra támaszkodna.

- **Megoldás (K7, K4, K3):** A K7 (Motiváció), K4 (UI) és K3 (Elemzés) fedezi a Folyamatos Motiváció és a Személyre Szabott Visszajelzés használati eseteket. A játékosítási elemek és a Gemini által generált magyarázó szöveges elemzések növelik az elkötelezettséget és csökkentik a lemorzsolódást.

## AI Logika és Működési Szabályok

A rendszer intelligens működését a **Gemini API** biztosítja, amely a természetes nyelvfeldolgozást és a személyre szabott edzési tanácsadást valósítja meg.  
A rendszer **nem használ kép- vagy mozgáselemzést**, így **TensorFlow vagy más ML-keretrendszer** alkalmazására **nincs** szükség.  
A hangsúly a **szöveges adatelemzésen** és a **valós idejű döntéstámogatáson** van.

A **Gemini API** helyzetfüggő prompt-sablonokat használ: az AI az aktuális edzéstervek, célok és naplóadatok alapján ad visszajelzéseket.  
Ha a felhasználó például azt írja, hogy „fáradt vagyok”, az AI pihenőnapot javasol, enyhébb edzést kínál, vagy motivációs üzenetet küld.  
A logika képes felismerni a hosszú távú mintákat (pl. inaktivitás, javuló teljesítmény), és ehhez igazítja a javaslatokat.

A **haladáskövetés** szabályai szerint a rendszer minden interakció után mentést végez, és 24 óránként teljes adatmentést hajt végre.  
A statisztikák heti, havi és éves bontásban készülnek, a fejlődés pedig grafikonokon és AI-elemzésekben jelenik meg.  

A **játékosítás (gamification)** növeli a motivációt: a felhasználók pontokat, jelvényeket és szinteket gyűjthetnek, amelyek a profiljukban láthatók.  
A ranglisták és kihívások dinamikusan frissülnek, az AI pedig a felhasználó teljesítménye alapján módosítja a nehézségi szinteket és ajánlásokat.

## Felhasználói Folyamatok (User Flow)

A rendszer célja, hogy a felhasználó egy **egyszerű, átlátható és interaktív** folyamat során érje el a céljait, egy **személyes, digitális edző** támogatásával. A következőkben bemutatjuk a felhasználói folyamatokat a belépéstől a napi terv adaptálásáig.


1.  **Alkalmazás Indítása és Profil Frissítése**
    A felhasználó megnyitja a webalkalmazást a böngészőben. A kezdőképernyőn a Bejelentkezés/Regisztráció történik. Ez kötelező lépés, mivel az adatok (célok, nem, súly) a **személyre szabott tervek** generálásához szükségesek (**K1**). A belépés után azonnal betöltődik a **React Dashboard** (**K4**).

2.  **AI Terv Generálás és Adaptálás**
    Az irányítópult megjeleníti az AI által generált **aktuális edzés- és étrendtervet** (**K2**). A felhasználó bármikor kezdeményezheti a terv frissítését vagy módosítását. A **Gemini API** a felhasználó teljesítménye és céljai alapján azonnal válaszol:
    * **Helyes adaptáció** esetén a terv automatikusan nehezebbé válik.
    * **Hibás adaptáció** (pl. kihagyott napok) esetén a rendszer az állapothoz igazított, könnyített tervet generál, valamint **szöveges figyelmeztetést** küld (**K3**).

3.  **Naplózás Képernyő**
    A felhasználó a navigációs sávon keresztül lép be a Naplózó Képernyőre (**K5**). Itt két fő tevékenységet végezhet:
    * **Edzés rögzítése:** Megadja az elvégzett gyakorlatok részleteit (ismétlések, súly).
    * **Étrend rögzítése:** Beírja a fogyasztott ételt. A rendszer a bevitelt azonnal kiegészíti a **Nutritionix API-tól** lekérdezett pontos tápértékkel (**K3**).

4.  **Visszajelzés és Motiváció**
    Az adatok rögzítése után (**K6**) a rendszer azonnal elemzést végez (**K3**):
    * **Szöveges visszajelzés:** A **Gemini AI** azonnal kiírja a Dashboardra a teljesítmény értékelését (pl. "Gratulálok a 15%-os súlyemelés növekedéshez!").
    * **Játékos elemek:** Az elért célkitűzésekért a felhasználó **jelvényeket** kap (**K7**).

5.  **Haladás Megtekintése**
    A felhasználó a **Statisztika** nézetre navigál. Itt megjelennek az interaktív **grafikonok** (**K4**) a súly, a teljesítmény és az étkezés változásairól.

6.  **AI Tanácsadás és Kilépés**
    A felhasználó a Chat ablakon keresztül (**K3/K4**) azonnali tanácsot kérhet a **Gemini API-tól**. A program bezárható, a **PostgreSQL adatbázisban** tárolt adatok (**K1/K6**) megőrződnek.

## Forgatókönyv

-   A felhasználó megnyitja az alkalmazást, bejelentkezik, és a **Dashboardon** látja az **AI-generált** napi tervét.

-   Elvégzi az edzést, majd a **Naplózó Képernyőn** (**K5**) rögzíti a vacsoráját (pl. "saláta csirkével").

-   A rendszer a **Nutritionix API** segítségével lekéri a tápértékeket, majd a **Gemini AI** elemzi, hogy a felhasználó túllépte-e a napi kalóriakeretét. (**K3**)

-   A **Gemini AI** azonnali **szöveges visszajelzést** küld a felhasználónak a Dashboardon (pl. "Nagyszerű edzés! Ügyelj a holnapi vízfogyasztásra!"). (**K3**)

-   A felhasználó a **Chatben** (K3/K4) felteszi a kérdését: "Mit egyek vacsorára?", amire a **Gemini API** azonnal válaszol.

-   A **Statisztika** nézetben a felhasználó látja, hogy új **jelvényt** szerzett (**K7**).

-   Ezután frissíti a profilját, (**K1**) és a rendszer **adaptálja** a tervet, (**K2**) majd kilép. 

Ez a felhasználói folyamat biztosítja, hogy az edzés és a táplálkozás követése **egyszerű, intuitív és motiváló** legyen, miközben valós idejű, személyre szabott segítséget nyújt.

## Megfeleltetés, hogyan fedik le a használati esetek a követelményeket

A felhasználói felület és a különböző funkciók szoros kapcsolatban állnak a követelményekkel. A fő cél a személyre szabott fitnesz- és táplálkozási támogatás nyújtása.

-   **Felhasználói Felület (**K4**):**
    * A **Dashboard** megjeleníti a **Gemini AI** által generált tervek és a haladási adatok összefoglalóját (**K2, K4**).
    * A navigációs sáv biztosítja az egyszerű átjárást a Naplózó (**K5**) és a Statisztika (**K4**) nézetek között.
    * A **React** reszponzivitása támogatja a **letisztult dizájnt**.

-   **AI Terv Képernyő:**
    * Az edzés- és étrendterv megjelenítése a **Gemini API** funkcionalitását testesíti meg (**K2**).
    * A terv folyamatos **adaptálása** a felhasználói adatok alapján biztosítja az optimális fejlődést.

-   **Visszajelzés és Motiváció:**
    * A **Szöveges visszajelzés** azonnali, személyre szabott megerősítést ad a felhasználónak a rögzített adatok elemzése alapján (**K3**).
    * A **Jelvények** (K7) megjelenítése és az elért célkitűzések státusza fokozza a **motivációt**.

-   **Adatkezelés és Integráció:**
    * A Naplózó képernyőn az adatok azonnal mentésre kerülnek a **PostgreSQL** adatbázisba (**K6, K1**).

## Képernyő Tervek

A képernyő tervek részletesen bemutatják az alkalmazás főbb nézeteit, amelyek a **React** és a **Bootstrap** keretrendszerekre épülnek, és az **AI** elemeket emelik ki.

-   **Főképernyő (Dashboard):**
    * Felső rész: A felhasználó neve, az aktuális cél. A navigációs sáv gombjai: *Terv*, *Napló*, *Statisztika*.
    * Középső Rész: Két fő **Bootstrap kártya**: **Napi Edzés Terv** és **Étrend Javaslat**. A kártyák a **Gemini API** legfrissebb adatait tartalmazzák. (**K2**)
    * Motivációs/Visszajelzés szekció: Itt jelenik meg a **Gemini** legutóbbi szöveges elemzése (**K3**), valamint a legújabb **jelvény** (**K7**).
    * **Letisztult**, modern, **reszponzív** elrendezés a **Bootstrap** komponensekkel.

-   **Naplózó Képernyő:**
    * Felső rész: Egy **React Form** az Edzés- és az Étkezés adatok beviteli mezőivel.
    * Ételkereső mező: Ide írja be a felhasználó az étel nevét, majd alatta azonnal megjelennek a **Nutritionix API** adatai a pontos rögzítéshez. (**K5**)

-   **Statisztika Képernyő:**
    * Felső rész: Interaktív **grafikonok** (vonal, oszlop) a teljesítmény (súly/ismétlésszám) és a súly (**K4**) változásairól.
    * Alul: A **célkitűzések** (**K7**) százalékos teljesülése.

-   **AI Chat Képernyő:** (**K3/K4**)
    * Felület, amely a **Gemini API-val** való valós idejű kommunikációt szolgálja (**K3**). Hagyományos chat ablak elrendezésben, ahol a felhasználó kérdést ír be, és azonnal választ kap.

-   **Reszponzív dizájn:**
    * A felület **React** és **Bootstrap** alapú kialakítása révén jól működik asztali gépen és mobil eszközökön is, garantálva a **reszponzív megjelenést**. (**K4**)

    ![Screen Design](static/images/kepernyokep.png)