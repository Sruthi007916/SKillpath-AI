import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sruthi&&07",
        database="skillpath_ai"
    )
    return connection

def get_conn():
    return get_db_connection()
