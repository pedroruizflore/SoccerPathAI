import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="soccerpath_db",
        user="pedrohenrique",
        password="" 
    )
    return conn
