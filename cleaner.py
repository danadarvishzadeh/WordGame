import re

"""
this script will clean the first hand produced words 
to make it easier for correctness cheking
"""


persian_letters = 'ابپتثجچحخدذرزژسشصضعغطظفقکگلمنوهی'

def WordMaker(level, letters):
    regular_words = letters.copy()
    special_words = ['کک', 'شش', 'سس', 'تتر', 'تتو']
    new_words = []
    count = 0
    while count != level:
        for i in regular_words:
            for j in letters:
                if i == j:
                    continue
                if len(i) > 3:
                    if re.findall(r"[^اوی]{4}", i+j):
                        continue
                    else:
                        new_words.append(i+j)
                else:
                    new_words.append(i+j)
                
        regular_words = new_words.copy()
        new_words.clear()
        count += 1
    regular_words += special_words
    return regular_words

def WordDump(_name, words):
    name = _name + '.txt'
    with open(name, 'w') as fout:
        for i in words:
            fout.write('{}, '.format(i))

