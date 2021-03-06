from datetime import datetime
import os
import sqlite3
import http.client
import codecs

print("------------------------\n")

conn = sqlite3.connect("tk.db")
cursor = conn.cursor()
sql = '''
CREATE TABLE IF NOT EXISTS Paikkakunnat(
    nimi CHAR(50) NOT NULL
) '''
cursor.execute(sql) 

syote = input("Haluatko muuttaa seurattavia paikkakuntia?\r\n")
id = 0
if syote == 'K':
    sql = 'DELETE FROM Paikkakunnat'
    cursor.execute(sql)
    conn.commit()
    while True:
        syote = input("Minkä paikkakuntien säätä seurataan? (X lopettaa)\r\n")
        sql = f'INSERT INTO Paikkakunnat(nimi) VALUES ("{syote}")'
        if syote=='X':
            break
        cursor.execute(sql)
        conn.commit()
        id +=1

syote = input("Haluatko hakea lämpötilatiedot ilmatieteenlaitokselta?\r\n")
monta = 0
try:
    if syote=='K':
        monta = 0
        for rivi in cursor.execute("SELECT * FROM Paikkakunnat"):

            x= ''.join(rivi)
            x = x.strip()

            if x:
                monta +=1
                x= ''.join(rivi)
                url = "www.ilmatieteenlaitos.fi"
                conn = http.client.HTTPSConnection(url)
                conn.request("GET", f"/saa/{x}/")
                res = conn.getresponse()
                html = str(res.read())

                z = 'class="temperature" data-v-732a7470><th role="rowheader" scope="row" class="offscreen" data-v-732a7470>L\xc3\xa4mp\xc3\xb6tila</th> <td role="cell" title="L\xc3\xa4mp\xc3\xb6tila\xa4mp\xc3\xb6tila  '
                index = html.index('class="temperature" data-v-732a7470><th role="rowheader" scope="row" class="offscreen" data-v-732a7470>')
                temp = html[index+len(z)+13:index+len(z)+16]
                temp = temp.replace("&", "")
                
                if len(x)>7:
                    print(f'{x}\t{temp}c')
                else:
                    print(f'{x}\t\t{temp}c')
    if monta == 0:
        print("Ei haettavia paikkakuntia.")
    else: 
        print(f"\nOhjelman suoritus päättyy. Noudettiin {monta} paikkakunnan säätietoa. Tiedot kirjoitettu lokiin.\r\n")
        date = datetime.now()
        tiedostoon = f"Haettu {monta} paikkakunnan lämpötila \t---\t"+date.strftime("%d/%m/%Y, %H:%M")+" \n"
        with codecs.open("hakutiedot.txt", "a", encoding="utf-8") as file:
            file.write(tiedostoon)
        file.close() 
    
except:
    print(f"\nVirhe tilanne! Paikkakunnan {x} tietojen haku epäonnistui.\r\nOhjelman suoritus keskeytetty.\n")
    date = datetime.now()
    tiedostoon = f"Virhe paikkakunnan {x} haussa \t---\t"+date.strftime("%d/%m/%Y, %H:%M")+" \n"
    with codecs.open("hakutiedot.txt", "a", encoding="utf-8") as file:
        file.write(tiedostoon)
    file.close() 

syote = input("Haluatko tarkastaa lokin tai poistaa sen? (L = lue loki, P = Poista, muut napit lopettaa.) \r\n")
if syote=='L':
    print("--------------------------\n")
    file = codecs.open("hakutiedot.txt", "r",encoding="utf-8")
    for rivi in file:
        print(rivi)
    file.close() 
elif syote=='T':
    os.remove("hakutiedot.txt")


print("--------------------------\r\n\nKiitos käynnistä! \n")




