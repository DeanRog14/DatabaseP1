# imports pandas library to help be able to read the part.tbl file
import pandas as pd
import json
import os


def choices():
    print()
    print()
    print("Actions able to be done to the table: ")
    print("1. Insert new part")
    print("2. Search for a part")
    print("3. Update a part")
    print("4. Delete a part")
    print("-1 to exit the program")
    print()

def create_data(file_path): 
    # creates the file path to find the file in the folders 
    # reads the file
    data = pd.read_csv(file_path, sep="|", header = None, names = [
        "PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", 
        "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"
    ], index_col = False)

    #creates dictionary from the tbl using pandas library
    parts_dict = data.to_dict(orient = "records")

    #saves the dictionary
    with open("output.json", "w") as f: 
        json.dump(parts_dict, f, indent = 4)

   #prints out the first 10 lines of the tbl
    # with open(file_path, "r") as f:
    #     lines = f.readlines()
    # for i, line in enumerate(lines[:10]):  # Print first 10 lines
    #     print(f"Line {i+1}: {line}")
    # returns dictionary
    return parts_dict
    
def authenication(file_path): 
    columns = ["PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"]

    try:
        data = pd.read_csv(file_path, sep="|", header=None, names=columns)
    except FileNotFoundError:
        print(f"File not found at {file_path}. Returning an empty table.")
        data = pd.DataFrame(columns=columns)
    except pd.errors.EmptyDataError:
        print(f"File is empty. Returning an empty table.")
        data = pd.DataFrame(columns=columns)
    return data
## returns dataframe

def add_data(file_path): 
    data = authenication(file_path)

    partkey = int(input("What is the partkey for the part you would like to add?: "))
    name = input("What is the name for the part you would like to add?: ")
    mfgr = input("Who is the manufacturer for the part?: ")
    brand = input("What is the brand for the part you would like to add?: ")
    part_type = input("What is the type for the part you would like to add?: ")
    size = int(input("What is the size of the part you would like to add?: "))
    container = input("What is the container for the part you would like to add?: ")
    retailprice = float(input("What is the retail price for the part you would like to add?: "))
    comment = input("Any comments for the part?: ")
    
    
    new_data = {
        "PARTKEY" : partkey,
        "NAME" : name,
        "MFGR" : mfgr, 
        "BRAND" : brand, 
        "TYPE" : part_type, 
        "SIZE" : size, 
        "CONTAINER" : container, 
        "RETAILPRICE" : retailprice, 
        "COMMENT" : comment
    } 

    new_row = pd.DataFrame([new_data])

    new_row.to_csv(file_path, sep="|", index=False, header=False, mode ="a", lineterminator="|\n")
    
    print(f"New data added successfully: \n{new_data}")





def search_data(parts): 

    keys = input("What atrribute would you like to use for your search?(PARTKEY, NAME, MFGR, BRAND, TYPE, SIZE, CONTAINER, RETAILPRICE, COMMENT)!(IF DELETING A PART CHOOSE PARTKEY)!: ").strip().upper()

    if keys not in ["PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"]:
        print(f"Invalid attribute '{keys}'. Please try again.")
        return
    
    if(keys == "PARTKEY" or keys == "SIZE"):
        try:
            values = int(input(f"What value were you looking for in '{keys}'?: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return
    elif(keys == "RETAILPRICE"):
        try:
            values = float(input(f"What value were you looking for in '{keys}'?: "))
        except ValueError:
            print("Invalid input. Please enter a valid float.")
            return
    else: 
        values = input(f"What value were you looking for in '{keys}'?: ").strip().lower()

    
    macthes_found = False
    for item in parts: 
        
        if item.get(keys, "") == values:
            print(item)
            macthes_found = True
            return item
        
    if not macthes_found:
        print(f"No macthes found for '{values}' in column '{keys}'")
        return "try again"
    
def delete_data(file_path, parts):
    data = authenication(file_path)
    
    item = search_data(parts)
    
    question = input("Are you sure you would like to delete this item?(Y/N): ").lower()

    if question == "y": 
        parts.remove(item)
    else:
        return


def main(): 
    data_file = "part2.tbl"
    
    parts = create_data(data_file)

    choices()
    choice = int(input("what would you like to do to the table?: "))

    while choice != -1: 
        if(choice == 1): 
            add_data(data_file)
        elif(choice == 2): 
            search_data(parts)
        elif(choice == 3):
            print("you are updating a part")
        elif(choice == 4): 
            delete_data(data_file, parts)
        choices()
        choice = int(input("what would you like to do to the table?: "))
    
    

main()
# add_data("/Users/matthewdevaney/Downloads/part.tbl")

