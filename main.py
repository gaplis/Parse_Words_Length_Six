import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from pathlib import Path

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36',
}


def get_source_html(url, file_path):
    print('[...] Loading source html...')

    get = requests.get(url, headers=headers)
    soup = BeautifulSoup(get.text, features='lxml')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())


def get_urls_from_source(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        src = file.read()

    print('[...] Get divs from class "words_group"...')

    soup = BeautifulSoup(src, features='lxml')
    item_divs = soup.find_all('div', class_='words_group')

    urls = []
    words = []
    for div in item_divs:
        print('[...] Find "href" in div...')

        try:
            item_url = div.find('div', class_='words_group-header').find('a').get('href')

            urls.append(f'https://vfrsute.ru{item_url}')

            print(f'[...] Get "href": {item_url}...')
        except Exception as _ex:
            print('[---] "href" not found, find words...')

            items_word = div.find('ul').find_all('li', class_='words_group-item')
            for li in items_word:
                word = li.find('a').text.replace(' ', '').replace('\n', '')
                words.append(word.lower())

                print(f'[...] Get word: {word}...')

    with open('data/items_urls.txt', 'w', encoding='utf-8') as file:
        print(f'[+++] Write urls in: data/items_urls.txt...')

        for item in urls:
            file.writelines(f'{item}\n')

    with open('data/words.txt', 'w', encoding='utf-8') as file:
        print(f'[+++] Write words in: data/words.txt...')

        for word in words:
            file.writelines(f'{word}\n')


def get_source_from_urls(file_path):
    print(f'[...] Read urls in: {file_path}/items_urls.txt...')

    with open(f'{file_path}/items_urls.txt', 'r', encoding='utf-8') as file:
        urls = file.read().split('\n')[:-1]

    for i, url in enumerate(urls, start=1):
        num = f"0{i}" if i < 10 else i
        path = f'{file_path}/letters_html/file_letter_{num}.html'

        print(f'[+++] Write html in: {path}...')

        get_source_html(url, path)

        rand = randint(3, 7)
        print(f'[-!-] Success! Sleep {rand} seconds...')
        sleep(rand)


def get_words_from_html(file_path):
    folder = Path(f'{file_path}/letters_html')

    words = []
    for i in range(1, len(list(folder.iterdir())) + 1):
        num = f"0{i}" if i < 10 else i
        with open(f'{file_path}/letters_html/file_letter_{num}.html', 'r', encoding='utf-8') as file:
            html = file.read()

        print(f'[...] Reading data from {file_path}/letters_html/file_letter_{num}.html...')

        soup = BeautifulSoup(html, features='lxml')
        item_li = soup.find_all('li', class_='words_group-item')

        print(f'[...] Find "li" in html...')

        if len(item_li) > 0:
            for li in item_li:
                print(f'[...] Find word in "li"...')

                word = li.find('a').text.replace(' ', '').replace('\n', '')
                words.append(word.lower())

                print(f'[+++] Word {word} found and appended...')
        else:
            print(f'[---] "li" not found. Find "p"...')

            find_p = soup.find('div', class_='main').find('div', class_='container') \
                .find('div', class_='wrapper').find_all('p')

            for p in find_p:
                print(f'[...] Find word in "p"...')

                word = p.text.replace(' ', '').replace('\n', '')
                if len(word) == 6:
                    words.append(word.lower())

                    print(f'[+++] Word {word} found and appended...')

    print(f'[+++] Writing words in {file_path}/words.txt...')

    with open(f'{file_path}/words.txt', 'a', encoding='utf-8') as file:
        for word in words:
            file.writelines(f'{word}\n')


def main():
    # get_source_html('https://vfrsute.ru/сканворд/слово-из-6-букв/', 'data/source_page.html')
    # get_urls_from_source('data/source_page.html')
    # get_source_from_urls('data')
    get_words_from_html('data')


if __name__ == '__main__':
    print('[...] Start parsing...')
    main()
    print('[!!!] Success parsing!')
