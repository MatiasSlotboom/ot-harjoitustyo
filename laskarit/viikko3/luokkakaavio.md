```mermaid
classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli

    Ruutu "40" -- "1" Aloitusruutu
    Ruutu "40" --  "1" Vankila
    Ruutu "40" --  "3" Sattuma
    Ruutu "40" --  "3" Yhteismaa
    Ruutu "40" --  "4" Asema
    Ruutu "40" --  "2" Laitos
    Ruutu "40" -- "22" Normaalikatu

    Pelaaja "1" -- "0..22" Normaalikatu
    Normaalikatu "1" -- "0..4" Talo
    Normaalikatu "1" -- "0..1" Hotelli
    
    Pelaaja "1" -- "*" Raha
    Sattuma "1" -- "*" Sattumakortti
    Yhteismaa "1" -- "*" Yhteismaakortti
    Ruutu "1" -- "1" Toiminto
    Sattumakortti "1" -- "1" Toiminto
    Yhteismaakortti "1" -- "1" Toiminto
```