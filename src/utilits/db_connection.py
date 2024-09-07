import pyodbc


class DBConnection:
    def __init__(self, database):
        with pyodbc.connect(f'''Driver=SQLite3 ODBC Driver;
                                          Database={database}''', autocommit=True) as cnxn:
            self.cursor = cnxn.cursor()
            self.columns_news = """id INTEGER PRIMARY KEY AUTOINCREMENT,
                                input_text TEXT,
                                city TEXT,
                                date TEXT,
                                UNIQUE (input_text, city)"""
            self.columns_private_ad = """id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    input_text TEXT,
                                    expir_date TEXT,
                                    days_left TEXT,
                                    UNIQUE (input_text, expir_date)"""
            self.columns_currency_conv = """id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    currency_from TEXT,
                                    currency_to TEXT,
                                    rate TEXT, 
                                    city TEXT,
                                    date TEXT,
                                    UNIQUE (currency_from, currency_to, rate, city)"""


    def db_create(self, table_name, columns_with_types):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                {columns_with_types})''')

    def db_insert(self, table_name, columns, insert_values):
        try:
            self.cursor.execute(f"""INSERT INTO {table_name} ({columns})
                           VALUES ({insert_values})""")
            print(f"Row inserted successfully into {table_name} table")
        except pyodbc.Error as e:
            if 'UNIQUE constraint failed' in str(e):
                print("Error: Unique constraint violation - Record already exists")
            else:
                raise e

    def db_select(self, table_name, columns='*'):
        self.cursor.execute(f"SELECT {columns} FROM {table_name}")
        rows = self.cursor.fetchall()
        return rows



