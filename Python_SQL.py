''' You may need to change your localhost, root, databases'''
from getpass import getpass
import mysql.connector

class Database():
    '''Making some database operations.'''
    database_choice = {
        "1": "crypto",
        "2": "schooldb",
        "3": "mydatabase",
        "4": "sys"
    }

    def choices(self):
        '''Takes database choice from users decision. Databases are under class section.'''
        print("Welcome to database operations")
        print("Choose DB\n1- crypto\n2- schooldb")
        print("3- mydatabase\n4- sys")
        print("88- List Databases")
        print("99- Create Database\n00- Exit")
        while True:
            choice = input()
            given_password = getpass("Enter Server Password: ")
            if choice in self.database_choice:
                self.server_connection(self.database_choice.get(choice), given_password)
            elif choice == "88":
                self.list_databases(self.server_operations(given_password))
            elif choice == "99":
                pass
            elif choice == "00":
                raise SystemExit
            else:
                print("Wrong choice")
                continue

    def menu_ask(self):
        ''' Keep asking after operations '''
        while True:
            print("Choose\n1- Main Menu\n2- Exit")
            choice = input()
            if choice == "1":
                self.choices()
            elif choice == "2":
                raise SystemExit
            else:
                continue

    @classmethod
    def server_connection(cls,db_name, given_password):
        ''' Connection to the server with given inputs before.'''
        connection = mysql.connector.connect(host = "localhost", user = "root", password = given_password, database = db_name)
        print("Connection Successful!", connection)
        print(f"Choose operation under {db_name}.")
        if db_name == "crypto":
            while True:
                print("1- Create Table\n2- Save Single Data to DB")
                print("3- Save Multiple Data to DB")
                choice = input()
                if choice == "1":
                    create_table()
                elif choice == "2":
                    print("There are 3 column here. Crypto Name, Symbol, Category")
                    crypto_name = input("Crypto name : ")
                    symbol = input("Symbol : ")
                    category = input("Category : ")
                    cursor = connection.cursor()
                    sql = "INSERT INTO crypto_currencies(crypto_name, symbol, category) VALUES(%s, %s, %s)"
                    values = (crypto_name, symbol, category)
                    cursor.execute(sql, values)
                    try:
                        connection.commit()
                        print(f"{cursor.rowcount} data added.")
                        print(f"ID of the last data is :{cursor.lastrowid}")
                    except mysql.connector.Error as err:
                        print("Error occured.", err)
                    finally:
                        connection.close()
                        print(f"Added to {db_name}.\n")
                    break
                elif choice == "3":
                    data_list = []
                    while True:
                        cursor = connection.cursor()
                        crypto_name = input("Crypto name : ")
                        symbol = input("Symbol : ")
                        category = input("Category : ")
                        data_list.append((crypto_name, symbol, category))
                        result = input("Do you want to continue adding datas ? Y/N ").upper()
                        if result == "N":
                            print("Datas are being transferred.")
                            print(data_list)
                            break
                        else:
                            continue
                    sql = "INSERT INTO crypto_currencies(crypto_name, symbol, category) VALUES(%s, %s, %s)"
                    cursor.executemany(sql, data_list)
                    try:
                        connection.commit()
                        print(f"{cursor.rowcount} datas added.")
                        print(f"ID of the last data is :{cursor.lastrowid}")
                    except mysql.connector.Error as err:
                        print("Error occured.", err)
                    finally:
                        connection.close()
                        print(f"Added to {db_name}.\n")
                    break

        while True:
            print("1- Create Table")
            choice = input()
            if choice == "1":
                create_table()

    def server_operations(cls, given_password):
        connection = mysql.connector.connect(host = "localhost", user = "root", password = given_password)
        return connection

    def crypto_currencies(self):
        ''' Connection to the server with given inputs before.'''
        connection = mysql.connector.connect(host = "localhost", user = "root", password = given_password, database = db_name)
        print("Connection Successful!", connection)

    def create_database(self):
        ''' Create new database on localhost '''
        # self.server_connection(self.database_choice.get(choice), given_password)
        database_name = input("Please enter database name: ")
        connection.cursor().execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created.\n")
        self.menu_ask()

    @classmethod
    def list_databases(cls, connection):
        ''' List of databases '''
        cursor = connection.cursor()# get the cursor
        cursor.execute("SHOW DATABASES") # select the database
        print("--- Databases ---")
        for (database_name,) in cursor:
            print(database_name,)
        # cursor.execute("SHOW TABLES")
        # print("--- Tables ---")
        # for (table_name,) in cursor:
        #     print(table_name)

    def create_table(self):
        cursor = connection.cursor()# get the cursor
        table_name = input("Table Name : ")
        connection.cursor().execute("CREATE TABLE schooldb(name VARCHAR(255), address VARCHAR(255))")
class_start = Database()
class_start.choices()
