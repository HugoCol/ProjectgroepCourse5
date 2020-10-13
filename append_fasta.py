from Bio import SeqIO
from sys import argv


def read_fasta(input_fasta, output_fasta):
    """Functie die m.b.v. BioPython een fasta bestand inleest en append
    aan een ander bestand
    :param input_fasta: fasta bestand met sequenties uit de huidige iteratie
    :param output_fasta: fasta bestand met sequeties uit alle iteraties
    :return: geen
    """
    for record in SeqIO.parse(input_fasta, "fasta"):
        with open(output_fasta, "a") as file:
            SeqIO.write(record, file, "fasta")


if __name__ == '__main__':
    read_fasta(argv[1], argv[2])