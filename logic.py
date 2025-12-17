import psycopg
from cryptography.fernet import Fernet

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

    #Decrypts Fernet encryption
    def login_decrypt(self, en_username, en_password):
        r_username = self.__f.decrypt(en_username)
        r_password = self.__f.decrypt(en_password)
        r_username = r_username.decode()
        r_password = r_password.decode()
        return r_username, r_password
        
    #Validates login credentials by opening database connection 
    def login_check(self, server, db, user, password):
        self.server = server
        self.database = db
        __user, __password = self.login_decrypt(user, password)
        self.__user = __user
        self.__password = __password

        login = psycopg.connect(f'dbname={self.database} user={self.__user} password={self.__password}')
        login.close()

    #Query the database to retrieve rowcount from table
    def row_count(self, tbl):
        with psycopg.connect(f'dbname={self.database} user={self.__user} password={self.__password}') as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT COUNT(*) FROM {tbl}')
                query = cur.fetchall()
                query = query.pop()
                query = query[0]
            return query
    
    #Query the database to retrieve all names from in450b table
    def name_list(self):
        with psycopg.connect(f'dbname={self.database} user={self.__user} password={self.__password}') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT first_name, last_name FROM in450b')
                query = cur.fetchall()
            return query