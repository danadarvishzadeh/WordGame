import mysql.connector

"""
checking words with database for more correct ones
and writing new words to it
"""

cnx = mysql.connector.connect(user='dana', database='word_game')
cursor = cnx.cursor()


def TableCheck():
    pass

def InsertToDB():
    pass


def Altering():
    pass


def Searching():
    pass



cursor.close()
cnx.close()