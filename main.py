# imports pandas library to help be able to read the part.tbl file
import pandas as pd

# creates the file path to find the file in the folders 
file_path = "/Users/matthewdevaney/Downloads/part.tbl"
# reads the file
data = pd.read_csv(file_path, sep="\t")



