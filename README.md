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
