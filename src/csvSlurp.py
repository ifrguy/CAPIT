# CSV Slurp - Read an entire csv file into a dictionary of dictionaries.
# The first line of the csv file must contain the field names.
#
# History:
# 23Dec15 MEG Created.

import csv


# slurp( file, id )
#        file - string containing the full path to the csv file to be read.
#        id - string containing the name of the field to be the key in the 
#             outer dictionary key.

def slurp( file, id ):
    db=dict()
    with open( file, 'r' ) as data:
        f = csv.DictReader( data )
        for line in f:
            db[line[ id ]]=line
        return db



