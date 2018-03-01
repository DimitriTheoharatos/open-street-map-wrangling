# Open Street Map Data Case Study

In this case study, the mapping data of Phoenix, Arizona is wrangled utilizing Python and queried using a local sqlite database.  The exact area of the map can be extracted at the following link:

https://mapzen.com/data/metro-extracts/metro/phoenix_arizona/

Note that the Raw OSM XML file was selected for download. 



### List of Files in Repository: 

OSM+Project.html --> Contains a html converted Jupyter Notebook that details the entire process of the project along with the answers to several queries. 

OSM_Project.ipynb --> Contains a python Juypter notebook where several queries into the database are organized.

audit.py --> contains the functions to update the street addresses and zip codes as part of the initial data wrangling phase

data.py --> Outputs several csv files based on the cleaned data processed by the audit.py file

transfer_to_db.py --> Converts the csv files into a database named "phoenix_az.db"

schema.py --> contains the mapping for each table's schema created in the database

phoenix_AZ_sample_smaller.osm --> a subset of the original Phoenix mapping data used by the provided code in the project details

