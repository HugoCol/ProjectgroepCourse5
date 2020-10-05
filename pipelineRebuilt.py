import os
import time
from sys import argv
import pickle

def hmm_build(hmmbuild_output, hmmbuild_input):
    os.system("hmmbuild {} {}".format(hmmbuild_output, hmmbuild_input))


def hmm_search(hmmsearch_output_tab, hmmsearch_input):
    os.system("hmmsearch --tblout {} --cpu 16 {} /home/niek/course5/database/swissprot"
              .format(hmmsearch_output_tab, hmmsearch_input))


def get_accessiecodes(hmmsearch_output_tab):
    os.system("python3 GetAcodes.py {}".format(hmmsearch_output_tab))


def get_fasta(converter_output_fasta):
    if os.path.isfile("changelist"):
        os.system("python3 converter.py {}".format(converter_output_fasta))
    else:
        print("---FILE NOT FOUND IN GET_FASTA FUNCTION---")


def MUSCLE(muscle_input_fasta, muscle_output):
    if os.path.isfile(muscle_input_fasta):
        os.system("muscle -in {} -out {}".format(muscle_input_fasta, muscle_output))
    else:
        print("---FILE CONVERT NOT FOUND IN MUSCLE FUNCTION---")
        print(muscle_input_fasta)


def name_generator(i):
    hmmbuild_output = "hmmbuild_" + str(i) + ".hmm"

    if i is 0:
        hmmbuild_input = "pfam_alignment.txt"
    else:
        hmmbuild_input = "muscle_" + str(i-1) + ".aln"

    hmmsearch_output_tab = "hmmbuild_tab_" + str(i)

   #acodes_file = "ACS.txt"

    converter_output_fasta = "seqs.fa"

    muscle_output = "muscle_" + str(i) + ".aln"

    return hmmbuild_output, hmmbuild_input, hmmsearch_output_tab, \
           converter_output_fasta, muscle_output


if __name__ == '__main__':
    itnr = int(argv[1])

    for i in range(itnr):
        hmmbuild_output, hmmbuild_input, hmmsearch_output_tab, \
        converter_output_fasta, muscle_output = name_generator(i)

        hmm_build(hmmbuild_output, hmmbuild_input)

        time.sleep(2)

        hmm_search(hmmsearch_output_tab, hmmbuild_output)

        time.sleep(2)

        get_accessiecodes(hmmsearch_output_tab)

        time.sleep(2)

        get_fasta(converter_output_fasta)

        time.sleep(4)

        MUSCLE(converter_output_fasta, muscle_output)