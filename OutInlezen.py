"""
open file met een gui window
maak filters met de GUI?

als je de sha2 error krijgt
terminal in pycharm -> pip3 install mysql-connector-python

accession', 'query', 'name', 'accession', 'Evalue', 'score', 'bias',
'Evalue', 'score', 'bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom',
 'rep', 'inc', 'description', 'of', 'target'

acessicode[0]
e-value full sequence [3]
score[4]
bias[5]

beste domein e-value [6]
score [7]
bias[8]

pfam hmm > X aantal iteraties van (hmmsearch > accessie > sequentie
opvragen > muscle > alignment > hmmsearch) > webscraper > database

"""

import mysql
import mysql.connector
import random
import string


def file_reader(file):
    """
    Filter the information in the file before adding it to database
    """
    filtered_output_file = []

    with open(file) as tsvfile:
        counter = 0
        # alle informatie in een tabel
        table_in_list = []

        for row in tsvfile:

            counter += 1
            # vanaf dit stuk pak je niet de headers in de lijst
            if counter >= 4:
                e = row.replace('-', '')
                try:
                    a = e.split()
                    table_in_list.append(a)
                    # extra filter over de accessiecodes

                except IndexError:
                    pass

    return table_in_list


def uid_gen(host, user, db, password):
    """Functie om een uniek ID te genereren en te checken of deze
    al aanwezig is in de database
    """
    try:
        t = True
        while t:
            uid = ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in
                range(12))
            conn = mysql.connector.connect(host=host, user=user, db=db,
                                           password=password)
            cursor = conn.cursor()
            SQL = "select tax_id from taxonomy where tax_id like \'{}\'". \
                format(uid)
            cursor.execute(SQL)
            uid_test = None
            for i in cursor:
                uid_test = i[0]
            if uid_test is not None:
                t = True
            else:
                t = False
            conn.close()
            return uid
    except ValueError:
        print('Onverwachte value')
    except ModuleNotFoundError:
        print("De benodigde module is niet gevonden")


def databasebasefiller(host, user, db, password, table_in_list):
    """
    table_in_list:
    acessicode[0]
    e-value full sequence [3]
    score[4]
    bias[5]
    beste domein e-value [6]
    score [7]
    bias[8]

Database:
    Alignments:
        - ID PK gegenereerd met uid_gen functie
        - Iteratie# (teller)
        - Alignment_file (uit muscle)
    GO
        - ID
        - Go_terms (webscraper)
    Sequentie (komt uit converter.py)
        - ID PK
        - Seq
        - Accessiecode (converter.py)
    Taxonomy
        - ID PK
        - Naam (webscraper)
    """
    conn = mysql.connector.connect(host=host, user=user, db=db,
                                   password=password)
    cursor = conn.cursor()
    for row in table_in_list:
        unique_id = uid_gen(host,user,db,password)

        # zet hier je Mysql command
        command = f"insert into Sequentie (ID,) values " \
                  f"('{unique_id}', " \
                  f"'{datadic[i][11][countlin]}')"

        # voer de command uit
        cursor.execute(command)
        conn.commit()
        # sluit de verbinding
    cursor.close()


if __name__ == '__main__':
    # /home/hugo/Documents/Tutor/Tutorperiode5/testfiles
    file = 'TBL0'

    # database inlog
    host = "hydron.io"
    user = "course5"
    db = "course5"
    password = "yGVBJW3rniUd8uw1"
    # aanroep

    table_in_list = file_reader(file)
    print(table_in_list)
    # databasebasefiller(host, user, db, password, table_in_list)
