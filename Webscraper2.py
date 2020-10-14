import bs4
import requests
from selenium import webdriver
import pandas as pd


def main():
    headers = bestand_inlezen()
    driver = webdriver.chrome()
    #headers, sequences = lees_inhoud(bestandsnaam)
    for header in headers:
        get_page_contents(header, driver)


def bestand_inlezen():
    headers = []
    bestandsnaam = "AccessiecodesTBL0.txt"
    bestand = open(bestandsnaam)
    for line in bestand:
        line = line.strip("\n")
        headers.append(line)

    return headers


def lees_inhoud(bestand):
    """
    Convert de inhoud van de fasta file naar 2 lijsten.
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
                headers.append(line)
            else:
                seq += line
        sequences.append(seq)
        return headers, sequences
    except FileNotFoundError:
        print("FileNotFoundError: The file was not found, give an valid file, and try agian")
    except IOError:
        print("IOerror, file can not be read")


def get_page_contents(header, driver):
    print("header")
    moFunctions = []
    url = "https://www.uniprot.org/uniprot/" + header
    page = driver.get("<a href={}>".format(url))
    content = driver.page_source
    soup = bs4.BeautifulSoup(content)
    for a in soup.findAll("a", href=True, attrs="class"):
        moFu = a.find("div", attrs={"noNumbering molecular_function"})
        moFunctions.append(moFu)
    print(moFunctions)

    #functie = soup.find("div", attrs="noNumbering molecular_function")  # , onclick_="window.ga('UniProt-Entry-View', 'click', 'Display-GO-Term')")


main()
