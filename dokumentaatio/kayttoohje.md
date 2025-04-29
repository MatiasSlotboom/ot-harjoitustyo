# Käyttöohje

Lataa projektin viimeisimmän [releasen](https://github.com/SINUN_KAYTTAJA/SINUN_REPO/releases) lähdekoodi valitsemalla _Assets_-osion alta _Source code_. *(Huom: Korvaa yllä oleva linkki oikealla projektisi GitHub-linkillä)*

## Ohjelman käynnistäminen

Ennen ohjelman käynnistämistä, asenna riippuvuudet komennolla:

```bash
poetry install
```

Jos projektissa on tietokannan alustustoimenpiteitä, suorita ne komennolla (tarkista projektikohtainen komento, jos se eroaa):

```bash
poetry run invoke build
```

Nyt ohjelman voi käynnistää komennolla (tarkista projektikohtainen komento, jos se eroaa):

```bash
poetry run invoke start
```
## Treenien Hallinta (Päänäkymä)

Näet listan tallennetuista treeneistäsi ("Saved Workouts"). Listassa näkyy kunkin treenin päivämäärä ja tunniste (ID).

*   **Lisää uusi treeni:** Paina **"Add New Workout"**.
*   **Tallenna uusi treeni:** Paina **"Save Workout"**.
*   **Katso/Muokkaa treeniä:** Valitse treeni listasta ja paina **"View/Edit Selected"** TAI kaksoisklikkaa treeniä listassa.
*   **Poista treeni:** Valitse treeni listasta ja paina **"Delete Selected"**. Vahvista poisto avautuvassa ikkunassa.
*   **Tallenna vaihdetut asiat:** Paina **"Save Workout"**.