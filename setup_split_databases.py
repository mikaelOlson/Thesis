import psycopg2
sql1 ="""DROP TABLE IF EXISTS trainingdata;
CREATE TABLE trainingdata AS 
SELECT * FROM addresses
WHERE kommun != 'København'
AND kommun != 'Esbjerg'
AND kommun != 'Aarhus'
AND kommun != 'Aalborg'
AND kommun != 'Odense';"""
sql2 = """DROP TABLE IF EXISTS testdata;
CREATE TABLE testdata AS 
SELECT * FROM addresses
WHERE kommun = 'København' OR kommun = 'Esbjerg';"""
sql3 = """DROP TABLE IF EXISTS validationData;
CREATE TABLE validationData AS
SELECT * FROM addresses
WHERE kommun = 'Aarhus' OR kommun = 'Aalborg' OR kommun = 'Odense';"""
conn = psycopg2.connect("host=localhost dbname=postgis user=postgres password=abc123")
curs = conn.cursor()
curs.execute(sql1)
curs.execute(sql2)
curs.execute(sql3)
