import csv
import json
import time
f = open('adresser.jsonl','r')
header = ['betegnelse','adresseringsnavn','husnr','supplerendebynavn','etage','door','postnr','postnrnavn','point']
count = 1
with open('file2.csv','w',encoding='UTF8',newline='') as out:
    writer = csv.writer(out)
    writer.writerow(header)
    start = time.time()
    for line in f: 
        j = json.loads(line)
        door = j['dør']
        etage = j['etage']
        supplerendebynavn = j['adgangsadresse']['supplerendebynavn']
        betegnelse = j['adressebetegnelse']
        adresseringsnavn = j['adgangsadresse']['vejstykke']['adresseringsnavn']
        postnr = j['adgangsadresse']['postnummer']['nr']
        postnavn = j['adgangsadresse']['postnummer']['navn']
        point = j['adgangsadresse']['adgangspunkt']['koordinater']
        point = (point[1],point[0])
        husnr = j['adgangsadresse']['husnr']
        writer.writerow([betegnelse,adresseringsnavn,husnr,supplerendebynavn,etage,door,postnr,postnavn,point])
        print(count)
        count = count + 1
    print("total amount of addresses: ",count)
    end = time.time()
    print("\n Elapsed time: ", end-start)
