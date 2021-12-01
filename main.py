import requests
from config import cookie
from bs4 import BeautifulSoup


with open('old_links.txt', 'r') as file:
    old_links_file = file.read()

s = requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': cookie

}


def get_page(headers=headers):
    res = s.get('https://qna.habr.com/', headers=headers)
    return res.text


def parse(src):
    soup = BeautifulSoup(src, 'lxml')
    old_links = []
    items = soup.find('ul', class_='content-list').find_all('li',
                                                            class_='content-list__item')
    new_links = 0
    res = {'questions': [], 'new_questions': [], 'new_questions_num': 0}
    for item in items:
        title = item.find('h2', class_='question__title').find('a')
        title_text = title.text.strip()
        link = title.get('href')
        r = {
            'title': title_text,
            'link': link
        }
        if link not in old_links_file:
            new_links += 1
            old_links.append(link)
            res['new_questions'].append(r)
        res['questions'].append(r)
        res['new_questions_num'] = new_links

    with open('old_links.txt', 'a') as file:
        for link in old_links:
            file.write(link + '\n')

    return res


def main():
    p = get_page()
    print(parse(p))
    # with open('site.html', 'w', encoding='utf-8') as file:
    #     file.write(p)


if __name__ == '__main__':
    main()
