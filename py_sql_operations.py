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
                break
            elif choice == "88":
                self.list_databases(self.server_operations(given_password))
                break
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

    def server_connection(self, db_name, given_password):
        ''' Connection to the server with given inputs before.'''
        connection = mysql.connector.connect(host = "localhost", user = "root", password = given_password, database = db_name)
        print("Connection Successful!", connection)
        print(f"Choose operation under {db_name}.")
        if db_name == "crypto":
            while True:
                print("\n1- List Cryptos\n2- Save Single Data to DB")
                print("3- Save Multiple Data to DB\n4- Filter Datas")
                print("5- Order Datas\n6- Delete Datas")
                print("99- Exit")
                choice = input()
                if choice == "1":
                    self.list_crypto(connection)
                    continue
                elif choice == "2":
                    self.single_data(connection, db_name)
                    break
                elif choice == "3":
                    self.multiple_data(connection, db_name)
                    break
                elif choice == "4":
                    self.filter_crypto(connection)
                    continue
                elif choice == "5":
                    self.order_by(connection)
                    break
                elif choice == "6":
                    self.delete_crypto(connection)
                    break
                elif choice == "99":
                    raise SystemExit
                else:
                    continue

    def list_crypto(self, connection):
        '''List Crypto Datas'''
        cursor = connection.cursor()
        cursor.execute('Select * From crypto_currencies')
        data_list = cursor.fetchall()
        for data in data_list:
            print(f"ID: {data[0]}, Name: {data[1]}, Symbol: {data[2]}, Category: {data[3]}")

    def single_data(self, connection, db_name):
        ''' Add single data to sql '''
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

    def multiple_data(self, connection, db_name):
        ''' Add multiple datas to sql '''
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

    def filter_crypto(self, connection):
        ''' filter by given queries '''
        cursor = connection.cursor()
        while True:
            print("1- ID\n2- Name\n3- Symbol")
            print("4- Category\n99- Exit")
            choice = input()
            if choice == "1":
                crypto_id = input("Filter by ID : ")
                cursor.execute(f"Select * From crypto_currencies Where id='{crypto_id}'")
                data_list = cursor.fetchall()
                for data in data_list:
                    print(f"ID: {data[0]}, Name: {data[1]}, Symbol: {data[2]}, Category: {data[3]}\n")
                break
            elif choice == "2":
                name = input("Filter by Name : ")
                cursor.execute(f"Select * From crypto_currencies Where crypto_name='{name}'")
                data_list = cursor.fetchall()
                for data in data_list:
                    print(f"ID: {data[0]}, Name: {data[1]}, Symbol: {data[2]}, Category: {data[3]}\n")
                break
            elif choice == "3":
                symbol = input("Filter by Symbol : ")
                cursor.execute(f"Select * From crypto_currencies Where symbol='{symbol}'")
                data_list = cursor.fetchall()
                for data in data_list:
                    print(f"ID: {data[0]}, Name: {data[1]}, Symbol: {data[2]}, Category: {data[3]}\n")
                break
            elif choice == "4":
                category = input("Filter by Category : ")
                cursor.execute(f"Select * From crypto_currencies Where category='{category}'")
                data_list = cursor.fetchall()
                for data in data_list:
                    print(f"ID: {data[0]}, Name: {data[1]}, Symbol: {data[2]}, Category: {data[3]}\n")
                break
            elif choice == "99":
                raise SystemExit
            else:
                continue

    def order_by(self, connection):
        ''' order by given queries '''
        cursor = connection.cursor()
        order = {
            "1": "id",
            "2": "crypto_name",
            "3": "symbol",
            "4": "category"
        }
        while True:
            print("Order By :")
            print("1- ID\n2- Name\n3- Symbol")
            print("4- Category\n99- Exit")
            choice = input()
            if choice == "99":
                raise SystemExit
            elif choice in order:
                cursor.execute(f"Select * From crypto_currencies Order By {order.get(choice)} ASC")
                data_list = cursor.fetchall()
                for data in data_list:
                    print(f"ID: {data[0]}, Name: {data[1]}, Symbol: {data[2]}, Category: {data[3]}\n")
            else:
                continue

    def delete_crypto(self, connection):
        ''' delete '''
        cursor = connection.cursor()
        delete_by = {
            "1": "id",
            "2": "crypto_name",
            "3": "symbol",
        }
        while True:
            print("Delete By :")
            print("1- ID\n2- Name\n3- Symbol")
            print("99- Exit")
            choice = input()
            delete = input(f"Delete by {delete_by.get(choice)} : ")
            if choice == "99":
                raise SystemExit
            elif choice in delete_by:
                sql = f"delete from crypto_currencies where {delete_by.get(choice)}={delete}"
                cursor.execute(sql)
                try:
                    connection.commit()
                    print(f"{cursor.rowcount} data deleted.")
                except mysql.connector.Error as err:
                    print("Error! ", err)
                finally:
                    connection.close()
                    print("Deleted. DB Closing.\n")
                break
            else:
                continue

    def server_operations(self, given_password):
        ''' returns connection '''
        connection = mysql.connector.connect(host = "localhost", user = "root", password = given_password)
        return connection

    def create_database(self):
        ''' Create new database on localhost '''
        # self.server_connection(self.database_choice.get(choice), given_password)
        database_name = input("Please enter database name: ")
        connection.cursor().execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created.\n")
        self.menu_ask()

    def list_databases(self, connection):
        ''' List of databases '''
        cursor = connection.cursor()# get the cursor
        cursor.execute("SHOW DATABASES") # select the database
        print("--- Databases ---")
        for (database_name,) in cursor:
            print(database_name,)
        print("\n")
        self.menu_ask()

class_start = Database()
class_start.choices()
