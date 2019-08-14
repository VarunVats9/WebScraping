# import dependencies
from bs4 import BeautifulSoup
import requests
import re
import operator
import sys
from tabulate import tabulate
from stop_words import get_stop_words
import json


# get_word_list
def get_word_list(url):
    word_list = []

    # get the data in lxml format
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    for text in soup.findAll('p'):
        if text.text is None:
            continue

        content = text.text
        words = content.lower().split()

        for word in words:
            cleaned_word = clean_word(word)
            if len(cleaned_word) > 0:
                word_list.append(cleaned_word)

    return word_list


def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word


def create_frequency_table(word_list):
    words_dict = {}
    for word in word_list:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    return words_dict


def remove_stop_words(sorted_word_list):
    stop_words = get_stop_words('en')
    temp_list = []

    for key, value in sorted_word_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list


# get data from wikipedia
wikipedia_api_link = "http://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "http://en.wikipedia.org/wiki/"

if len(sys.argv) < 2:
    print("Enter valid string.")
    exit()

# get search word
search_query = sys.argv[1]

if len(sys.argv) > 2:
    search_mode = True
else:
    search_mode = False

# create url
url = wikipedia_api_link + search_query

try:
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))

    # format the data
    wikipedia_page_tag = data['query']['search'][0]['title']

    # create the new url
    url = wikipedia_link + wikipedia_page_tag
    print("Fetching the URL: " + url)

    # create table of word counts
    page_word_list = get_word_list(url)
    page_word_count = create_frequency_table(page_word_list)
    sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)

    # remove the stop words
    if search_mode:
        sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

    # sum the total words
    total_words = 0
    for key, value in sorted_word_frequency_list:
        total_words = total_words + value

    # get the top 20 words
    if len(sorted_word_frequency_list) > 20:
        sorted_word_frequency_list = sorted_word_frequency_list[:20]

    # create our final list, word + frequency + percentage
    final_list = []
    for key, value in sorted_word_frequency_list:
        percentage = float(value * 100) / total_words
        final_list.append([key, value, round(percentage, 4)])

    print_headers = ['Word', 'Frequency', 'Frequency Percentage']

    # print the table with tabulate
    print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

# throw an exception in case it breaks
except requests.exceptions.Timeout:
    print("The server didn't respond. Please, try again later.")
