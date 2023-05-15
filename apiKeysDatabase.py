import psycopg2
from psycopg2 import sql
import hashlib
import secrets


class ApiKeysDatabase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def get_api_key(self, email):
        conn = self.connect()
        if conn:
            try:
                cur = conn.cursor()
                query = sql.SQL("SELECT api_key FROM api_keys WHERE email = {}").format(sql.Literal(email))
                cur.execute(query)
                api_key = cur.fetchone()
                if api_key:
                    return api_key[0]
            except psycopg2.Error as e:
                print(f"Error fetching api key: {e}")
            finally:
                conn.close()
        return None

    def create_api_key(self, email):
        conn = self.connect()
        if conn:
            try:
                cur = conn.cursor()
                api_key = generate_api_key(email)
                query = sql.SQL("INSERT INTO api_keys (email, api_key, created_date) VALUES ({}, {}, now()::timestamp)").format(sql.Literal(email), sql.Literal(api_key))
                cur.execute(query, [email, api_key])
                conn.commit()
                return api_key
            except psycopg2.Error as e:
                print(f"Error creating api key: {e}")
                conn.rollback()
            finally:
                conn.close()
        return None


    def get_all_api_keys(self):
        conn = self.connect()
        if conn:
            try:
                cur = conn.cursor()
                query = sql.SQL("SELECT * FROM api_keys")
                cur.execute(query)
                rows = cur.fetchall()
                api_keys = []
                for row in rows:
                    #---> api_key = {'email': row[0], 'api_key': row[1], 'created_date': row[2]}
                    api_keys.append(row[1])
                return api_keys
            except psycopg2.Error as e:
                print(f"Error getting api keys: {e}")
            finally:
                conn.close()
        return None


def generate_api_key(email):
     # Generate a random 16-byte string using a CSPRNG
    random_bytes = secrets.token_bytes(16)
    
    # Concatenate the random bytes and email
    input_bytes = random_bytes + email.encode('utf-8')
    
    # Generate a SHA-256 hash of the input bytes
    hashed_key = hashlib.sha256(input_bytes).digest()
    
    # Encode the hashed key in hexadecimal format
    api_key = hashed_key.hex()
    
    # Return the first 32 characters of the API key
    return api_key[:32]
