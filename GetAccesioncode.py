import os
from sys import argv


def accesionlistmaker(file_in):
    """
    Filter the information Get the accesioncode from the TSV
    """

    with open(file_in) as tsvfile:
        counter = 0

        accesiecode_lijst = []
        for row in tsvfile:
            counter += 1
            # vanaf dit stuk pak je niet de headers in de lijst
            if counter >= 4:
                e = row.replace('-', '')
                try:
                    a = e.split()
                    # extra filter over de accessiecodes
                    if a[0] != '#':
                        accesiecode_lijst.append(a[0])
                except IndexError:
                    pass
    return accesiecode_lijst


def filewriting(accesionlist, file_out):
    """
    Get a list, write to file
    """
    f = open(file_out, "w+")
    for accesioncode in accesionlist:
        f.write(accesioncode + '\n')
    f.close()


if __name__ == '__main__':
    """
    This function gets the accesioncodes from a muscle output
    terminal command: python3 GetAccesioncode.py file_in file_out.txt
    De argumenten die je meegeeft worden gebruikt als files name
    misschien niet helemaal ideaal omdat dit ook filepaths zijn
    """

    file_in = argv[1]
    file_out = argv[2]
    accesioncodelist = accesionlistmaker(file_in)
    filewriting(accesioncodelist, file_out)
