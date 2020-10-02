import os
from sys import argv
def Accesionfilewriter(file_in,file_out):
    """
    Filter the information Get the accesioncode from the
    """

    f = open(file_out,"w+")
    with open(file_in) as tsvfile:
        counter = 0
        # alleen de accessiecodes
        accesiecode_lijst = []
        for row in tsvfile:

            e = row.replace('-', '')
            counter += 1
            # vanaf dit stuk pak je niet de headers in de lijst
            if counter >= 4:
                try:
                    a = e.split()

                    # extra filter over de accessiecodes
                    if a[0] != '#':
                        accesiecode_lijst.append(a[0])
                        f.write(a[0] + '\n')

                except IndexError:
                    pass
        f.close()
    return accesiecode_lijst

if __name__ == '__main__':
    """
    This function gets the accesioncodes from a muscle output
    terminal command: python3 GetAccesioncode.py file_in file_out.txt
    """

    file_in = argv[1]
    file_out = argv[2]
    Accesionfilewriter(file_in,file_out)