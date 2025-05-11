# Ohjelmistotekniikka, harjoitustyö

Harjoitustyössä kehitän yksinkertaisen *Kuntosaliseurantasovelluksen*, perustuen Tkinter kirjastoon joka auttaa käyttäjää **tallentaa**, **vertailla** ja **tutkia** treenejään.
Uusin julkaistu versio löytyy [täältä](https://github.com/MatiasSlotboom/ot-harjoitustyo/releases/latest).


[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
[Tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
[Changelog](dokumentaatio/changelog.md)
[Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)
[Kayttöohje](dokumentaatio/kayttoohje.md)


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

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät formatointitarkastus voi suorittaa komennolla:

```bash
poetry run invoke lint
```

Release viikko 5: [Viikko 5](https://github.com/MatiasSlotboom/ot-harjoitustyo/releases/tag/Viikko5)
Release viikko 6: [Viikko 6](https://github.com/MatiasSlotboom/ot-harjoitustyo/releases/tag/Viikko6)