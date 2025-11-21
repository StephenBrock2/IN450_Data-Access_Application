import psycopg

# Business Layer
class Logic():
    #Validates login credentials by opening database connection 
    def login_check(self, server, db, user, password):
        self.server = server
        self.database = db
        self.user = user
        self.password = password

        login = psycopg.connect(f'dbname={self.database} user={self.user} password={self.password}')
        login.close()

    #Query the database to retrieve rowcount from table
    def row_count(self, tbl):
        with psycopg.connect(f'dbname={self.database} user={self.user} password={self.password}') as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT COUNT(*) FROM {tbl}')
                query = cur.fetchall()
                query = query.pop()
                query = query[0]
            return query
    
    #Query the database to retrieve all names from in450b table
    def name_list(self):
        with psycopg.connect(f'dbname={self.database} user={self.user} password={self.password}') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT first_name, last_name FROM in450b')
                query = cur.fetchall()
            return query