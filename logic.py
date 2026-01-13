import psycopg
from cryptography.fernet import Fernet

VALID_TABLES = ['in450a', 'in450b', 'in450c']

# Business Layer
class Logic():
    def __init__(self):
        self.server_list = ['', 'PostgreSQL']
        self.db_list = ['', 'IN450DB']

        __key = Fernet.generate_key()
        self.__f = Fernet(__key)

    #Encrypts username and password entry using Fernet
    def login_encrypt(self, r_username, r_password):
        r_username = r_username.encode()
        r_password = r_password.encode()
        en_username = self.__f.encrypt(r_username)
        en_password = self.__f.encrypt(r_password)
        return en_username, en_password

    #Decrypts credential encryption
    def cred_decrypt(self, en_cred):
        r_cred = self.__f.decrypt(en_cred)
        r_cred = r_cred.decode()
        return r_cred
        
    #Validates login credentials by opening database connection 
    def login_check(self, server, db, user, password):
        self.server = server
        self.database = db
        self.__user = user
        self.__password = password

        login = psycopg.connect(f'dbname={self.database} user={self.cred_decrypt(self.__user)} password={self.cred_decrypt(self.__password)}')
        login.close()

    #Query the database to retrieve rowcount from table
    def row_count(self, tbl):
        tbl = VALID_TABLES[tbl]
        with psycopg.connect(f'dbname={self.database} user={self.cred_decrypt(self.__user)} password={self.cred_decrypt(self.__password)}') as conn:
            with conn.cursor() as cur:
                if tbl == 'in450a':
                    cur.execute(f'SELECT GetRowsTableA();')
                elif tbl == 'in450c':
                    cur.execute(f'SELECT GetRowsTableC();')
                query = cur.fetchall()
                query = query.pop()
                query = query[0]
            return query
    
    #Query the database to retrieve all names from in450b table
    def name_list(self):
        with psycopg.connect(f'dbname={self.database} user={self.cred_decrypt(self.__user)} password={self.cred_decrypt(self.__password)}') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM NameListTableB();')
                query = cur.fetchall()
            return query