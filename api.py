import json
from getpass import getpass
from mysql.connector import connect, Error

# open_database_sql should be turned into a decorator, and connection should
# be enclosed in a 'with' statement 
# in order to get rid of connection.close() in every function
# also there should be a setup database function
def open_database_sql():
    """Open and return data from the MySQL database"""
    try:
        connection = connect(
            host="localhost",
            user='root',
            password=getpass("Enter password: "),
            database="grocery_database",
        )
    
    except Error as e:
        print(e)
    
    finally:
        return connection
        
def add_dish_sql():
    """Add a dish to the MySQL database"""
    connection = open_database_sql()
    dish_name = input("Please type in dish name: ")
    select_all_dishes_query = f"INSERT INTO Dishes(dish_name) VALUES('{dish_name}')"
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_all_dishes_query)
            connection.commit()
    except Error as e:
        if '1062' in str(e):
            print('This dish already exists in the database!')
        else:
            print(e)
    connection.close()

def show_dish_sql():
    """List ingredients of a dish from MySQL database"""
    connection = open_database_sql()
    dish_name = input("Which dish to display? ")
    display_dish_query = f'''SELECT ingredient
                            FROM Ingredients
                            WHERE dish_id = (SELECT dish_id
                                                FROM Dishes
                                                WHERE dish_name = '{dish_name}')'''
    with connection.cursor() as cursor:
        cursor.execute(display_dish_query)
        result = cursor.fetchall()
        if len(result) >= 1:
            for row in result:
                print(row[0])
        else:
            print('There are no ingredients added for this dish yet')
    connection.close()
   
# it would be nice to be able to add argument -A to the option in CLI 
# to delete all the dishes
def rm_dish_sql():
    """Remove dish from the MySQL database"""
    connection = open_database_sql()
    dish_name = input("Which dish to delete? ")
    remove_dishes_query = f'''DELETE FROM Dishes 
                              WHERE dish_name = "{dish_name}"'''
    remove_ingredients_query =  f'''DELETE FROM Ingredients 
    WHERE dish_id = (SELECT dish_id FROM Dishes WHERE dish_name = '{dish_name}')'''
    with connection.cursor() as cursor:
        # remove ingredients of the dish from Ingredients table
        cursor.execute(remove_ingredients_query)
        connection.commit()
        # remove the dish from Dishes table
        cursor.execute(remove_dishes_query)
        connection.commit()
    connection.close()
    print(f'Deleted {dish_name}')

def show_all_sql():
    """Show all dishes saved in the MySQL database"""
    connection = open_database_sql()
    show_all_query = '''SELECT dish_name
                        FROM Dishes
                        ORDER BY dish_name'''
    with connection.cursor() as cursor:
        cursor.execute(show_all_query)
        result = cursor.fetchall()
        print(f'Displaying {len(result)} saved dishes:')
        for row in result:
            print(row[0])
        
    connection.close()
    

def open_database():
    """Open and return data from the json database"""
    while True:
        try:
            with open('database.json') as f:
                database = json.load(f)
        except FileNotFoundError:
            print('File database.json is missing! Creating new database...')
            contents = {}
            with open('database.json', 'w') as f:
                json.dump(contents, f)
            print('Done!')
            continue
        else:
            return database
            break
    
def add_dish():
    """Adding a new dish to the database"""
    database = open_database()
    d_name = input("Please type in dish name: ")
    if d_name in database.keys():
        print(f"Dish {d_name} already exists!")
    else:
        print(f"Adding dish {d_name}.")
        database[d_name]=[]
        while True:
            usr_inp = input("Add ingredient or (q)uit: ")
            if usr_inp == 'q':
                with open('database.json', 'w') as f:
                    json.dump(database, f)
                break
            else:
                database[d_name].append(usr_inp)
        print("Dish added!")
    
def show_dish():
    """List ingredients of a dish specified by user"""
    database = open_database()
    usr_inp = input("Which dish to display? ")
    if usr_inp in database.keys():
        print(f"The ingredients of {usr_inp} are: {database[usr_inp]}")
    else:
        print(f"Dish {usr_inp} doesn't exist in the database")
        
def rm_dish():
    """Remove dish specified by user"""
    database = open_database()
    usr_inp = input("Which dish would you like to remove? ")
    if usr_inp in database.keys():
        print(f"Deleting dish {usr_inp}")
        del database[usr_inp]
        with open('database.json', 'w') as f:
                json.dump(database, f)
    else:
        print(f"Dish {usr_inp} doesn't exist in the database")

def show_all():
    """Shows all dishes in the database"""
    database = open_database()
    for key in database.keys():
        print(f"{key} ")
    if len(database.keys()) == 0:
        print('The database is currently empty.')

show_all_sql()
