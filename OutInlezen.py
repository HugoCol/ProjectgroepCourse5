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


def fasta_to_dict(fasta):
    d = {}

    with open(fasta) as f:
        for line in f:
            if line.startswith('>'):
                key = line.strip()
                d[key] = ""
            else:
                d[key] = line.strip()


    return d

def uni_accessie(host, user, db, password,accessiecode,tabel_naam):
    """
    Functie om te checken of een accessiecode al in de databaes zit
    Je geeft de gegevens mee om aan de database te verbinden
    Dan de accessiecode die je wilt controleren en de tabelnaam waarin
    je wilt zoeken
    als de accessiecode uniek is krijg je een True terug
    als de accessiecode al in de tabel staat is het False
    """
    try:
        t = True
        while t:
            conn = mysql.connector.connect(host=host, user=user, db=db,
                                           password=password)
            cursor = conn.cursor()

            SQL = "select ID from \'{}\' where ID like " \
                  "\'{}\'"

            cursor.execute(SQL,(accessiecode,tabel_naam))

            for i in cursor:
                accode = i[0]
                if accode is not None:
                    t = False
                else:
                    t = True
            conn.close()
            return t
    except ValueError:
        print('Onverwachte value')
    except ModuleNotFoundError:
        print("De benodigde module is niet gevonden")


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


def databasebasefiller(host, user, db, password, table_in_list):
    """
    uitdenken: Wat zijn onze inputs voor de functies?

    hoe voer je die in je database?

    maken:

    controleer of een accessiecode uniek is voordat je deze toevoegd

    maak per tabel een functie om deze te vullen, je maakt aparte
    commando's

    table_in_list :
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

    add_entry_sequentie = ('INSERT INTO Sequentie '
                           '(`ID`, `Seq`, `Accessiecode`)'
                           ' VALUES(%s,%s,%s)')

    add_entry_taxonomy = ('INSERT INTO Taxonomy '
                          '(`ID`, `Naam` )'
                          'VALUES(%s,%s)')

    add_entry_Alignments = ('INSERT INTO Alignments '
                            '(`ID`, `Iteratie`, `Alignment_file`)'
                            'VALUES(%s,%s,%s)')

    add_entry_GO = ('INSERT INTO GO'
                    '(`ID`, `GO_terms`)'
                    'VALUES(%s,%s)')

    conn = mysql.connector.connect(host=host, user=user, db=db,
                                   password=password)

    for row in table_in_list:
        cursor = conn.cursor()

        cursor.execute(add_entry_GO, (row[0] row[GOterms]))
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


    # databasebasefiller(host, user, db, password, table_in_list)
