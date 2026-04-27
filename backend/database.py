import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="soccerpath_db",  
        user="postgres",
        password="password"   
    )
