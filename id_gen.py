import random
import string
import mysql.connector

def uid_gen():
    """Functie om een uniek ID te genereren en te checken of deze al aanwezig
    is in de database
    :return: uid
    """
    try:
        t = True
        while t:
            uid = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in
                range(12))
            conn = mysql.connector.connect(host='hydron.io',
                                           user='course5',
                                           password='yGVBJW3rniUd8uw1',
                                           db='course5')
            cursor = conn.cursor()
            SQL = "select tax_id from taxonomy where tax_id like \'{}\'".\
                format(uid)
            cursor.execute(SQL)
            uid_test = None
            for i in cursor:
                uid_test = i[0]
            if uid_test is not None:
                t = True
            else:
                t = False
            conn.close()
            return uid
    except ValueError:
        print('Onverwachte value')
    except ModuleNotFoundError:
        print("De benodigde module is niet gevonden")