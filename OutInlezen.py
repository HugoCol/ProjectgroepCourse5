"""
open file met een gui window
maak filters met de GUI?

als je de sha2 error krijgt
terminal in pycharm -> pip3 install mysql-connector-python

"""

import csv
import mysql
import mysql.connector

def file_reader(file):
    """
    Filter the information in the file before adding it to database
    """
    filtered_output_file = []

    with open(file) as tsvfile:
        for row in tsvfile:
            print(''.join(row))

    return filtered_output_file


def databasebasefiller(host, user, db, password, filtered_output_file):
    """
    pak de data uit de gefilterde info lijst en stop deze in
    """
    conn = mysql.connector.connect(host=host, user=user, db=db,
                                   password=password)


if __name__ == '__main__':

    # /home/hugo/Documents/Tutor/Tutorperiode5/testfiles
    file = '/home/hugo/Documents/Tutor/Tutorperiode 5/testfiles/TBL0.txt'

    # database inlog
    host = "hydron.io"
    user = "course5"
    db = "course5"
    password = "yGVBJW3rniUd8uw1"
    # aanroep

    filtered_output_file = file_reader(file)
    databasebasefiller(host, user, db, password, filtered_output_file)