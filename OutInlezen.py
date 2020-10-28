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
""" verwerkt het fasta bestand van de pipeline naar een dictonary
input : fasta, dit is een file bestand
output : d, dit is een dictonary met als key de header
         en sequentie also value
"""
    d = {}

    with open(fasta) as f:
        for line in f:
            if line.startswith('>'):
                key = line.strip()
                d[key] = ""
            else:
                d[key] += line.strip()

    return d


def seq_table(d):
""" voegt alle informatie die nuttig is toe aan Sequentie(_muscle)
input : d, de dictonary met alle headers en sequenties uit het fasta bestand
output: 
"""
    import re
    regex = "(?<=\().+?(?=\))"
  #de tabel kan Sequentie of Sequentie_muscle zijn
  # want we hebben twee verschillende tabellen om muscle en custalO 
  # te vergelijken 
    add_entry_sequentie = ('INSERT INTO Sequentie_muscle'
                           '(`ID`, `Seq`, `virus_info`, `header`)'
                           ' VALUES(%s,%s,%s,%s)')

    conn = mysql.connector.connect(host="hydron.io", user="course5", db="course5",
             password="yGVBJW3rniUd8uw1")
    cursor = conn.cursor(buffered=True)
    cursor2 = conn.cursor(buffered=True)

# een loop die over alle headers van het meegeven fasta bestand gaat
# en daarna alle informatie die we willen vinden in verschillende 
# variable zet
    for k in d.keys():
        header = k
        virus_info_start = re.findall(regex, k)

        if virus_info_start:
            virus_info = virus_info_start[0].replace('(', '| ')
            virus_info = str(virus_info)
        elif not virus_info_start:
            virus_info = str("niet gevonden met regex")

        line = k.split('/')
        line = line[0].replace('>', '')
        code = line
  # de tabel kan Sequentie of Sequentie_muscle zijn
  # want we hebben twee verschillende tabellen om muscle en custalO 
  # te vergelijken 
  # dit deel is om te kijken of de accessiecode niet al een keer voorkomt
  # dit was vooral gemaakt om duplicaten niet mogelijk te maken
        SQL = "select ID from Sequentie_muscle where ID like \'{}\'".format(code)
        print(SQL)
        cursor.execute(SQL)
        j = cursor.fetchall()
        if j:
            str('skip')
        else:
            cursor2.execute(add_entry_sequentie, (line, d[k], virus_info, header))
            conn.commit()

    conn.close()

    return

def open_webscarper(web):
""" Voegt alle informatie gevonden bij de webscraper toe aan de GO tabel
input: web, een txt bestand gemaakt door de web scraper
output: 
"""
    conn = mysql.connector.connect(host="hydron.io", user="course5", db="course5",
             password="yGVBJW3rniUd8uw1")
    cursor = conn.cursor(buffered=True)
    accesion_codes = []
    molecular = []
    biological = []

    add_entry_go = ('INSERT INTO GO'
                    '(`ID`, `Biological_function`, `Molecular_function`)'
                    ' VALUES(%s,%s,%s)')
#opened het bestand en zoekt naar de accessiecode, molecular en biological function
#en voegt dit toe aan de GO tabel en 
#wanneer het niet gevonden wordt voegt het niet gevonden toe
    with open(web) as file:
        for line in file:
            if line.startswith('accession'):
                line = line.split(':')
                accesion = line[1].strip()
                accesion_codes.append(accesion)
            elif line.startswith('molecular'):
                line = line.split(':')
                go = line[1].strip()
                if go:
                    mol_term = go
                if not go:
                    mol_term = "Niet gevonden"
                molecular.append(mol_term)
            elif line.startswith('biological'):
                line = line.split(':')
                go = line[1].strip()
                if go:
                    bio_term = go
                if not go:
                    bio_term = "Niet gevonden"
                biological.append(bio_term)

    for i in range(len(accesion_codes)):
        cursor.execute(add_entry_go, (accesion_codes[i], biological[i],
                                      molecular[i]))
        conn.commit()

    conn.close()
    return


if __name__ == '__main__':
    # /home/hugo/Documents/Tutor/Tutorperiode5/testfiles
    file = 'TBL0'
    login = {"host=":"hydron.io", "user=":"course5", "db=":"course5",
             "password=":"yGVBJW3rniUd8uw1"}
    fasta = 'Mseqs.fa'
    d = fasta_to_dict(fasta)
    seq_table(d)
    web = 'web_output.txt'
    open_webscarper(web)
 
