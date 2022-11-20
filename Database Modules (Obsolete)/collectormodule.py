import sys
sys.path.append(r"D:\Perso\DEV\SQL-Dev-Tool")

import datamodule as data
import urlmodule as url
import SQL as SQL

URLS = url.generator()

print(URLS[0])
def DISCOS(URLS) :
    dico = []
    for i in range(1):
        URL = URLS[i]
        try:
            dico = data.disco(URL)
        except IndexError:
            pass

        connexion = SQL.create_connection(r"/DICOS/DICO_" + str(i) + ".sqlite")

        SQL.execute_modify_query(SQL.create_table("DICO_" + str(i),
                                                  ["Mot", "Longueur", "Definition"],
                                                  ["TEXT", "INTEGER", "TEXT"]),
                                 connexion)

        SQL.execute_modify_query(SQL.create_values("DICO_" + str(i), dico),
                                 connexion)


DISCOS(URLS)

