import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_file_signatures'
baseurl = 'https://filesignatures.net/index.php?page=all&order=EXT&alpha=All&currentpage='
page = requests.get(url)
all_extensions = []

with open('signatury.txt', 'w+') as file:
    for i in range(18):
        url = f'{baseurl}{i+1}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(id='innerTable')
        extensions = table.find_all('td', {'width': '147'})
        signatures = table.find_all('td', {'width': '236'})
        length = len(extensions)
        for i in range(length):
            signature = signatures[i].string
            extension = extensions[i].string
            print(extension)
            if extension not in all_extensions:
                all_extensions.append(extension)
            file.write(f'{signature} - {extension}\n')

with open('extensions.txt', 'w+') as file:
    for i in all_extensions:
        file.write(f'{i}\n')
