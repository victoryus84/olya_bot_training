import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
 
def get_connection():
    try:
        return psycopg2.connect(
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host="OlyaBot-db",
            port=5432,
        )
    except:
        return False