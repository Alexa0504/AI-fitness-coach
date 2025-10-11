# Követelmény Specifikáció

## Bevezetés és Projektcél

Az AI-Driven Fitness Coach projekt célja egy forradalmi, személyre szabott webalkalmazás létrehozása, amely az adatok és a gépi tanulás erejét használva optimalizálja a felhasználók edzés- és táplálkozási terveit.

A rendszer definiálása: egy dinamikusan adaptív, adatvezérelt fitnesz és wellness asszisztens, amely megfizethető és széles körben elérhető alternatívát kínál a tradicionális, drága személyi edzői szolgáltatásokkal szemben.

Projektcél: A felhasználók fitnesz céljainak (súlyvesztés, izomnövekedés, erőnlét, stb.) hatékonyabb elérése, miközben minimalizálja a sérülések kockázatát a technika és a regenerálódás precíz monitorozásával.

Célközönség: Két fő csoport: a kezdők és az átlagfelhasználók (akik iránymutatást és motivációt igényelnek), valamint a haladók (akik optimalizálni szeretnék teljesítményüket a stagnálás elkerülése végett).

Az AI/Gépi Tanulás (ML) kulcsfontosságú szerepe abban rejlik, hogy képes folyamatosan elemezni az egyéni teljesítményt, a biometrikus adatokat és a visszajelzéseket, biztosítva ezzel a terv valós idejű adaptálását.

Az alkalmazás platformja elsődlegesen egy modern webes alkalmazás lesz (React alapon), amely a skálázhatóságot és az elérhetőséget helyezi előtérbe, és megalapozza a későbbi mobil (React Native) kiterjesztés lehetőségét.

A rendszernek stabil, tudományos alapot kell biztosítania minden edzési döntéshez.

## Jelenlegi üzleti folyamatok modellje

## Jelenlegi helyzet

A digitális fitnesz alkalmazások jelenlegi állapota számos kihívást tartogat a felhasználók számára. Gyakran előfordul, hogy az edzéstervek nem igazodnak a felhasználó személyes igényeihez és céljaihoz, amely a fejlődés lassulásához vezethet. Emellett a helytelen mozgásforma gyakran sérülésveszélyt jelenthet, különösen kezdők vagy kevés edzési tapasztalattal rendelkezők számára.
A táplálkozási adatok manuális rögzítése rendkívül időigényes és pontatlan lehet, ezért sokan elhanyagolják a naplózást, ami csökkenti a hatékonyságot.

További problémát jelent, hogy a statikus, előre rögzített edzéstervek nem képesek alkalmazkodni a felhasználó aktuális teljesítményéhez vagy közérzetéhez, így a motiváció fenntartása is nehéz lehet. A legtöbb jelenlegi alkalmazás nem használ AI-alapú interakciót a felhasználói szokások és az előrehaladás elemzésére, így a személyre szabott visszajelzés és az adaptív fejlődés lehetősége hiányzik. Gyakori, hogy a felhasználók több különálló alkalmazást használnak egyszerre, például fitnesz, kalóriaszámláló és jegyzetelő alkalmazásokat, amely megnehezíti az adatok áttekintését.

 Összességében tehát hiányzik egy integrált, személyre szabott és azonnali visszajelzést nyújtó rendszer, amely összekapcsolja az edzés- és táplálkozási adatokat, és folyamatos visszajelzést biztosít a felhasználó számára.

 ## Vágyálom rendszer

 Az ideális AI Fitness Coach egy olyan interaktív és adaptív rendszert képvisel, amely nem csupán adatokat tárol, hanem valós segítséget nyújt a felhasználónak. Tulajdonképpen egy személyre szabott, digitális edzőként működik. A rendszer valós idejű visszajelzést ad az edzések során, amely támogatja a helyes mozgásforma elsajátítását és a sérülések elkerülését. Az edzéstervek automatikusan módosulnak a felhasználó teljesítményének és állapotának függvényében, így a kihagyott napok vagy új célok nem rontják a fejlődést.  

Az AI alapú motivációs rendszer folyamatosan személyre szabott üzeneteket, emlékeztetőket és statisztikai visszajelzéseket biztosít. Emellett a rendszer integrálja a táplálkozási javaslatokat, amelyek összhangban vannak az edzéstervekkel, figyelembe véve a napi energiaszükségletet és az étkezési preferenciákat. A haladás nyomon követhető grafikonok és kimutatások segítségével, miközben a játékos elemek, mint például a célkitűzések, ranglisták és jelvények, fokozzák a motivációt. Mindez egy felhasználóbarát, React alapú felületen keresztül érhető el, amely reszponzív és könnyen navigálható.

## Funkcionális követelmények

A rendszer fő funkciói a felhasználói élmény maximalizálására és az interakciók zökkenőmentessé tételére összpontosítanak. Az egyik legfontosabb elem az AI-alapú edzésterv generálás, amely a felhasználó profilja és céljai alapján készül, és módosul a teljesítmény vagy a kihagyott edzések függvényében. A táplálkozási tanácsadás szintén AI által generált, és napi illetve heti szinten biztosít személyre szabott étrendet, figyelembe véve az allergiákat, preferenciákat és kalóriacélokat.  

A rendszer haladást követő modulja részletes statisztikákat és grafikonokat nyújt az edzések, teljesítmény és étkezések tekintetében, miközben az AI folyamatosan értékeli a fejlődést és motivációs üzeneteket küld a felhasználónak. Emellett a ranglisták és a célkitűzések segítik a versenyszellem és a motiváció fenntartását. Az AI-vezérelt elemzés a naplózott adatokat feldolgozva szöveges visszajelzéseket ad az edzések hatékonyságáról.

A felhasználói felület React technológiára épül, biztosítva a könnyű kezelhetőséget és a valós idejű adatfrissítést. A navigáció egyszerűen történik a profil, az edzéstervek, az étkezési tervek és a statisztikák között, így a felhasználó mindig naprakész információkhoz juthat.

Összességében ezek a funkciók biztosítják, hogy az alkalmazás személyre szabott, motiváló és könnyen kezelhető legyen minden felhasználó számára.

## Nem funkcionális követelmények és technológia

Ez a szakasz részletezi a Fitness Coach AI alkalmazásunk technológiai döntéseit és nem funkcionális követelményeit. A célunk egy olyan termék létrehozása, amely hatékony, megbízható, személyre szabott és skálázható.

A felhasználói felület megvalósításához frontendhez **HTML**, **CSS** és **JavaScript** nyelveket használunk, illetve **React**-et, backendhez pedig **Pythont**, ezen belül **Flask** keretrendszert. Adatbázisnak pedig **PostgreSQL**-adatbázit használunk.

**Teljesítmény**:  Az alkalmazásnak gyors válaszidőt kell produkálnia, különösen az AI-alapú funkcióknál. A Python/Flask backend optimalizálásával a tervgenerálás maximális válaszideje 5 másodperc lehet. Az alapvető adatbázis-lekérdezések (pl. naplóbejegyzések, statisztikák) válaszideje nem haladhatja meg a 200 ms-ot.

**Megbízhatóság**: A személyes adatok védelme és a rendszer stabilitása kiemelt. A jelszavak hashelése és az adatok titkosítása a PostgreSQL-ben kötelező. Minden adatforgalom a frontend és a backend között HTTPS/TLS protokollon keresztül, titkosítva történik.

**Karbantarthatóság**: A seed.py szkript használatával biztosítjuk, hogy a fejlesztőcsapat minden tagja egységes adatbázis-struktúrával és tesztadatokkal dolgozzon, ami csökkenti a hibák esélyét.

**Felhasználóbarát UI**: A felületnek intuitívnak és könnyen kezelhetőnek kell lennie, biztosítva a felhasználói élmény maximalizálását. A **React** keretrendszer használata biztosítja, hogy a design letisztult és a navigáció egyszerű legyen a profil, a személyre szabott edzések, a táplálkozási tervek és a haladási statisztikák között. A React komponens-alapú felépítése garantálja a gyors valós idejű adatfrissítést a Gemini API-ból érkező AI-válaszok és grafikonok esetében, ami létfontosságú az adaptív rendszernél.

**Korlátok**: Mivel a felhasználók személyes profiladatait, edzésnaplóit, étkezési céljait és a célkitűzéseket a **PostgreSQL adatbázisban** tároljuk, az adatok tartósan megmaradnak, és a felhasználók visszatérő munkamenetek során is elérhetik a korábbi eredményeiket. A rendszer lehetővé teszi, hogy a felhasználó progressziója (súly, teljesítmény) és a motivációs jelvények folyamatosan frissüljenek.

## Követelménylista

## Funkcionális követelmények (AI Fitness Coach)

| Modul ID | Név és Kifejtés |
| :--- | :--- |
| **K1** | **Adatkezelés és Profil**<br>A program a felhasználói adatokat (súly, nem, célok), az edzésnaplókat és az AI által generált terveket egy **PostgreSQL adatbázisból** olvassa be. Ha a felhasználói profil hiányos, a program regisztrációs űrlappal reagál. |
| **K2** | **AI Tervgenerálás Logika**<br>A program a felhasználó céljai és profiladatai alapján kéri le a **Gemini API-tól** a személyre szabott edzés- és étrendtervet. A tervet a rendszer eltárolja, és szükség esetén módosítja a felhasználó új céljai alapján. |
| **K3** | **Haladás Elemzés**<br>Az AI algoritmus folyamatosan értékeli a felhasználó naplózott teljesítményét és étkezését. **Szöveges visszajelzéseket** és statisztikai elemzéseket biztosít, amelyek a felhasználói teljesítmény **hatékonyságától** is függenek. |
| **K4** | **Felhasználói Felület**<br>A felhasználó beírhatja adatait (regisztráció), majd **megjeleníti** a Coach elemeit: **személyre szabott étrend**, **adaptív edzésterv**, fejlődési **grafikonok**, és az AI-tanácsadó Chat gombját. |
| **K5** | **Naplózó Képernyő**<br>A felhasználó **megjeleníti** az étkezési és edzési naplót. Lehetővé teszi az adatok manuális rögzítését, valamint a **Nutritionix API-val** való kiegészítését a pontos kalóriaszámlálás érdekében. |
| **K6** | **Adatbázisba mentés**<br>A felhasználó által rögzített napi edzés- és étkezési adatokat, valamint a Gemini által generált hosszú szöveges tanácsokat a program elküldi a backendnek, amely az adatokat a **PostgreSQL adatbázisba** menti a tartós tárolás érdekében. |
| **K7** | **Motivációs Modul**<br>A főmenüből megtekinthető a célkitűzések státusza és a megszerzett **jelvények** listája. A rendszer **személyre szabott emlékeztetőket** és motivációs üzeneteket küld. |