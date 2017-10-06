import os

import requests
from bs4 import BeautifulSoup

from util import BASE_URL, check_directory, login, get_input


class ConversationDownloader:
    def __init__(self, base_url, target_dir, username, password):
        self.base_url = base_url
        self.target_dir = target_dir

        self.session = login(username, password)

    def get_page(self, url):
        response = self.session.get(url)
        return response.text

    def start(self):
        if not check_directory(self.target_dir):
            print("Created directory '{0}'".format(self.target_dir))

        conversation_urls = []

        for number, url in enumerate(self.get_page_urls()):
            print('Getting URLs from page {0}...'.format(number+1))
            conversation_urls += self.get_conversation_urls(url)

        for url in conversation_urls:
            self.download_conversation(url)

        self.session.close()
        print('Done!')

    def get_page_urls(self):
        soup = BeautifulSoup(self.get_page(self.base_url + 'conversation-list'), 'html5lib')
        pagination = soup.find('nav', {'class': 'pagination'})
        pages = int(pagination.get('data-pages'))
        return [BASE_URL + 'conversation-list/?filter=&pageNo={0}&sortField=lastPostTime&sortOrder=DESC'.format(n+1) for n in range(pages)]

    def get_conversation_urls(self, page_url):
        urls = []
        soup = BeautifulSoup(self.get_page(page_url), 'html5lib')
        conversions_list = soup.find('div', {'class': 'messageGroupList'}).find('ol')
        rows = conversions_list.find_all('li', {'class': 'tabularListRow'})
        for row in rows:
            if 'tabularListRowHead' in row.get('class'):
                continue
            url = row.find('ol').find('li', {'class': 'columnSubject'}).find('h3').find('a').get('href')
            urls.append(url)
        return urls

    def download_conversation(self, conversation_url):
        identifier = conversation_url.replace(self.base_url, '').replace('conversation/', '').replace('/', '')
        print('Downloading {0}'.format(identifier))
        html = self.get_page(conversation_url)
        with open(os.path.join(self.target_dir, '{0}.html'.format(identifier)), 'w') as f:
            f.write(html)


def main():
    username = get_input('Username')
    password = get_input('Password', hidden=True)
    target_dir = get_input('Target directory', 'forum_conversations')
    downloader = ConversationDownloader(BASE_URL, target_dir, username, password)
    downloader.start()


if __name__ == '__main__':
    main()
