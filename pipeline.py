import os

def naamGeneratorOutput(i):
    naamHMM = "IT" + str(i) + ".hmm"
    naamALN = "IT" + str(i) + ".sto"
    naamMUSCLE = "MUSCLE" + str(i)
    naamCONVERT = "CONV" + str(i)
    naamACS = "ACS" + str(i) + ".txt"
    return naamHMM, naamALN, naamACS

def naamGeneratorInput(i):
    naamHMM = "IT" + str(i) + ".hmm"
    naamALN = "IT" + str(i - 1) + ".sto"
    return naamHMM, naamALN


def hmm_build(naamOutput, naamALN, i):
    os.system("hmmbuild {} {}".format(naamOutput, naamALN))



def hmm_search(naamOutput, naamHMM, i, naamTBL):
    os.system("hmmsearch --tblout {} -A {} --cpu 16 {} database/nr".format(naamTBL, naamOutput, naamHMM))


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


def get_fasta(naamACS):
    os.system("python3 converter.py {} output".format(naamACS))


def MUSCLE():
    os.system("muscle -in output.fa -out outfasta -clwstrict")

if __name__ == '__main__':
    x = int(input("Hoeveel iteraties wil je doen? "))
    for i in range(x):
        naamHMMOutput, naamALNOutput, naamACS = naamGeneratorOutput(i)
        naamHMMInput, naamALNInput = naamGeneratorInput(i)
        naamTBL = "TBL" + str(i)
        #print(naamHMM, naamALN)
        if i == 0:
            naamALNInput = "pfam_alignment.txt"
        hmm_build(naamHMMOutput, naamALNInput, i)
        hmm_search(naamALNOutput, naamHMMInput, i, naamTBL)
        get_acs(naamTBL, naamACS)
        get_fasta(naamACS)
        MUSCLE()
        print("----------ITERATION " + str(i) + " DONE----------")