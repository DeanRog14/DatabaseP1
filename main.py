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
    parts = data.to_dict(orient = "records")

    
    #saves the dictionary
    with open("output.json", "w") as f: 
        json.dump(parts, f, indent = 4)

   #prints out the first 10 lines of the tbl
    # with open(file_path, "r") as f:
    #     lines = f.readlines()
    # for i, line in enumerate(lines[:10]):  # Print first 10 lines
    #     print(f"Line {i+1}: {line}")
    # returns dictionary
    return parts
    
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

def add_data(file_path,parts): 

    existing_partkeys = [item["PARTKEY"] for item in parts]
    try: 
        partkey = int(input("What is the partkey for the part you would like to add?: "))
    except ValueError:
        print("Error: use a integer. try again.")
        return

    if partkey in existing_partkeys:
        print(f"Error: A part with PARTKEY {partkey} already exists. Please use a different PARTKEY.")
        return
    name = input("What is the name for the part you would like to add?: ")
    mfgr = input("Who is the manufacturer for the part?: ")
    brand = input("What is the brand for the part you would like to add?: ")
    part_type = input("What is the type for the part you would like to add?: ")
    try: 
        size = int(input("What is the size of the part you would like to add?: "))
    except ValueError:
        print("Error: use a integer. try again.")
        return
    container = input("What is the container for the part you would like to add?: ")
    try:
        retailprice = float(input("What is the retail price for the part you would like to add?: "))
    except ValueError:
        print("Error: use a float. Try again.")
        return
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

    keys = input("What atrribute would you like to use for your search?(PARTKEY, NAME, MFGR, BRAND, TYPE, SIZE, CONTAINER, RETAILPRICE, COMMENT)!(IF DELETING OR UPDATING A PART CHOOSE PARTKEY)!: ").strip().upper()
    print()
    if keys not in ["PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"]:
        print(f"Invalid attribute '{keys}'. Please try again.")
        return
    print()
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
            print()
            print(item)
            macthes_found = True
            return item
        
    if not macthes_found:
        print(f"No macthes found for '{values}' in column '{keys}'")
        return None
    
def delete_data(file_path, parts):
    data = authenication(file_path)
    
    item = search_data(parts)
    
    question = input("Are you sure you would like to delete this part?(Y/N): ").lower()

    if question == "y": 
        parts.remove(item)
    elif question == "n":
        return None
    else:
        print("Not a valid answer.")

    
    updated_df = pd.DataFrame(parts)
    updated_df.to_csv(file_path, sep="|", index=False, header=False, lineterminator= "|\n")
    print(f"Part deleted successfully. Updated data saved to {file_path}.")

def update_data(file_path, parts):
    data = authenication(file_path)

    item = search_data(parts)

    if not item: 
        print("No part found to update.")
        return
    
    question = input("Are you sure you would like to update this item?(Y/N): ").lower()

    if question == "y":
        for key in item:
            # skips the partkey value for the update
            if key != "PARTKEY":
                #has user input a new value if they want and shows old value
                new_value = input(f"Enter the new value for '{key}'(current: {item[key]}: ")
                # changes value if they input a new value
                if new_value:
                    item[key] = new_value
    else:
        return None

    
    
    updated_df = pd.DataFrame(parts)
    updated_df.to_csv(file_path, sep="|", index=False, header=False, lineterminator= "|\n")
    print(f"Part updated successfully. Updated data saved to {file_path}.")
    


def main(): 
    data_file = "part2.tbl"
    
    parts = create_data(data_file)

    choices()
    choice = int(input("what would you like to do to the table?: "))

    while choice != -1: 
        if(choice == 1): 
            add_data(data_file, parts)
            parts = create_data(data_file)
            
        elif(choice == 2): 
            search_data(parts)
        elif(choice == 3):
            update_data(data_file, parts)
            parts = create_data(data_file)
        elif(choice == 4): 
            delete_data(data_file, parts)
            parts = create_data(data_file)
        choices()
        choice = int(input("what would you like to do to the table?: "))
    parts.sort(key=lambda x: x.get("PARTKEY", 0))
    updated_df = pd.DataFrame(parts)
    updated_df.to_csv(data_file, sep="|", index=False, header=False, lineterminator= "|\n")
    

main()
# add_data("/Users/matthewdevaney/Downloads/part.tbl")

