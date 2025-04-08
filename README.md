# Ohjelmistotekniikka, harjoitustyö

Harjoitustyössä kehitän yksinkertaisen *Kuntosaliseurantasovelluksen*, perustuen Tkinter kirjastoon joka auttaa käyttäjää **tallentaa**, **vertailla** ja **tutkia** treenejään.

[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
[Tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
[Changelog](dokumentaatio/changelog.md)
[Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)


1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Sovelluksen tietokannan luominen komennolla:

```bash
poetry run invoke build
```
3. Sovellus käynnistyy komennolla:

```bash
poetry run invoke start
```

### Testaaminen

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus-raportti

Testikattavuusraportin voi luoda komennolla:

```bash
poetry run invoke coverage-report
```

Komennon valmistettua _htmlcov_-hakemistosta löytyy html tiedosto jonka voi avata selaimella.