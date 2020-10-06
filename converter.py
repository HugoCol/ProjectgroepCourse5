import requests
import re
import time
from sys import argv
import pickle


def get_acessionCodes(file):
    """Functie die de accessiecodes in het juiste format voor de API zet.
    :return: string met accessiecodes.
    """
    codes = []

    file = open(file, "r")

    file = file.readlines()

    for line in file:
        line = line.strip()
        codes.append(line)

    print(codes)

    return codes


def esearch_history(url_id):
    """Functie die accessiecodes in de ESearch history zet (dit is nodig om een EFetch te doen)
    :param url_id: string met accessiecodes uit de get_accessiecodes functie.
    :return: env, query
    """

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term={}&usehistory=y&api_key=7fef8992ebefa5ccc23e3d3a2425b9ed0109".format(
        url_id)
    print(url)

    r = requests.get(url)

    print(r.text)

    # WebEnv key die teruglinkt naar de ESearch query.
    env = re.search("<WebEnv>(.*?)<\/WebEnv>", r.text).group(1)

    # Query ID dat teruglinkt naar de ESearch query.
    query = re.search("<QueryKey>(.*?)<\/QueryKey>", r.text).group(1)

    return env, query


def build_request_url(databaseSelection, returnFormat, webEnv, query):
    """Functie waar de request url wordt opgebouwd uit de verschillende
    variabelen.
    :param databaseSelection: Entrez database selectie,
    zie: https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly
    :param returnFormat: return format van de opgevraagde data,
    zie: https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly
    :param webEnv: webenv key die gegenereerd wordt in de esearch_history functie
    :param query: query key die gegenereerd wordt in de esearch_history functie
    :return:
    """
    default_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    url_database = "db={}".format(databaseSelection)
    url_query = "query_key={}".format(query)
    url_webEnv = "WebEnv={}".format(webEnv)
    url_returnFormat = "rettype={}".format(returnFormat)
    url_api_key = "api_key=7fef8992ebefa5ccc23e3d3a2425b9ed0109"

    url = default_url + "?" + url_database + "&" + url_api_key + "&" + url_query + "&" + \
          url_webEnv + "&" + url_returnFormat

    print(url)

    r = requests.get(url)

    return r


def fasta_writer(r, file_name):
    """Functie om de request output naar fasta te schrijven.
    :param r: request object
    :param file_name: door de gebruiker ingevoerde filename
    :return: geen
    """
    file = open(file_name, "a")

    file.write(r.text)

    file.close()


def get_pickle():
    loadfile = open("changelist", 'rb')
    codes = pickle.load(loadfile)
    loadfile.close()
    return codes


def list_splitter(codes):
    d = {}
    total = (len(codes) / 90).__round__()

    for j in range(total):
        temp_list = []
        for i in range(90):
            temp_list.append(codes[i])
        d[j] = '+'.join(temp_list)

    return d, total


if __name__ == '__main__':
    databaseSelection = "protein"
    returnFormat = "fasta"
    #file = argv[1]
    file_name = argv[1]

    #codes = get_acessionCodes(file)

    codes = get_pickle()

    if len(codes) > 90:
        d, total = list_splitter(codes)

        for i in range(total):
            webEnv, query = esearch_history(d[i])

            time.sleep(10)

            r = build_request_url(databaseSelection, returnFormat, webEnv, query)

            time.sleep(10)

            fasta_writer(r, file_name)

            print('---------' + str(i+1) + "/" + str(total) +
                  " SLEEPING 10--------")
            time.sleep(10)
    else:
        url_id = "+".join(codes)

        webEnv, query = esearch_history(url_id)

        time.sleep(10)

        r = build_request_url(databaseSelection, returnFormat, webEnv, query)

        time.sleep(10)

        fasta_writer(r, file_name)


# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=P87506.1,O56140.2&rettype=fasta
