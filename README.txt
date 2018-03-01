Here are a list of the files in the project submission along with their function. 

OSM+Project.html --> Contains a html converted Jupyter Notebook that details the entire process of the project along with the answers to several questions. 

audit.py --> contains the functions to update the street addresses and zip codes as part of the initial data wrangling phase

data.py --> Outputs several csv files based on the cleaned data processed by the audit.py file

transfer_to_db.py --> Converts the csv files into a database named "phoenix_az.db"

schema.py --> contains the mapping for each table's schema created in the database

phoenix_AZ_sample_smaller --> a subset of the original Phoenix mapping data used by the provided code in the project details

