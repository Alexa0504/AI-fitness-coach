# Követelmény Specifikáció

## 2. Jelenlegi helyzet

A digitális fitnesz alkalmazások jelenlegi állapota számos kihívást tartogat a felhasználók számára. Gyakran előfordul, hogy az edzéstervek nem igazodnak a felhasználó személyes igényeihez és céljaihoz, amely a fejlődés lassulásához vezethet. Emellett a helytelen mozgásforma gyakran sérülésveszélyt jelenthet, különösen kezdők vagy kevés edzési tapasztalattal rendelkezők számára.
A táplálkozási adatok manuális rögzítése rendkívül időigényes és pontatlan lehet, ezért sokan elhanyagolják a naplózást, ami csökkenti a hatékonyságot.

További problémát jelent, hogy a statikus, előre rögzített edzéstervek nem képesek alkalmazkodni a felhasználó aktuális teljesítményéhez vagy közérzetéhez, így a motiváció fenntartása is nehéz lehet. A legtöbb jelenlegi alkalmazás nem használ AI-alapú interakciót a felhasználói szokások és az előrehaladás elemzésére, így a személyre szabott visszajelzés és az adaptív fejlődés lehetősége hiányzik. Gyakori, hogy a felhasználók több különálló alkalmazást használnak egyszerre, például fitnesz, kalóriaszámláló és jegyzetelő alkalmazásokat, amely megnehezíti az adatok áttekintését.

 Összességében tehát hiányzik egy integrált, személyre szabott és azonnali visszajelzést nyújtó rendszer, amely összekapcsolja az edzés- és táplálkozási adatokat, és folyamatos visszajelzést biztosít a felhasználó számára.

 ## 3. Vágyálom rendszer

 Az ideális AI Fitness Coach egy olyan interaktív és adaptív rendszert képvisel, amely nem csupán adatokat tárol, hanem valós segítséget nyújt a felhasználónak. Tulajdonképpen egy személyre szabott, digitális edzőként működik. A rendszer valós idejű visszajelzést ad az edzések során, amely támogatja a helyes mozgásforma elsajátítását és a sérülések elkerülését. Az edzéstervek automatikusan módosulnak a felhasználó teljesítményének és állapotának függvényében, így a kihagyott napok vagy új célok nem rontják a fejlődést.  

Az AI alapú motivációs rendszer folyamatosan személyre szabott üzeneteket, emlékeztetőket és statisztikai visszajelzéseket biztosít. Emellett a rendszer integrálja a táplálkozási javaslatokat, amelyek összhangban vannak az edzéstervekkel, figyelembe véve a napi energiaszükségletet és az étkezési preferenciákat. A haladás nyomon követhető grafikonok és kimutatások segítségével, miközben a játékos elemek, mint például a célkitűzések, ranglisták és jelvények, fokozzák a motivációt. Mindez egy felhasználóbarát, React alapú felületen keresztül érhető el, amely reszponzív és könnyen navigálható.

## 4. Funkcionális követelmények

A rendszer fő funkciói a felhasználói élmény maximalizálására és az interakciók zökkenőmentessé tételére összpontosítanak. Az egyik legfontosabb elem az AI-alapú edzésterv generálás, amely a felhasználó profilja és céljai alapján készül, és módosul a teljesítmény vagy a kihagyott edzések függvényében. A táplálkozási tanácsadás szintén AI által generált, és napi illetve heti szinten biztosít személyre szabott étrendet, figyelembe véve az allergiákat, preferenciákat és kalóriacélokat.  

A rendszer haladást követő modulja részletes statisztikákat és grafikonokat nyújt az edzések, teljesítmény és étkezések tekintetében, miközben az AI folyamatosan értékeli a fejlődést és motivációs üzeneteket küld a felhasználónak. Emellett a ranglisták és a célkitűzések segítik a versenyszellem és a motiváció fenntartását. Az AI-vezérelt elemzés a naplózott adatokat feldolgozva szöveges visszajelzéseket ad az edzések hatékonyságáról.

A felhasználói felület React technológiára épül, biztosítva a könnyű kezelhetőséget és a valós idejű adatfrissítést. A navigáció egyszerűen történik a profil, az edzéstervek, az étkezési tervek és a statisztikák között, így a felhasználó mindig naprakész információkhoz juthat.

Összességében ezek a funkciók biztosítják, hogy az alkalmazás személyre szabott, motiváló és könnyen kezelhető legyen minden felhasználó számára.

## 5. Nem funkcionális követelmények
