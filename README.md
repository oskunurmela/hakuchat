# Asennus- ja käynnistysohjeet

**1. Virtuaaliympäristö päälle**
Avaa projektin kansio terminaalissa ja luo Python-virtuaaliympäristö:

python3 -m venv .venv
source .venv/bin/activate

**2. Riippuvuudet sisään**

Asenna tarvittavat paketit (Flask, OpenAI ja python-dotenv):

pip install flask openai python-dotenv

**3. API-avaimen asetus**
Jotta kielimalli toimii, tarvitset OpenRouterin API-avaimen. Laita se suoraan terminaalin ympäristömuuttujiin tällä komennolla (korvaa oma avaimesi):

export OPENROUTER_API_KEY="sk-or-v1-sinun-avaimesi-tähän"


**4. Palvelin tulille**
Käynnistä Flask-palvelin komennolla:

python app.py

Sitten vain selain auki ja osoitteeksi: http://127.0.0.1:5000

---

## Miten "Tool Use" -silmukka oikeasti toimii?

1. Ensin kielimallille lähetetään käyttäjän viesti, mutta sen lisäksi sille viedään JSON-muodossa lista työkaluista, joita se saa käyttää (meillä se on `web_search`).
2. Sitten tulee se juju: tekoäly *ei itse* tee mitään verkkohakuja. Jos se tajuaa, että nyt tarvitaan lisätietoa netistä, se pysäyttää vastaamisen ja palauttaa ohjelmalle erikoisviestin (`tool_calls`).
3. Minun koodini nappaa tuon pyynnön kiinni, lukee mitä malli haluaa hakea, ja ajaa ihan normaalin Pythonin `subprocess.run`-komennon, joka tekee sen curl-kutsun.
4. Koodi ottaa Wikipedian palauttaman hakutuloksen, muotoilee sen ja tunkee takaisin mallin viestihistoriaan ikään kuin uutena viestinä (jonka roolina on 'tool').
5. Lopuksi mallia kutsutaan vielä kerran tällä uudella historialla. Nyt se näkee alkuperäisen kysymyksen ja haetut faktat, ja osaa niiden pohjalta muotoilla fiksun vastauksen käyttäjälle.

Laitoin silmukkaan myös 5 kierroksen maksimirajan, ettei koodi jää ikuiseen luuppiin, jos tekoäly sattuisi menemään jotenkin jumiin.

## Reflektio

1. **Missä kohdassa agentti teki virheen tai huonon ratkaisun, ja miten huomasit sen?**
Agentti teki pari virhettä. Ensiksi se yritti alustaa OpenAI-yhteyden ennen kuin .env-tiedosto oli ladattu load_dotenv()-funktiolla, ja lisäksi se käytti väärää ympäristömuuttujan nimeä (OPEN_ROUTER_UUS). Huomasin tämän, kun ohjelma kaatui toistuvasti Missing credentials -virheeseen. Toinen virhe tapahtui käyttöliittymää yhdistäessä: agentin koodi ei käsitellyt virheitä oikein reitityksessä, jolloin selain sai JSONin sijaan HTML-virhesivun ja antoi Unexpected token -virheen. Huomasin nämä lukemalla terminaalin ja selaimen virheilmoituksia.

2. **Minkä osan koodista ymmärrät heikoimmin? Mitä tekisit asialle?**
Heikoimmin ymmärrän selainkäyttöliittymän JavaScriptin (fetch-kutsut) ja Flask-palvelimen välisen tiedonsiirron yksityiskohdat, sekä sen, miten työkalun JSON tarkalleen määritellään API-kutsussa. Voisin parantaa ymmärrystäni lukemalla Flaskin perehtymällä asiaan paremmin ja kokeilemalla kirjoittaa yksinkertaisen fetch-pyynnön kokonaan itse ilman tekoälyä.

3. **Miten agentin käyttö vaikutti oppimiseesi verrattuna siihen, että olisit kirjoittanut koodin itse?**
Agentin käyttö siirsi huomioni koodin kirjoittamisesta koodin lukemiseen ja ohjelman arkkitehtuuriin. Sen sijaan, että olisin jumiutunut syntaksivirheisiin tai puuttuviin sulkeisiin, pystyin keskittymään tietoturvaan (kuten komentoinjektioiden estämiseen ja API-avaimen suojaamiseen) sekä tool use -silmukan logiikkaan. Se opetti myös kriittisyyttä. Agentin tuottamaan koodiin ei voi sokeasti luottaa, vaan sen jokainen tuotos on testattava.

4. **Milloin malli päätti hakea ja milloin ei? Toimiko päätös järkevästi?**
Malli teki päätökset erittäin fiksusti ja loogisesti. Kun kysyin "Mikä on rekursio?", malli ymmärsi, että kyseessä on yleinen ohjelmointikonsepti, ja vastasi suoraan omasta opetusdatastaan ilman hakua. Kun taas annoin syötteen "Etsi linkkejä aiheesta Python asyncio", malli tunnisti heti tarpeen käyttää ulkoista lähdettä ja aktivoi web_search-työkalun saadakseen oikeita, klikattavia linkkejä.
