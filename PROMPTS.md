# Agentin ohjauksessa käytetyt promptit

### 1. Suunnitelma (Plan-agentti)
**Prompti:**
> "Lue weather.py. Suunnittele Python-sovellus, jossa on Flask-palvelin, yksinkertainen index.html-chat ja tool use -työkalu web_search, joka hakee curlilla Wikipedian haku-API:sta. Käytä samaa openai-kirjastoa, OpenRouteria ja mallia kuin weather.py:ssä. Älä kirjoita vielä koodia. Listaa tiedostot, funktiot ja toteutusjärjestys pieninä testattavina askelina. Huomioi AGENTS.md:n tietoturvasäännöt."

**Miten agentti suoriutui:**
Agentti teki aika hyvän ja selkeän suunnitelman. Se tajusi suoraan AGENTS.md:n turvasäännöt (subprocess listana ja curlin aikaraja). Ainoa moka oli se, että agentti nappasi mallitiedostosta väärän ympäristömuuttujan nimen, joka piti korjata myöhemmin.

### 2. Hakufunktion teko (Build-agentti)
**Prompti:**
> "Suunnitelma on erinomainen! Aloitetaan vaiheesta 2. Toteuta web_search.py, jossa on funktio web_search(query). Käytä subprocess.run-kutsua listamuodossa ilman shell=True-asetusta. URL-enkoodaa hakusana ja aseta curlille 10 sekunnin aikaraja. Palauta Wikipedia-haun tulokset listana sanakirjoja {title, url}. Lisää tiedoston loppuun __main__-lohko komentorivitestausta varten."

**Miten agentti suoriutui:**
Tämä meni purkkiin ihan ykkösellä. Agentti koodasi turvallisen hakufunktion ja osasi nätisti parsia Wikipedian palauttaman JSON-datan Pythonin listaksi.

### 3. Tool use -silmukka (Build-agentti)
**Prompti:**
> "Hienoa, web_search.py toimii! Siirrytään vaiheeseen 3. Tee chat_core.py, jossa on funktio chat(messages). Määrittele web_search-työkalu JSON-skeemana tools-listassa. Toteuta tool use -silmukka: kutsu mallia, suorita työkalukutsut ja kutsu mallia uudelleen, kunnes tulee tekstivastaus (max 5 kierrosta)."

**Miten agentti suoriutui:**
Logiikka oli muuten oikein, mutta tässä tuli ongelmia ympäristömuuttujien kanssa. Koodi kaatui `Missing credentials` -virheeseen, koska agentti ei ladannut avainta oikein ennen clientin luomista.

### 4. Ympäristömuuttujien bugin korjaus (Build-agentti)
**Prompti:**
> "Saan yhä 'Missing credentials' -virheen, koska os.environ.get('OPENROUTER_API_KEY') palauttaa None. Syy on se, että OpenAI-client luodaan ennen kuin .env-tiedosto on ehditty lukea. Korjaa chat_core.py rakenne tällaiseksi: 1. Kaikki importit ylös. 2. Heti importtien jälkeen kutsu: load_dotenv(). 3. VASTA NÄIDEN JÄLKEEN luo muuttuja client."

**Miten agentti suoriutui:**
Kun annoin näin tarkan ohjeen, agentti sai tiedoston rakenteen korjattua. Tämän jälkeen testiajo komentoriviltä onnistui heti.

### 5. Flask ja frontend (Build-agentti)
**Prompti:**
> "Siirrytään vaiheeseen 4. Tee app.py (Flask) ja käyttöliittymä templates/index.html. app.py tarjoaa index.html:n ja POST /api/chat -rajapinnan. index.html tehdään ilman ulkoisia kirjastoja. Tärkeä näkyvyysvaatimus: UI:n pitää näyttää erillisenä, visuaalisena huomiona, jos malli käytti hakua ja millä hakusanalla. Vastauksen linkkien pitää olla klikattavia."

**Miten agentti suoriutui:**
Käyttöliittymästä tuli ihan siisti ja se teki sen mitä piti. Mutta app.py:n reitityksessä oli taas pieni fiba: selain sai virhetilanteissa Flaskilta HTML-virhesivun eikä JSONia, mistä seurasi kummallisia erroreita selaimen konsolissa.
