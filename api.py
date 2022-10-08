import json

def open_database():
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
