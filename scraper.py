import requests
from bs4 import BeautifulSoup
import concurrent.futures
import threading
"""
this script will check each word's correctness
from an online dictionary
"""

word_list = []

print_lock = threading.Lock()

def WordCheck(word):
    url = 'http://www.vajehyab.com/?q=' + word + '&f=dehkhoda'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    answer = soup.find('div', attrs={'class':'fieldset'})
    with print_lock:
        if answer:
            if answer.text.strip() == 'جست‌وجوی دقیق':
                print(word, 'is word')
            else:
                print(word, 'not a word')
        else:
            print(word, 'not a word')

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(WordCheck, word_list)