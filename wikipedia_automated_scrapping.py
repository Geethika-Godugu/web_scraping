import requests
from bs4 import BeautifulSoup

title = str(input('Enter the topic: ')).replace(' ','+')
link='https://www.google.com/search?q=' + title + '+wikipedia'#automating the link: generating link from user input and get data from wikipedia
print(link)
res= requests.get(link)
soup=BeautifulSoup(res.text,'html.parser')

for sp in soup.find_all('div'):#to get the wikipedia link for the given input
    try:
        link=sp.find('a').get('href')
        if ('en.wikipedia.org' in link):#searching using particular string
            print(link)
            break
    except:
        pass
new_link=link[7:].split('&')[0]

res=requests.get(new_link)
soup=BeautifulSoup(res.text,'html.parser')

heading=soup.find('h1').text
corpus=''

for para in soup.find_all('p'):#to get data in a better way ,like data will be divided into paragraphs
    corpus+=para.text
    corpus+= '\n'
corpus=corpus.strip()#removes extra spaces


for i in range(2,400):#data has characters like [1],[2]....[356] so replacing those with nothing
    corpus=corpus.replace('['+str(i)+']','')

fd=open(heading + '.txt', 'w')#writing data in to a txt file
fd.write(corpus)
fd.close()