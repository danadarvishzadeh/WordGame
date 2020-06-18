import requests
from bs4 import BeautifulSoup

"""
this script will check each word's correctness
from an online dictionary
"""

word_list = ['تاذل', 'لب', 'اقا', 'لفب', 'بسیی', 'کباب', 'محمد']


with requests.Session() as s:
    for word in word_list:
        url = 'http://www.vajehyab.com/?q=' + word + '&f=dehkhoda'
        response = s.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        answer = soup.find('div', attrs={'class':'fieldset'})
        if answer:
            if answer.text.strip() == 'جست‌وجوی دقیق':
                print(word, 'is word')
            else:
                print(word, 'not a word')
        else:
            print(word, 'not a word')