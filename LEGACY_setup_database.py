import json
import sqlite3
#from sqlite3 import error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def parse_data(conn):
	#Parses data from file to SQL database
	f = open("addresses.json")
	data = json.load(f)
	for x in data['features']:
		y = x['properties']
		vejnavn = y['vejnavn']
		husnr = y['husnr']
		etage = y['etage']
		dor = y['dør']
		postnr = y['postnr']
		postnrnavn = y['postnrnavn']
		bredd = y['wgs84koordinat_bredde']#latitude?
		lengd = y['wgs84koordinat_længde']#longitude?
		data = (vejnavn, husnr, etage, dor, postnr, postnrnavn, bredd, lengd)
		insert_query(data,conn)

		#Insert into sql
def insert_query(data, conn):
	sql = '''INSERT INTO geodata(road, house_number, floor, door, postcode, postort, coord_x, coord_y) VALUES (?,?,?,?,?,?,?,?)'''
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def main():
	conn = create_connection('database.db')
	sql_create_tables = """CREATE TABLE IF NOT EXISTS geodata (
							id integer PRIMARY KEY,
							road text NOT NULL,
							house_number integer NOT NULL,
							floor VARCHAR,
							door VARCHAR,
							postcode VARCHAR,
							postort text,
							coord_x DOUBLE,
							coord_y DOUBLE)"""

	if conn is not None: #connection worked
	#DropTables, createtables and then input data
		create_table(conn, sql_create_tables)
		parse_data(conn)

	else:
		print("Could not establish connection to database.")

if __name__ == '__main__':
    main()
