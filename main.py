import urllib.request
from bs4 import BeautifulSoup
import re
import csv


BASE_URL = 'https://www.kinopoisk.ru/top/navigator/m_act%5Bgenre%5D/28/order/rating'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Movie name', 'User rating', 'IMDb rating'))
        for project in projects:
            writer.writerow((project['title'], project['kino'], project['imdb']))


def page_count(html):
    soup = BeautifulSoup(html, "html.parser")
    page = soup.find('div', class_='pagesFromTo').text
    string_find = str(page)
    ans = ''
    for i in range(len(string_find)):
        if string_find[i] == '—':
            for j in range(i+1, len(string_find)):
                if ord(string_find[j]) >= 48 and ord(string_find[j]) <= 58:
                    ans += (string_find[j])
                else:
                    break
    return int(ans)


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('div', class_='tenItems')
    rows = table.find_all('div', class_='item _NO_HIGHLIGHT_')
    projects = []
    prog = re.compile('\d+\.+\d{2,}')

    for row in rows:
        cols = row.find_all('div', class_='name')
        cols1 = row.find_all('div', class_='numVote')
        cols2 = row.find_all(text=re.compile('IMDb'))
        # print(cols.find_all('div', class_='name'))
        m = prog.findall(str(cols2))
        j = prog.findall(str(cols1))
        if (len(m) <= 0):
            m.append(-1)
        projects.append({
            'title': cols[0].a.text,
            'kino': j[0],
            'imdb': m[0]
        })
    return projects


def main():
    # parse(get_html('https://www.kinopoisk.ru/top/navigator/m_act%5Bgenre%5D/3/order/rating/#results'))
    pg = page_count(get_html(BASE_URL + '/#results'))
    projects = []
    for i in range(1, pg+1):
        projects.extend(parse(get_html(BASE_URL + '/pages/' + str(i) + '/#results')))
        print('Parsing {}%'.format(i * 100 // pg))
    save(projects, 'projects.svc')
    # for i in projects:
    #    print(i)


if __name__ == '__main__':
    main()
