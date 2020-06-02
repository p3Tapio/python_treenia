from datetime import datetime
import os
import sqlite3
import http.client

print("------------------------\n")

conn = sqlite3.connect("tk.db")
cursor = conn.cursor()
sql = '''
CREATE TABLE IF NOT EXISTS Paikkakunnat(
    nimi CHAR(50) NOT NULL
) '''
cursor.execute(sql) 

syote = input("Haluatko muuttaa seurattavia paikkakuntia?\r\n")
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

syote = input("Haluatko hakea lämpötilatiedot ilmatieteenlaitokselta?\r\n")
try:
    if syote=='K':
        monta = 0
        for rivi in cursor.execute("SELECT * FROM Paikkakunnat"):
            monta +=1
            x= ''.join(rivi)
            url = "www.ilmatieteenlaitos.fi"
            conn = http.client.HTTPSConnection(url)
            conn.request("GET", f"/saa/{x}/")
            res = conn.getresponse()
            html = str(res.read())
            z = '<td class="temperature-container"> <div class="temperature positive" title="l&#xE4;mp&#xF6;tila '
            index = html.index('<td class="temperature-container"> <div class="temperature positive" title="')
            temp = html[index+len(z):index+len(z)+2]
            temp = temp.replace("&", "")
            if len(x)>7:
                print(f'{x}\t{temp}c')
            else:
                print(f'{x}\t\t{temp}c')
            
    print(f"\nOhjelman suoritus päättyy. Noudettiin {monta} paikkakunnan säätietoa onnistuneesti. Tiedot kirjoitettu lokiin.")
    
    
except:
    print("ei natsaa")


syote = input("Haluatko tarkastaa lokin? (K = kyllä) \r\n")






