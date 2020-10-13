import os
import time
from sys import argv


def hmm_build(hmmbuild_output, hmmbuild_input):
    """Functie om hmmbuild aan te roepen
    :param hmmbuild_output: output file met het gemaakte hmm
    :param hmmbuild_input: alignment file, 1e iteratie van pfam daarna muscle.
    :return: geen
    """
    os.system("hmmbuild {} {}".format(hmmbuild_output, hmmbuild_input))


def hmm_search(hmmsearch_output_tab, hmmsearch_input):
    """Functie om hmmsearch aan te roepen
    :param hmmsearch_output_tab: tab delimited file met accessiecodes
    en scores
    :param hmmsearch_input: gemaakte hmmlogo uit de hmmsearch functie
    :return: geen
    """
    os.system("hmmsearch -A {} --cpu 16 {} /home/niek/course5"
              "/database/swissprot"
              .format(hmmsearch_output_tab, hmmsearch_input))


def convert(hmmsearch_output_tab):
    """Functie om de hmmsearch output te converteren naar een fasta file
    met sequenties
    :param hmmsearch_output_tab: tbl file uit hmmsearch
    :return: geen
    """
    os.system("esl-reformat -o output.fa fasta {}".format
              (hmmsearch_output_tab))
    time.sleep(1)
    if os.path.isfile("output.fa"):
        os.system("python3 append_fasta.py output.fa seqs.fa")


def muscle(muscle_input_fasta, muscle_output):
    """Functie om muscle aan te roepen
    :param muscle_input_fasta: fasta gegenereerd door de getfasta functie
    :param muscle_output: alignment file
    :return: geen
    """
    if os.path.isfile(muscle_input_fasta):
        os.system("muscle -in {} -out {}".format(muscle_input_fasta,
                                                 muscle_output))
    else:
        print("---FASTA FILE NOT FOUND IN MUSCLE FUNCTION---")
        print(muscle_input_fasta)


def clustalo(input_fasta, muscle_output):
    """Functie om clustalo aan te roepen
    :param input_fasta: input file met sequenties in fasta format
    :param muscle_output: output file met alignments
    :return: geen
    """
    os.system("clustalo --threads=12 -i {} -o {}".format(
        input_fasta, muscle_output))


def name_generator(i):
    """Functie om bestandsnamen te genereren per iteratie
    :param i: iteratienummer
    :return: bestandsnamen per functie
    """
    hmmbuild_output = "hmmbuild_" + str(i) + ".hmm"

    if i is 0:
        hmmbuild_input = "pfam_alignment.txt"
    else:
        hmmbuild_input = "clustalo_" + str(i - 1) + ".fa"

    hmmsearch_output_tab = "hmmbuild_aln_" + str(i) + ".sto"

    converter_output_fasta = "seqs.fa"

    muscle_output = "clustalo_" + str(i) + ".fa"

    return hmmbuild_output, hmmbuild_input, hmmsearch_output_tab, \
           converter_output_fasta, muscle_output,


if __name__ == '__main__':
    itnr = int(argv[1])

    for i in range(itnr):
        hmmbuild_output, hmmbuild_input, hmmsearch_output_tab, \
        converter_output_fasta, muscle_output = name_generator(i)

        hmm_build(hmmbuild_output, hmmbuild_input)

        time.sleep(2)

        hmm_search(hmmsearch_output_tab, hmmbuild_output)

        time.sleep(2)

        convert(hmmsearch_output_tab)

        time.sleep(2)

        clustalo("seqs.fa", muscle_output)
