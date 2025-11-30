# Cubic subgraph

## Zadání

Program dostane na vstupu neorientovaný graf G = (V, E)
a jeho cílem je nalézt neprázdnou podmnožinu hran F takovou,
že mají všechny vrcholy podgrafu H = (V, F) stupně 0 nebo 3.

## Jak program používat

Program je napsaný v Python 3 a podporuje Glucose 4.2 SAT solver.

Program přijímá přes argument `-i` nebo `--input` cestu k souboru se vstupem.

Přes argument `-v` nebo `--verbosity` lze nastavit, jak moc má být zavolaný SAT solver výřečný.
Tento argument se předává přímo použitému solveru.

Jaký Glucose solver se má použít se nastavuje pomocí argumentu `-s` nebo `--solver`.
Solver se musí nacházet ve stejném adresáři, jako spouštěný program.

Pomocí `-o` nebo `--output` lze nastavit jméno souboru s vygenerovanou DIMACS CNF formulí.

## Formát vstupu a výstupu

Na prvním řádku vstupu přijímá program dvě celá čísla `V`, `E` oddělená mezerou
— a odpovídají počtu vrcholů a hran grafu.

Na dalších `E` řádcích se poté musí nacházet hrany ve formátu
dvou čísel vrcholů oddělených mezerou.
Indexy vrcholů musí být v uzavřeném intervalu od 0 do `V-1`.

Výstup obsahuje výpis ze solveru a seznam hran, které byly vybrány.

## Kódování problému do SAT

Program využívá dva typy proměnných:

1. **Hrany:** proměnné `e_i` odpovídají jednotlivým hranám grafu.
   Proměnná `e_i` je `True` právě tehdy, pokud byla tato hrana zařazena do množiny F.

2. **Pomocné proměnné:** pro každý vrchol vzniká sada proměnných
   `var(i, c)` reprezentující stav počítadla.
   Hodnota `var(i, c)` znamená, že „po zpracování prvních `i` incidentních hran
   má vrchol přesně `c` vybraných hran“.
   Hodnoty `c` nabývají hodnot od 0 do 4 (kde 4 představuje přetečení — počet > 3).

### Princip kódování

Pro každý vrchol `v` kóduji podmínku na stupeň pomocí simulace počítadla, které postupně prochází jednotlivé hrany vrcholu a kontroluje, zda je na konci stupeň 0 nebo 3. To je realizováno implikacemi,
které vynucují, že musí být skutečný stupeň vždy ohodnocen `True`.

Implikace jsou automaticky programem převedeny na odpovídající množinu klauzulí. Využívá se toho, že mají všechny implikace na levé straně několik literárů oddělených pomocí `AND` a na pravé jediný literár.
 
### Typy implikací

Program využívá tři základní formy implikací:

- **Výběr hrany (inkrement počítadla):**

    Pokud je `var(i, c) = True` a hrana byla vybrána, potom je i `var(i+1, c+1) = True`. 

- **Nevýběr hrany (přenos stavu):**

    Pokud je `var(i, c) = True` a hrana nebyla vybrána, potom je i `var(i+1, c) = True`.

- **Zachování přetečení (stupeň musí zůstat navždy větší než 3):**

    Pokud je `var(i, 4) = True`, je i `var(i+1, 4) = True`

### Zbylé klauzule

Program přidává klauzuli obsahující všechny proměnné odpovídající hranám a zajišťuje tak, že musí být vybrána alespoň jedna hrana, tedy že F není prázdná.

Dále přidává klauzule, které povolují, případně zakazují jednotlivé stupně.

### Alternativní kódování

Zvolené počítadlo má pro každý rozlišovaný stupeň jednu proměnnou.
To by ale bylo v případě problému, kde je stupeň větší než 3 velice neefektivní. Dalo by se proto pro větší stupně použít binární počítadlo, kde už jednotlivé proměnné odpovídají jednotlivým cifrám počtu a ne samotným počtům.

## Instance a experimenty

Netriviální splnitelné instance jsem generoval pomocí přiloženého Python skriptu.
Jsou dvou druhů:

### Náhodný graf

Tady jsem nejprve vygeneroval úplný bipartitní graf o dvou paritách se třemi vrcholy v každé, aby byla instance splnitelná, a poté jsem do grafu doplnil náhodně další hrany.

Na řídkém grafu se 3000 vrcholy a 15000 hranami běžel solver 22 sekund.

Úplný graf o 100 vrcholech potřeboval 15 sekund, i přesto, že je řešením každý existující kubický graf o 100 či méně vrcholech a dají se případná řešení generovat velice jednoduše.

Úplný graf o 200 vrcholech mi doběhl až 10 minutách a 40 sekundách.

### Cesta

Tady jsem vygeneroval úplný bipartitní graf o dvou paritách se třemi vrcholy v každé, aby byla instance splnitelná a k němu jsem připojil dlouhou cestu. I přes jednoduchou strukturu grafu stačilo navýšit délku cesty na ~100000 hran a solver potom potřeboval 14 sekund.
