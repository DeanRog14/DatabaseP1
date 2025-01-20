# imports pandas library to help be able to read the part.tbl file
import pandas as pd
import json



def create_data(file_path): 
    # creates the file path to find the file in the folders 
    file_path = "/Users/matthewdevaney/Downloads/part.tbl"
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

def add_data(file_path): 
    columns = ["PARTKEY", "NAME", "MFGR", "BRAND", "TYPE", "SIZE", "CONTAINER", "RETAILPRICE", "COMMENT"]

    try:
        data = pd.read_csv(file_path, sep="|", header=None, names=columns)
    except FileNotFoundError:
        data = pd.DataFrame(columns=columns)

    partkey = int(input("What is the partkey for the part you would like to add?: "))
    name = input("What is the name for the part you would like to add?: ")
    mfgr = input("Who is the manufacturer for the part?: ")
    name = input("What is the name for the part you would like to add?: ")
    brand = input("What is the brand for the part you would like to add?: ")
    part_type = input("What is the type for the part you would like to add?: ")
    size = int(input("What is the size of the part you would like to add?: "))
    container = input("What is the container for the part you would like to add?: ")
    retailprice = int(input("What is the retail price for the part you would like to add?: "))
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
    updated_tbl = pd.concat([data, new_row], ignore_index = True)

    updated_tbl.to_csv(file_path, sep = "|", index = False, header = False)
    print(f"New data added successfully: \n{new_data}")


def main(): 
    data_file = "/Users/matthewdevaney/Downloads/part.tbl"
    create_data(data_file)

    print("Actions able to be done to the table: ")
    print("1. Insert new part")
    print("2. Search for a part")
    print("3. Update a part")
    print("4. Delete a part")
    print("-1 to exit the program")
    choice = input("what would you like to do to the table?: ")

    while choice != -1: 
        if(choice == 1): 
            add_data(data_file)
        elif(choice == 2): 
            print("you are searching for a part")
        elif(choice == 3):
            print("you are updating a part")
        elif(choice == 4): 
            print("you are deleting a part")
        
    # print(parts_dict)
    # print(data)


main()
# add_data("/Users/matthewdevaney/Downloads/part.tbl")

