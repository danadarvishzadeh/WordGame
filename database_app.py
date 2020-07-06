import mysql.connector
from mysql.connector import errorcode
import re
"""
checking words with database for more correct ones
and writing new words to it
"""

cnx = mysql.connector.connect(user='USERNAME', password='PASSWORD',
        database='WordGame', auth_plugin='mysql_native_password'
    )
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
    str_lters = "(\w*[^{},]{{1,}}\w*.)".format(''.join(letters))
    for letter in letters:
        like_stmt += f"'%{letter}%' OR name LIKE "
    like_stmt = like_stmt[:-14]
    cursor.execute(f"SELECT name FROM WORDS WHERE name LIKE {like_stmt} AND len='{length}' ORDER BY reps")
    word_list = [word[0] for word in cursor]
    word_list = ','.join(word_list)
    answers = re.sub(str_lters, '', word_list).strip().split(',')
    return answers


def closing(cnx, cursor):
    cursor.close()
    cnx.close()