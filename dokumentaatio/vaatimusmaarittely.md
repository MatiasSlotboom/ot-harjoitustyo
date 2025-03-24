# Vaatimusmäärittely

## Sovelluksen tarkoitus

Kuntosaliseurantasovelluksen avulla käyttäjä voi seurata kuntosaliharjoituksiaan. Sovellus tallentaa tiedot harjoituksista (liikkeet, setit, toistot, painot, muistiinpanot ja ajankohta) tietokantaan, ja mahdollistaa näiden tietojen tarkastelun ja muokkaamisen. Kaikki tiedot tallennetaan paikallisesti, eikä ole käyttäjätilejä.

## Käyttöliittymäluonnos

Sovellus voisi koostua esimerkiksi seuraavista näkymistä (tarkentuu suunnittelun edetessä):

1.  **Treeninäkymä:** Listaa käyttäjän aiemmat treenit, järjestettynä esim. päivämäärän mukaan.
2.  **Treenin lisäys/muokkausnäkymä:** Lomake, jolla syötetään treenin tiedot (liikkeet, setit, toistot, painot, muistiinpanot, päivämäärä/aika).
3.  **Treenin tarkastelunäkymä:** Näyttää valitun treenin kaikki tiedot. Mahdollisuus siirtyä muokkaustilaan.

## Tarjottava toiminnallisuus

-   Käyttäjä näkee listan aiemmista treeneistään (esim. päivämäärän mukaan järjestettynä kalenteri-tapaisesti).
-   Käyttäjä voi lisätä uuden treenin. Treenin lisäämisen yhteydessä:
    -   Käyttäjä voi lisätä yhden tai useamman liikkeen.
    -   Jokaiselle liikkeelle määritellään:
        -   Liikkeen nimi (esim. "Penkkipunnerrus").
        -   Settien määrä.
        -   Jokaiselle setille: toistojen määrä ja käytetty paino.
        -   Vapaamuotoinen muistiinpano (esim. "Kevyt sarja (palautumassa)").
    -   Treenille asetetaan päivämäärä ja kellonaika (oletuksena treenin luontihetki, mutta käyttäjän muokattavissa).
-   Käyttäjä voi tarkastella yksittäisen treenin tietoja.
-   Käyttäjä voi muokata olemassa olevan treenin tietoja.
-   Käyttäjä voi poistaa treenin.

## Jatkokehitysideoita

Järjestelmää voidaan täydentää esim. seuraavilla ominaisuuksilla:

-   **Tilastot:** Näytetään käyttäjälle tilastoja treeneistä (esim. kehitys tietyissä liikkeissä, treenimäärät, suosituimmat liikkeet).
-   **Liikekirjasto:**  Valmis kirjasto yleisimmistä liikkeistä, josta käyttäjä voi valita liikkeitä treeneihinsä.  Mahdollisuus lisätä omia liikkeitä.
-   **Haku:** Mahdollisuus hakea treenejä esim. päivämäärän, liikkeen tai muistiinpanon perusteella.
-   **Treeniohjelmat:** Mahdollisuus luoda ja tallentaa valmiita treeniohjelmia, joita voi sitten käyttää treenien pohjana.
-   **Yhden toiston maksimin (1RM) arvion laskenta ja seuranta:** Mahdollisuus laskea ja seurata arvioitua yhden toiston maksimia eri liikkeissä.
-   **Graafiset esitykset:** Treenidatan visualisointi kaavioiden avulla (esim. painojen kehitys ajan mukaan).
-   **Mobiilisovellus:** Tällähetkellä vaatimukset ovat työpöytäsovellukselle, mutta mobiilisovelluksella tuotaisiin lisäarvoa.
-   **Tietojen tuonti ja vienti:** Mahdollisuus tuoda ja viedä treenitietoja esim. CSV- tai JSON-muodossa.