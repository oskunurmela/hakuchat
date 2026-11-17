# Hakuchat

Yksitiedostoinen Python-sovellus, joka kutsuu OpenRouteria (OpenAI-yhteensopiva asiakas) sää- ja hakutoiminnoilla.

## Asennus ja käynnistäminen

1. Luo virtuaaliympäristö (.venv):

```bash
python -m venv .venv
```

2. Aktivoi virtuaaliympäristö:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

3. Asenna riippuvuudet (repo ei sisällä requirements.txt):

```bash
pip install openai python-dotenv flask
```

4. Aseta API-avain ympäristömuuttujaan. `weather.py` lukee muuttujan `OPEN_ROUTER_UUS`, kun taas `api.env` määrittelee `OPENROUTER_API_KEY`. Aseta ainakin se, jota sovelluksesi käyttää:

```bash
export OPEN_ROUTER_UUS="sk-or-..."
# tai
export OPENROUTER_API_KEY="sk-or-..."
```

Voit myös luoda `.env`-tiedoston (gitignore:ssa) ja ladata sen.

5. Käynnistä sovellus:

```bash
python app.py
```

Sovellus käynnistyy osoitteeseen `http://127.0.0.1:5000`.

### Huomautus ympäristömuuttujista

`api.env`-tiedosto sisältää `OPENROUTER_API_KEY`, mutta `weather.py` lukee nimenomaan `OPEN_ROUTER_UUS`. Ne eivät täsmää, josta voi seurata virhe. Aseta oikea muuttuja shelliin tai `.env`-tiedostoon ennen käynnistystä.

## Miten chat_core.py:n tool use -silmukka toimii

`chat_core.py` toteuttaa niin sanotun työkalukutsusilmukan (tool use / function calling), jossa kielimalli voi itse päättää, tarvitseeko se ulkoista hakua vastauksen tuottamiseen. Se toimii seuraavasti askel askeleelta:

1. **Alustus**: Funktio `chat(messages)` saa syötteenä listan viestisanakkoja (esim. käyttäjän viesti). Se kopioi viestilistan omaksi muuttujakseen `current_messages` ja alustaa seurantamuuttujat `search_used` ja `search_query`.

2. **Mallille lähetys**: Silmukka toistuu enintään `MAX_ROUNDS` (oletus 5) kertaa. Jokaisella kierroksella se kutsuu OpenAI-yhteensopivaa rajapintaa (`client.chat.completions.create`) annetuilla viesteillä ja antaa mukana työkalumäärittelyn `web_search_tool`. Työkalu kuvaa Suomen Wikipedia -haun, joka ottaa vastaan yhden merkkijonoparametrin `query`.

3. **Vastaanotto ja tarkistus**: Mallilta saadaan vastaus. Tarkistetaan, sisältääkö vastaus työkalukutsuja (`message.tool_calls`). Jos työkalukutsuja ei ole, malli on valmis vastaamaan suoraan, ja funktio palauttaa vastauksen sanakirjana avaimilla `answer`, `search_used` ja `search_query`.

4. **Työkalukutsun käsittely**: Jos malli pyytää työkalun käyttöä:
   - Vastausviesti lisätään viestilistaan (`current_messages.append(message)`).
   - Käydään läpi jokainen pyydetty työkalukutsu. Jos työkalun nimi on `web_search`, puretaan sen argumentit JSON-muodosta ja luetaan `query`-parametri.
   - Suoritetaan varsinainen haku kutsumalla `web_search.web_search(query)`.
   - Hakutulokset lisätään viestilistaan "tool"-tyyppisenä viestinä, jossa on mukana työkalukutsun ID (`tool_call_id`) ja tulos JSON-merkkijonona. Tämä kertoo mallille, mitä haku palautti.

5. **Seuraava kierros**: Silmukka jatkuu seuraavalta kierrokselta. Mallille toimitetaan nyt päivitetty viestilista, joka sisältää sekä alkuperäisen pyynnön että työkalun tuottamat tulokset. Malli voi tässä vaiheessa joko pyytää lisää haukia tai lopettaa ja antaa lopullisen vastauksen.

6. **Lopetus**: Jos enimmäiskierrosmäärä saavutetaan ilman lopullista vastausta, palautetaan oletusviesti "(Vastaus ei valmis enimmäiskierrosten jälkeen.)".

Tällä tavalla malli voi hakea lisätietoa verkosta tarvittaessa ja rakentaa vastauksen haettujen tietojen perusteella, eikä sen tarvitse luottaa pelkästään omaan koulutustietoonsa.

## Reflektio

1. **Missä kohdassa agentti teki virheen tai huonon ratkaisun, ja miten huomasit sen?**
Agentti teki pari virhettä. Ensiksi se yritti alustaa OpenAI-yhteyden ennen kuin .env-tiedosto oli ladattu load_dotenv()-funktiolla, ja lisäksi se käytti väärää ympäristömuuttujan nimeä (OPEN_ROUTER_UUS). Huomasin tämän, kun ohjelma kaatui toistuvasti Missing credentials -virheeseen. Toinen virhe tapahtui käyttöliittymää yhdistäessä: agentin koodi ei käsitellyt virheitä oikein reitityksessä, jolloin selain sai JSONin sijaan HTML-virhesivun ja antoi Unexpected token -virheen. Huomasin nämä lukemalla terminaalin ja selaimen virheilmoituksia.

2. **Minkä osan koodista ymmärrät heikoimmin? Mitä tekisit asialle?**
Heikoimmin ymmärrän selainkäyttöliittymän JavaScriptin (fetch-kutsut) ja Flask-palvelimen välisen tiedonsiirron yksityiskohdat, sekä sen, miten työkalun JSON tarkalleen määritellään API-kutsussa. Voisin parantaa ymmärrystäni lukemalla Flaskin perehtymällä asiaan paremmin ja kokeilemalla kirjoittaa yksinkertaisen fetch-pyynnön kokonaan itse ilman tekoälyä.

3. **Miten agentin käyttö vaikutti oppimiseesi verrattuna siihen, että olisit kirjoittanut koodin itse?**
Agentin käyttö siirsi huomioni koodin kirjoittamisesta koodin lukemiseen ja ohjelman arkkitehtuuriin. Sen sijaan, että olisin jumiutunut syntaksivirheisiin tai puuttuviin sulkeisiin, pystyin keskittymään tietoturvaan (kuten komentoinjektioiden estämiseen ja API-avaimen suojaamiseen) sekä tool use -silmukan logiikkaan. Se opetti myös kriittisyyttä. Agentin tuottamaan koodiin ei voi sokeasti luottaa, vaan sen jokainen tuotos on testattava.

4. **Milloin malli päätti hakea ja milloin ei? Toimiko päätös järkevästi?**
Malli teki päätökset erittäin fiksusti ja loogisesti. Kun kysyin "Mikä on rekursio?", malli ymmärsi, että kyseessä on yleinen ohjelmointikonsepti, ja vastasi suoraan omasta opetusdatastaan ilman hakua. Kun taas annoin syötteen "Etsi linkkejä aiheesta Python asyncio", malli tunnisti heti tarpeen käyttää ulkoista lähdettä ja aktivoi web_search-työkalun saadakseen oikeita, klikattavia linkkejä.
