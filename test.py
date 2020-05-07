from bs4 import BeautifulSoup
import cfscrape
import os

go = input('Go?')


def start(q):
    i = 1
    while i <= 10:
        images = []
        true_images = []
        site = 'https://gdz.ru/class-7/himiya/gabrielyan-vvodnij-kurs/' + str(q) + '-quest-' + str(i) + '/'
        soup = BeautifulSoup(cfscrape.create_scraper().get(site).content.decode('utf-8'), 'html.parser')
        for k in soup.findAll('img'):
            true_images.append('https:' + k.get('src'))
        try:
            for l in true_images:
                if l[0:40] == 'https://gdz.ru/attachments/images/tasks/':
                    images.append(l)
        except Exception:
            pass
        with open(os.mkdir('C:/Users/PycharmProjects/vk_bot/gdz/class-7/himiya/gabrielyan-vvodnij-kurs/' + str(q) + '-quest-/') + str(i) + '.txt', 'w') as file:
            for j in images:
                file.write(j + '\n')
        i += 1


if go == 'go':
    q = 1
    while q <= 19:
        start(q)
        q += 1
else:
    print('((9(')
