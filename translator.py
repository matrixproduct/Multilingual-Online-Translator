import requests, sys
from bs4 import BeautifulSoup
from contextlib import redirect_stdout


def get_translation(lan1, lan2, word):
    url = 'https://context.reverso.net/translation/'
    url += lan1.lower() + '-' + lan2.lower() + '/' + word
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 404:
        print(f'Sorry, unable to find {word}')
        exit()
    if r.status_code != 200:
        print('Something wrong with your internet connection')
        exit()

    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.find_all(lambda tag: 'title' in tag.attrs and '<em class=\'translation\'' in tag['title'])
    translations = []
    for row in rows:
        soup_title = BeautifulSoup(row['title'], 'html.parser')
        translations.append(soup_title.select('em', class_='translation')[0].get_text())
    rows = soup.find_all(lambda tag: tag.name == 'span' and 'class' in tag.attrs and tag['class'] == ['text'] and len(tag.contents) == 3)
    examples = [row.get_text().strip().strip("\'\"") for row in rows]
    return translations, examples


def print_translation(lan, translations, examples, num):
    print(f'\n{lan} Translations:')
    print(*translations[:num], sep='\n')
    print(f'\n{lan} Examples:')
    _ = [print(s + '\n') if i % 2 else print(s + ':') for i, s in enumerate(examples[:num * 2])]


def print_all(lan1):
    for lan2 in languages[1:]:
        if lan2 != lan1:
            translations, examples = get_translation(lan1, lan2, word)
            print_translation(lan2, translations, examples, 1)


languages = ['All', 'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
                 'Portuguese', 'Romanian', 'Russian', 'Turkish']

# print('Hello, you\'re welcome to the translator. Translator supports:')
# _ = [print(i + 1, ". ", lan, sep='') for i, lan in enumerate(languages[1:])]
# lan1 = languages[int(input('Type the number of your language:\n'))]
# lan2 = languages[int(input("Type the number of a language you want to translate to or '0' "
#                            "to translate to all languages:\n"))]
# word = input('Type the word you want to translate:\n').lower()

args = sys.argv
lan1, lan2, word = args[1].capitalize(), args[2].capitalize(), args[3]
for lan in (lan1, lan2):
    if lan not in languages:
        print(f'Sorry, the program doesn\'t support {lan.lower()}')
        exit()

if lan2 != 'All':
    translations, examples = get_translation(lan1, lan2, word)
    print_translation(lan2, translations, examples, 5)
else:
    print_all(lan1)
    with open(word + '.txt', 'w', encoding="utf-8") as f:
        with redirect_stdout(f):
            print_all(lan1)





