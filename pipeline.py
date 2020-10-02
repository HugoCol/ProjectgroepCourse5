import os
import time


def naamGeneratorOutput(i):
    naamHMM = "IT" + str(i) + ".hmm"
    naamALN = "IT" + str(i) + ".sto"
    naamMUSCLE = "M" + str(i) + ".aln"
    naamCONVERT = "CONV" + str(i) + ".fa"
    naamACS = "ACS" + str(i) + ".txt"
    return naamHMM, naamALN, naamACS, naamMUSCLE, naamCONVERT


def naamGeneratorInput(i):
    naamHMM = "IT" + str(i) + ".hmm"
    naamALN = "IT" + str(i - 1) + ".sto"
    naamMUSCLEin = "M" + str((i - 1)) + ".aln"
    return naamHMM, naamALN, naamMUSCLEin


def hmm_build(naamOutput, naamALN, i):
    os.system("hmmbuild {} {}".format(naamOutput, naamALN))


def hmm_search(naamOutput, naamHMM, i, naamTBL):
    os.system("hmmsearch --tblout {} -A {} --cpu 16 {} /home/niek/course5/database/swissprot".format(naamTBL, naamOutput, naamHMM))


def get_acs(naamTBL, naamACS):
    with open(naamTBL, newline='') as file:
        ids = []
        for line in file:
            line = line.replace("-", "")
            try:
                if line.split()[0] is '#':
                    pass
                else:
                    ids.append(line.split()[0])
            except IndexError:
                pass

    file = open(naamACS, "w")
    for i in ids:
        file.write(i)
        file.write("\n")
    file.close()


def get_fasta(naamACS, naamCONVERT):
    if os.path.isfile(naamACS):
        os.system("python3 converter.py {} {}".format(naamACS, naamCONVERT))
    else:
        print("---FILE NOT FOUND IN GET_FASTA FUNCTION---")
        print(naamACS, naamCONVERT)


def MUSCLE(naamCONVERT, naamMUSCLE):
    if os.path.isfile(naamCONVERT):
        os.system("muscle -in {} -out {}".format(naamCONVERT, naamMUSCLE))
    else:
        print("---FILE CONVERT NOT FOUND IN MUSCLE FUNCTION---")
        print(naamCONVERT)


if __name__ == '__main__':
    x = int(input("Hoeveel iteraties wil je doen? "))
    for i in range(x):
        naamHMMOutput, naamALNOutput, naamACS, naamMUSCLE, naamCONVERT  = naamGeneratorOutput(i)
        naamHMMInput, naamALNInput, naamMUSCLEin = naamGeneratorInput(i)
        naamTBL = "TBL" + str(i)
        #print(naamHMM, naamALN)
        if i == 0:
            naamALNInput = "pfam_alignment.txt"
        else:
            naamALNInput = naamMUSCLEin

        print(naamALNInput, naamMUSCLE, naamMUSCLEin)

        hmm_build(naamHMMOutput, naamALNInput, i)

        hmm_search(naamALNOutput, naamHMMInput, i, naamTBL)

        time.sleep(3)

        get_acs(naamTBL, naamACS)

        time.sleep(3)

        get_fasta(naamACS, naamCONVERT)

        time.sleep(3)

        print(naamMUSCLEin, naamMUSCLE, naamCONVERT)

        MUSCLE(naamCONVERT, naamMUSCLE)

        print("----------ITERATION " + str(i) + " DONE----------")