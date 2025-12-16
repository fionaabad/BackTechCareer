import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DB")

    print("MYSQL_HOST =", host)
    print("MYSQL_PORT =", port)

    if not port:
        raise RuntimeError("MYSQL_PORT no está definido en el .env")

    return mysql.connector.connect(
        host=host,
        port=int(port),   # 👈 aquí ya no rompe
        user=user,
        password=password,
        database=database
    )
