"""
This file is used to audit an .osm file. 

In this case, the file represents the Open Street Map data for Phoenix, Arizona. 
The mapping variable maps abbreviations to their respective street type and 
cardinal direction to make the data consistent across all entries when entered
into the database.  Note that the mapping variable will be unique to whichever
OSM file you choose to use and must be updated accordingly.

The functions update_name and update_postcode update streets and postcodes
respectively, which are called by the data.py file, which then writes the data
to a csv file to be uploaded to a database.  
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "phoenix_arizona.osm"

#regular expressions to get the street type and cardinal direction of the address
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
direction_type_re = re.compile(r'(N |E |S |W |N\.|S\.|E\.|W\.)')

#some expected values for street types and directions
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "North", "South", "East", "West"]

# dictionary mapping to map to full-length street types and directions
mapping = { "St": "Street",
            "St.": "Street",
            "Ste": "Suite",
            "Ave.": "Avenue",
            "Ave,": "Avenue",
            "Ave": "Avenue",
            "Av": "Avenue",
            "Rd": "Road",
            "rd": "Road",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Pkwy": "Parkway",
            "Blvd.": "Boulevard", 
            "Blvd": "Boulevard",
            "N.": "North",
            "S.": "South",
            "E.": "East",
            "W.": "West",
            "N ": "North ",
            "S ": "South ",
            "E ": "East ",
            "W ": "West "}



def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    '''determine whether the element represents a street name'''
    return (elem.attrib['k'] == "addr:street")

def is_postcode(elem):
    '''determine whether the element represents a postal code'''
    return (elem.attrib['k'] == "addr:postcode")

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types  

def audit_postcode(osmfile):
    osm_file = open(osmfile, "r")
    post_codes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    #only include the 5 digit zip code for consistency across the data
                    if 'AZ' in tag.attrib['v']:
                        new_post_code = tag.attrib['v'].strip('AZ ')[0:5]
                    else:
                        new_post_code = tag.attrib['v'][0:5]
                        #print new_post_code
    osm_file.close()
    return post_codes

def update_name(name, mapping):
    '''this function updates the address name such that it unabbreviates street types, 
        directions, and removes commas in the addresses as to assure data consistency
        across all data entries'''

    m = street_type_re.search(name)
    n = direction_type_re.match(name)
    if n:
        name = re.sub(n.group(), mapping[n.group()], name)
        name = name.replace(',', '')
    if m.group() not in expected:
            if m.group() in mapping.keys():
                name = re.sub(m.group(), mapping[m.group()], name)
                name = name.replace(',' ,'')
    
    #Some entries are not filtered using the regular expressions
    #update certain entries manually instead
    name = name.replace('Rd.', 'Road')
    name = name.replace('Rd ', 'Road ')
    name = name.replace('St ', 'Street ')
    name = name.replace('Ste.', 'Suite')
    name = name.replace("Blvd.", "Boulevard")
    name = name.replace('Blvd', 'Boulevard')
    name = name.replace('Bldg.', 'Building')
    name = name.replace("Bldg", "Building")
    name = name.replace("Dr.", "Drive")
    name = name.replace(",", '')
    
    return name

def update_postcode(postcode):
    '''This function updates the postcodes to a standard 5 digit number'''
    if 'AZ' in postcode:
        new_post_code = postcode.strip('AZ ')[0:5]
    else:
        new_post_code = postcode[0:5]
    return new_post_code

######################################################################

st_types = audit_street(OSMFILE)
post_types = audit_postcode(OSMFILE)


for st_type, ways in st_types.iteritems():
    for name in ways:
        #RegEx takes care of a majority of data inconsistencies
        better_name = update_name(name, mapping)
        
        #Clean up the rest of the data not taken care of by update_name function
        better_name = better_name.replace('Rd.', 'Road')
        better_name = better_name.replace('Rd ', 'Road ')
        better_name = better_name.replace('St ', 'Street ')
        better_name = better_name.replace('Ste.', 'Suite')
        better_name = better_name.replace("Blvd.", "Boulevard")
        better_name = better_name.replace('Blvd', 'Boulevard')
        better_name = better_name.replace('Bldg.', 'Building')
        better_name = better_name.replace("Bldg", "Building")
        better_name = better_name.replace("Dr.", "Drive")
        better_name = better_name.replace(",", '')

        print name, "=>", better_name
        

