## Copilot Agent-mode raportti

#### Käytössä oli VSCoden agent-mode, mikä hyödynsi Claude Haiku 4.5:sta

Agentti päätyi hyvin toimivaan ja yksinkertaiseen ratkaisuun. Se käytti toteutuksessa pelkästään Flaskia ja tuotti erittäin luettavaa ja ymmärrettävää koodia. Se ymmärsi edeltävän koodin erittäin hyvin ja kolmannen botin lisääminen onnistui erittäin helposti, minkä toteutus on samankaltainen kuin muiden bottien ja pvp-moden.

Varmistuin, että ratkaisu toimii käymällä läpi agentin ratkaisua tarkastelemalla sen tuottamaa koodia ja testaamalla itse sovellusta selaimessa. Olen 99 % varma, että ratkaisu toimii oikein (en täysin tiedä miten kolmas botti toimii).

Annoin agentille, joka stepin alussa yksityiskohtaisen tehtävä-kuvauksen, minkä jälkeen agentti selvisi tehtävästä hyvin. Jouduin kuitenkin välillä huomauttaumaan, että agentti päivittäisi kaikkia tiedostoja (usein README:t ja pienet muuttuja muutokset unohtuivat).

Agentin luomat testit olivat selkokielisä ja hyvin kattavia. Kuitenkin kaikki testit ovat suoria API kutsuja, eikä se luonut Robot-frameworkin tapaisia selaimessa suoritettavia testejä.

Agentin luoma koodi oli erittäin ymmärettävää. Myös uusien bottien lisääminen luotuun koodiin on hyvin helppoa. Kolmannen botin lisääminen lisäsi varsinaiseen sovellukseen vain muutaman rivin uutta koodia.

Agentti muutti omaa koodiani vain lisäämällä tarvittavat osat liittyen kolmanteen bottiin, koskien vain tarvittavia osia (muutokset tiedostoihin luo_peli.py ja index.py).

Opin sen että suoraan editoriin integroitu agent-mode on erittäin nopea ja tehokas koodauksessa, erityisesti verrattuna kielimallien käyttöön selaimessa. Sain viikon homman tehtyä tunnissa. Se on myös erittäin hyvä koodin muokkauksessa sovellukseen sopivaksi. Esimerkiksi agentti integroi sen Internetistä löytämän KPS-algoritmin mallikkaasti olemassa olevaan koodiin. Opin paljon agenttien käytöstä, mutta en varsinaisesta ohjelmoinnista. Agentit ovat hyviä featureiden shippauksessa, mutta mielestäni manuaalinen koodaaminen on opettavaisempaa. Agentteja on lisäksi mukavaa käyttää boilerplaten ja testien koodaamiseen (vihaan näiden käsin koodaamista).