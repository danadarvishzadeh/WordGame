import mysql.connector
from mysql.connector import errorcode
import re
"""
checking words with database for more correct ones
and writing new words to it
"""

cnx = mysql.connector.connect(user='dana', database='WordGame')
cursor = cnx.cursor()

def wordreader(filename):
    with open(filename, 'r') as f:
        f = f.read().strip().split(',')
        word_list = f[:-1].copy()
    return word_list



def inserttodb(filename):
    word_list = wordreader(filename)
    for word in word_list:
        insert = f"INSERT INTO WORDS(name, reps, len) VALUES('{word}', 1, {len(word)})"
        cursor.execute(insert)
    cnx.commit()



def addrepeatation(word):
    cursor.execute(f"call addreps('{word}')")
    cnx.commit()




def searching(length, letters):
    like_stmt = ''
    str_lters = ''.join(letters)
    for letter in letters:
        like_stmt += f'%{letter}% AND name LIKE '
    like_stmt = like_stmt[:-15]
    cursor.execute(f'SELECT name FROM WORDS WHERE len={length} AND name LIKE {} ORDER BY reps')
    word_list = [word for word in cursor]
    word_list = ','.join(word_list)
    answers = re.sub(f'(\w*[{str_lters}]\w*.)', '', word_list).strip().split(',')
    return answers


def closing(cnx, cursor):
    cursor.close()
    cnx.close()