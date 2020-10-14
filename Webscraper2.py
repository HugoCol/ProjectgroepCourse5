import bs4
import requests
from lxml import html


def main():
    """     De main functie voert het webscrapen uit en
    ontvangt de lijst met headers die aan de url worden meegegeven.
    Ook opent deze functie het resultaten bestand en
    schrijft de lijsten met resultaten weg, een lijst met headers en
    een lijst met de go-termen die hier bij horen.
    """
    bestandsnaam = bestand_inlezen()
    headers, sequences = lees_inhoud(bestandsnaam)
    megaItemList = []
    file = open("testoutput.txt", "a+")

    megatext = ""

    for item in headers:
        item = item.replace(">", "").split("_")
        ##print(item[0])
        url = "https://www.uniprot.org/uniprot/" + item[0]
        soup = get_page_contents(url)
        items, filetext = scrapen(url, soup, item)
        megaItemList.append(items)
        megatext += filetext + "\n"

    try:
        file.write(str(megatext) + "\n")
        file.close()
    except:
        pass


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
    templist = []
    functie = soup.find(class_="noNumbering molecular_function").findAll(
        'a')  # , onclick_="window.ga('UniProt-Entry-View', 'click', 'Display-GO-Term')")
    print(header)
    for i in functie:
        print(i.text)
    #        if not temp[0].isupper():
    #           ##print(i.text)
    #          templist.append(i.text)

    functie = soup.find(class_="noNumbering biological_process").findAll(
        'a')  # , onclick_="window.ga('UniProt-Entry-View', 'click', 'Display-GO-Term')")
    filetext = ""
    for i in functie:
        print(i.text)
    #        if not temp[0].isupper():
    #           ##print(i.text)
    #          filetext += str(i.text) + "\n"
    #   templist.append(i.text)

    # recommended_name = soup.find(property="name", class_="recommended-name").find()
    # gene_name = soup.find(class_="noBorders").find("a")
    # name = soup.find(class_="name").findAll("a")
    # dbtabel = soup.find(href="/taxonomy/{}").format(header).findAll("a")
    # print(recommended_name.children)
    # print(gene_name.text)
    # print(name.text)
    # print(dbtabel)
    # for i in dbtabel:
    #   print(i.text)
    #  filetext += str(i.text) + "\n"
    # page = requests.get(url, headers={"Accept-Language": "en-US"})
    table = soup.findAll(class_="databaseTable")
    table = table[1]
    # tree = html.fromstring(page)
    # dbtabel = tree.xpath("//table[@class='databaseTable']/text()")
    counter = 0
    for line in table:
        if counter == 0:
            line = line.strip("")
            print(line)
            counter = + 1
        else:
            pass

    return templist, filetext


main()
