import bs4
import requests
from lxml import html


def main():
    """     De main functie voert het webscrapen uit en
    ontvangt de lijst met headers die aan de url worden meegegeven.
    Ook opent deze functie het resultaten bestand en
    schrijft de lijsten met resultaten weg, een lijst met headers en
    een lijst met de go-termen die hier bij horen. 
    Deze worden weggeschreven in een tekstbestand
    """
    bestandsnaam = bestand_inlezen()
    headers, sequences = lees_inhoud(bestandsnaam)
    megaItemList = []
    file = open("testoutput.txt", "a+")
    print(headers)
    megatext = ""

    for item in headers:
        print(item)
        item = item.replace(">", "").split("_")
        ##print(item[0])
        url = "https://www.uniprot.org/uniprot/" + item[0]
        soup = get_page_contents(url)
        item = ''.join(item)
        try:
            molfunctions, biofunctions = scrapen(url, soup, item)
        except:
            molfunctions = []
            biofunctions = []
            file.write("header: " + item + "\n"
                                           "for this protein no GO terms were recovered" + '\n')
            pass
        print(molfunctions, biofunctions)
        file.write("accession code:" + item + "\n")
        molfunctions = ','.join(molfunctions)
        biofunctions = ','.join(biofunctions)
        try:
            file.write("molecular function:" + molfunctions + "\n")
        except:
            file.write("molecular function: none" + "\n")
        try:
            file.write("biological function:" + biofunctions + "\n")
        except:
            file.write("biological function: none" + '\n')
        file.write("\n")
    file.close()


def bestand_inlezen():
    """     Ontvangt de naam van het bestand en returnt deze aan de main

    :return: bestandsnaam
    """
    bestandsnaam = "Test_input.fasta"
    return bestandsnaam


def lees_inhoud(bestand):
    """    Convert de inhoud van de fasta file naar 2 lijsten.
    Namelijk de headers en de sequenties

    :param bestand:
    :return list met Headers en een list met sequences:
    """
    bestand = open(bestand)
    headers, sequences = [], []
    try:
        seq = ""
        for line in bestand:
            line = line.strip()
            if line.startswith(">"):
                if seq != "":
                    sequences.append(seq)
                    seq = ""
                line = line[4:10]
                headers.append(line)
            else:
                seq += line
        sequences.append(seq)
        return headers, sequences

    except FileNotFoundError:
        print(
            "FileNotFoundError: The file was not found, give an valid file, and try agian")
    except IOError:
        print("IOerror, file can not be read")


def get_page_contents(url):
    '''    Haalt de pagina op aan de hand van de meegegeven url

    param: de url van de site
    return: is de pagina in html code
    '''
    print(url)
    page = requests.get(url, headers={"Accept-Language": "en-US"})
    return bs4.BeautifulSoup(page.text, "html.parser")


def scrapen(url, soup, header):
    '''  Deze functie haalt aan de hand van het BeautifulSoup 4 package de delen van de website op waarin de go-termen staan
    en voegt deze toe aan lijsten met daarin de go-termen voor het meegegeven eiwit.
    param: de url van de site, en de htmnl code
    return: de go-termen van het meegegeven eiwit
    '''
    biofunctions = []
    molfunctions = []

    functie = soup.find(class_="noNumbering molecular_function").findAll(
        'a')  # , onclick_="window.ga('UniProt-Entry-View', 'click', 'Display-GO-Term')")
    print("the molecular functions of {} include:".format(header))
    for i in functie:
        print(i.text)
        molfunctions.append(i.text)
    #        if not temp[0].isupper():
    #           ##print(i.text)
    #          templist.append(i.text)

    functie = soup.find(class_="noNumbering biological_process").findAll(
        'a')  # , onclick_="window.ga('UniProt-Entry-View', 'click', 'Display-GO-Term')")
    filetext = ""
    print("the biological functions of {} include:".format(header))
    for i in functie:
        print(i.text)
        biofunctions.append(i.text)

    return molfunctions, biofunctions


main()
