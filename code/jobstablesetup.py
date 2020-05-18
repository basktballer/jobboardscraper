import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user = "eden",
                                  password = "Ed3nEd3nEd3n",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "jobsdb")

    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE jobs
          (ID SERIAL PRIMARY KEY     NOT NULL,
          TITLE           TEXT    NOT NULL,
          SALARY          TEXT,
          LOCATION        TEXT,
          DESCRIPTION     TEXT    NOT NULL,
          COMPANY         TEXT    NOT NULL,
          URL             TEXT,
          DATEPOSTED      DATE    NOT NULL,
          UNIQUE (TITLE, COMPANY, DATEPOSTED)
          ); '''
    
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")