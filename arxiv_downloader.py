import requests
from bs4 import BeautifulSoup
import re
import sys


def download_rename_paper(url: str):
    if re.search(r'http[s]?\://arxiv\.org/abs/', url):
        abs_url = url
        pdf_url = url.replace('abs', 'pdf') + '.pdf'
    elif re.search(r'http[s]?\://arxiv\.org/pdf/', url):
        pdf_url = url
        abs_url = url.replace('pdf', 'abs')[:-4]
    else:
        print(f'Not a valid url: {url}')
        return
    
    r = requests.get(abs_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    title = soup.select('h1.title')[0].text[6:]
    filename = title.replace(' ', '_') + '.pdf'
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
    r = requests.get(pdf_url, headers=headers)
    
    with open(filename, mode='wb') as f:
        f.write(r.content)
        
    print(f'Downloaded: {title}')
        
for line in sys.stdin:
    download_rename_paper(line.rstrip())

