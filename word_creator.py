import re


"""
this script will clean the first hand produced words 
to make it easier for correctness cheking
"""

# dump words to a file named after requested length of word 
# with number at the end of file
def WordDump(name, words):
    name = str(name) + '.txt'
    count = 0
    with open(name, 'w') as f:
        for word in words:
            f.write('{},'.format(word))
            count += 1
        f.write(str(count))

# making a list of words and handing them to the WordDump function
def WordMaker(length, letters):
    regular_words = letters.copy()
    special_words = ['کک', 'شش', 'سس', 'تتر', 'تتو']
    new_words = []
    counter = 1
    while counter != length:
        for i in regular_words:
            for j in letters:
                if i == j:
                    continue
                if i[-1] == 'ا' and j == 'ا':
                    continue
                if i[-1] == 'و' and j == 'و':
                    continue
# bacause of the persian language specefic instructions
                if len(i) > 3:
                    if re.findall(r"[^اوی]{4}", i+j):
                        continue
                    else:
                        new_words.append(i+j)
                else:
                    new_words.append(i+j)
                
        regular_words = new_words.copy()
        new_words.clear()
        counter += 1
    regular_words += special_words
    return regular_words


