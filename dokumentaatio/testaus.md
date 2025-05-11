# Testausdokumentti

Ohjelmaa on testattu sekä automatisoiduin yksikkö- ja integraatiotestein unittestilla sekä manuaalisesti tapahtunein järjestelmätason testein.

## Sovelluslogiikka

Sovelluslogiikasta vastaavia `WorkoutService`, `ExerciseService` ja `SetService` -luokkia testataan yksikkötesteillä. Näille luokille injektoidaan riippuvuuksiksi repositorio-oliot, jotka tallentavat tietoa tietokantaan. Testit varmistavat, että palveluluokat toimivat odotetusti ja käsittelevät tietokantaa oikein.

## Repositorio-luokat

Repositorio-luokkia `WorkoutRepository`, `ExerciseRepository` ja `SetRepository` testataan erikseen. Testit varmistavat, että tietokantakyselyt toimivat oikein ja että tietokannan tila vastaa odotuksia eri operaatioiden jälkeen.

## Testauskattavuus

Käyttöliittymäkerrosta lukuun ottamatta sovelluksen testauksen haarautumakattavuus on korkea. Testit kattavat sovelluslogiikan ja tietokantakerroksen toiminnallisuudet.

## Järjestelmätestaus

Sovelluksen järjestelmätestaus on suoritettu manuaalisesti.

### Asennus ja konfigurointi

Sovellus on haettu ja sitä on testattu [käyttöohjeen](./kayttoohje.md) kuvaamalla tavalla sekä macOS- että Linux-ympäristöissä. Testauksessa on käytetty eri konfiguraatioita _.env_-tiedoston kautta.

Sovellusta on testattu sekä tilanteissa, joissa tietokantatiedosto on ollut olemassa, että tilanteissa, joissa sovellus on luonut uuden tietokannan.

### Toiminnallisuudet

Kaikki [vaatimusmäärittelyn](./vaatimusmaarittely.md) ja [käyttöohjeen](./kayttoohje.md) listaamat toiminnallisuudet on käyty läpi. Syötekentät on täytetty myös virheellisillä arvoilla, kuten tyhjillä tai väärän tyyppisillä syötteillä, ja varmistettu, että sovellus käsittelee ne oikein.

## Sovellukseen jääneet laatuongelmat

Sovellus ei anna tällä hetkellä järkeviä virheilmoituksia seuraavissa tilanteissa:

- Konfiguraation määrittelemiin tiedostoihin ei ole luku- tai kirjoitusoikeuksia.
- SQLite-tietokantaa ei ole alustettu, eli `poetry run invoke build` -komentoa ei ole suoritettu.
