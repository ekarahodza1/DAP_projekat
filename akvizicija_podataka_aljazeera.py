from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import feedparser
import re
from bs4 import BeautifulSoup

def remove_HTML_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_urls_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    urls = []
    for link in links:
        urls.append('https://balkans.aljazeera.net' + link['href'])

    return urls

def get_text_from_url(url):
  if (re.search('liveblog', url) == None ):  #da izbjegnem liveblog vijesti jer treba drugaciji nacin rada za njih
    feed = feedparser.parse(url)
    try:
        temp = feed['feed']['summary'].split('<p>') # dobavljam sadrzaj jer se on nalazi izmedju <p>
        temp = temp[1:]  #dobijem sadrzaj zajedno sa izvorom ali bez onog pocetka naslov itd
        index = temp[len(temp)-1].index("</p>")
        sadrzaj = ' '.join([str(elem) for elem in temp[:len(temp)-1]])
        sadrzaj += temp[len(temp)-1][:index]
        sadrzaj = remove_HTML_tags(sadrzaj)
        return sadrzaj
    except:
        return None

#get html after vise is clicked click_num times
def get_html(url, click_num=15):
    service = Service(executable_path="C:\\Users\\HP\\Downloads\\chromedriver\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.get(url)

    cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    cookies.click()

    for i in range(click_num):
        button = driver.find_element(By.XPATH, '//*[@id="news-feed-container"]/button')
        button.click()
        driver.implicitly_wait(1.5)
    html_source = driver.page_source
    driver.quit()

    return html_source

def filter_urls(urls):
    remove_about_page = urls[17:-28] #remove irrelevant urls like about page, cookies, etc
    filtered = list(set(remove_about_page)) #remove duplicates
    return filtered

news = ['https://balkans.aljazeera.net/news/balkan/', 'https://balkans.aljazeera.net/news/world/', 'https://balkans.aljazeera.net/news/culture/',
        'https://balkans.aljazeera.net/news/technology/', 'https://balkans.aljazeera.net/news/economy/']

urls = []
for url in news:
    print(url)
    html = get_html(url)
    links = get_urls_from_html(html)
    filtered_urls = filter_urls(links)
    urls.append(filtered_urls)

with open("urls.txt", "w") as output:
    output.write(str(urls))

text = []
for news in urls:
  for url in news:
    t = get_text_from_url(url)
    if (t != None):
      text.append(t)

with open("news.txt", "w", encoding="utf-8") as output:
    output.write(str(text))