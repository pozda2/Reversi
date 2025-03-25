# Turnaj v reversi / othello

Poslední přednášku se bude konat turnaj v reversi.

Účast v turnaji je dobrovolná, ale turnaj se bude konat minimálně pro 8 hráčů.

Svůj program je třeba odevzdat přes git nejpozději den před turnajem.

Vítěz turnaje po prezentaci svého algoritmu získá zkoušku.

# Pravidla reversi
https://cs.wikipedia.org/wiki/Othello_(deskov%C3%A1_hra)


# Pravidla turnaje
- Rozlosování do turnajového pavouku bude náhodné.
- Přiřazení barvy kamenů je náhodné (horní má bílé kameny, spodní černé kameny).
- Hraje se na jedno vítězství. Vítěz postupuje v pavouku, poražený končí.
- Na tah je **maximálně 30 vteřin**. Pokud program nestihne vrátit svůj tah, tah propadá a hraje protihráč.
- Pokud program vrátí neplatný tah, hraje protihráč.
- Hra se koná na notebooku. Nepočítejte s nějakým velkým výkonem ;-(

# Technické poznámky
Partii budou hrát vždy dva studentské programy v docker kontejnerech.

Složky reversi_dummy a reversi_student nyní obsahují hloupé implementace (metoda min_max vrací tah, který povede k nejvyššímu skóre na konci tahu).

Vašim úkolem je upravit **reversi_student**.

## State.py
Obsahuje třídu, která implementuje hračovu strategii a hru.
- __init__ konstruktor
- terminal_test() - vrací logickou hodnotu, zda je patrie u konce
- score() - vrácí aktuální skóre stavu hry white_count, black_count
- winner() - 0 remíze, 1 bílý, 2 černý
- next_player() - protihráč
- next_current_player() - protihrač pro procházení stavového prostoru
- possible_actions() - seznam možných tahů
- expand(action) - zahrání tahu, vrací nový stav
- utility() - ohodnocení stavu partie (TODO)
- minmax() - vrací vybraný tah a jeho ohodnocení (TODO)

## main.py
Hlavní program hráčské strategie. Pomocí restového API POST /minmax získá aktuální stav partie a vrací vybraný tah.

Vstupní JSON
```
{
         "gameplan": [
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 2, 0, 0, 0],
             [0, 0, 0, 2, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]
         ],
         "player": 1
     }
```

Výstupní JSON
```
{
  "best_move": [
    7,
    2
  ],
  "rc": 0,
  "message": "Ok"
}
```
rc obsahuje 1 při chybě, message obsahuje zprávu

## requirements.txt
Potřebné python moduly v kontejneru

## Dockerfile
Soubor pro vytvoření docker image

## docker-compose.yaml
Definice docker aplikace

# Spuštění hry
- Nainstalujte si docker.

- V adresáři reversi_dummy spusťte protihráče. 
```
docker compose up
```

- V adresáři reversi_student spusťte svůj program
```
docker compose build
docker compose up
```

Spusťte si partii
```
python reversi.py 
```

Pokud chcete prohodit bílého a černého, tak je třeba spustit programy na jiném portu např. v docker-compose.yaml
```
    ports:
      - "8001:80"
```