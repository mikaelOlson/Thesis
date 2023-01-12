import psycopg2

conn = psycopg2.connect('host=localhost dbname=postgis user=postgres password=abc123')
curs = conn.cursor()
sql = """SELECT address, geog, ST_X(geog::geometry), ST_Y(geog::geometry) FROM training_small"""
curs2 = conn.cursor()

curs.execute(sql)
for row in curs.fetchall():
    #rint(row)
    x = row[2]
    y = row[3] #FLOAT
    sql2 = """SELECT address, ST_Distance(geog, ST_GeographyFromText('POINT({})')) AS dist
    FROM addresses WHERE ST_DWithin(geog,ST_GeographyFromText('POINT({})'),1000 )
    ORDER BY dist LIMIT 2""".format(str(x) + " " + str(y), str(x) + " " + str(y))
    curs2.execute(sql2)
    res = curs2.fetchall()
    #print(res[1])
    #input()
    