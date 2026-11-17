# PROMPTS.md

Tässä tiedostossa on koottuna tärkeimmät käyttäjän antamat promptit tämän istunnon aikana ja lyhyt kuvaus siitä, miten kuhunkin vastattiin.

## 1. JSON-virheen korjaus frontendin ja palvelimen välillä

**Prompt:** Käyttäjä ilmoitti selaimen konsolissa ilmenevästä virheestä: `SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON`. Syynä oli, että frontend odotti JSON-vastausta, mutta palvelin palautti HTML:ää (esim. Flaskin oletusvirhesivu tai väärä reitti/index.html). Käyttäjä pyysi tekemään kolme korjausta:

- Varmistaa, että `app.py`:n reitti on täsmälleen `@app.route('/api/chat', methods=['POST'])` ja että se palauttaa vastauksen aina Flaskin `jsonify`-funktiolla (esim. `return jsonify({"response": vastaus})`).
- Kääriä `app.py`:n `/api/chat`-reitin logiikka try-except-lohkoon. Jos `chat_core`-kutsussa tapahtuu virhe, palauttaa sekin JSON-muodossa: `return jsonify({"error": str(e)}), 500`. Älä anna Flaskin palauttaa HTML-virhesivua.
- Varmistaa, että `index.html`:n fetch-kutsu osoittaa täsmälleen osoitteeseen `/api/chat` ja käsittelee vastauksen oikein (`res.json()`).

**Vastaus:** Luin `app.py`, `templates/index.html` ja `chat_core.py`. Huomasin, että reitti `/api/chat` oli jo oikein ja vastaus käytettiin jo `jsonify`-funktiolla. Samoin `index.html`:n fetch osoitti jo `/api/chat` ja käytti `res.json():a`. Ainoa puuttuva oli try-except-kääritys `chat_core.chat`-kutsun ympärille, jonka lisäsin. Virhetilanteessa reitti palauttaa nyt `jsonify({"error": str(e)}), 500` Flaskin HTML-virhesivun sijaan. Tarkistin tiedoston syntaksin `python3 -c "import ast; ..."` -komennolla.

## 2. Dokumentaatio: README.md ja PROMPTS.md

**Prompt:** Käyttäjä pyysi kirjoittamaan kaksi tiedostoa:

- `README.md`, jossa on a) asennus- ja käynnistysohjeet (miten `.venv` tehdään, riippuvuudet asennetaan, avain asetetaan exportilla ja `app.py` käynnistetään) sekä b) selitys omin sanoin suomeksi siitä, miten `chat_core.py`:n tool use -silmukka toimii askel askeleelta. Tiedoston loppuun tuli jättää otsikko "Reflektio", johon käyttäjä kirjoittaa itse myöhemmin vastaukset.
- `PROMPTS.md`, johon kerätään lista tärkeimmistä prompteista, jotka käyttäjä antoi istunnon aikana, ja lyhyt huomio siitä, miten vastasi niihin.

**Vastaus:** Kirjoitin molemmat tiedostot. `README.md` sisältää vaiheittaiset asennusohjeet virtuaaliympäristön luomisesta, riippuvuuksien asentamisesta, API-avaimen asettamisesta ja sovelluksen käynnistyksestä, sekä suomenkielisen askel askeleelta -selityksen `chat_core.py`:n tool use -silmukasta ja lopussa otsikon "Reflektio". `PROMPTS.md` sisältää yllä olevan listauksen istunnon prompteista ja vastauksista.
