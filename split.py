import json
import csv
import psycopg2
import pandas as pd
import os
from tqdm import tqdm

def json_to_dict(dict_list, json_file):
    

    for line in json_file:


        x = json.loads(line)
        
        entry={}
        
        entry['address'] = x['adressebetegnelse']

        entry['street_name']=x['adgangsadresse']['vejstykke']['adresseringsnavn']
        entry['house_number']=x['adgangsadresse']['husnr']
        entry['floor'] = x['etage']
        entry['door']=x['dør']
        entry['additional_city_name'] = x['adgangsadresse']['supplerendebynavn']
        entry['post_number']=x['adgangsadresse']['postnummer']['nr']
        entry['postnavn'] = x['adgangsadresse']['postnummer']['navn']
        entry['kommun'] = x['adgangsadresse']['kommune']['navn']

        long = x['adgangsadresse']['adgangspunkt']['koordinater'] [0]
        lat = x['adgangsadresse']['adgangspunkt']['koordinater'] [1] 

        

        point = "POINT(" + str(long) + " " + str(lat) + ")"

        entry['geog'] = point
        
        for k in entry.keys():
            if not entry[k]:
                entry [k] = 'null'


        dict_list.append(entry)

    return dict_list

def list_to_csv(dict_list):
    
    df = pd.DataFrame(dict_list)
    df.drop_duplicates(subset = 'address', inplace=True)
    df.to_csv('addr.csv', header=False, index=False, encoding='utf-8')



def files_to_dict(path, dict_list):
    files = []
    for file in os.scandir(path):
        files.append(file)
    
    for file in tqdm(files):

        json_file = open(file, 'r', encoding='utf-8')
        data = json_to_dict(dict_list, json_file)
    return data
    

data = []

path = r'split_data'

fil = open('adresser.jsonl','r',encoding='utf-8')
data = json_to_dict(data, fil)

list_to_csv(data)


def connect_to_database():
    conn = None
    try:
        conn = psycopg2.connect("host=localhost dbname=postgis user=postgres password=abc123")
        return conn
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False


conn = connect_to_database()

create_table_sql = ("""

    DROP TABLE IF EXISTS addresses;
    CREATE TABLE addresses(
        address text PRIMARY KEY,
        street_name text,
        house_number text,
        floor text,
        door text,
        additional_city_name text,
        post_number integer,
        postnavn text,
        kommun text,
        geog geography(Point)
    );
""")

with conn:

    with conn.cursor() as curs:
        curs.execute(create_table_sql)



copy_sql = """
    COPY addresses FROM STDIN WITH CSV HEADER DELIMITER AS ',';
"""


f = open(r'addr.csv', 'r', encoding='utf-8')
with conn:
    with conn.cursor() as cur:
        conn.set_client_encoding('UTF8')
        cur.copy_expert(copy_sql, f)

f.close()