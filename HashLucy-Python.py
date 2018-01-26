from html.parser import HTMLParser
import queue
from threading import Thread
import csv

links = ['https://medium.com']
seen = []


def crawl(links):
    counter = 0
    threads = []
    seen = set(links)
    class WebParser(HTMLParser):
        links = list()
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        self.links.extend([attr[1]])

    def get_link(url):
        import requests
        page = requests.get(url)
        parser = WebParser()
        parser.feed(str(page.content))
        return parser.links

    def spider():
        while True:
            try:
                print ('In Spider')
                x = links.pop()
                a = get_link(x)
                links.extend(a)
                #print(links)
                with open('links.csv', 'w') as csvfile:
                            fieldnames = ['links']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            for l in links:
                                writer.writerow({'links': l})
                seen.add(x)
            except:
                break


    print('doing threads')
    while threads:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

    while len(threads) < 5 and links:
        print('Making Thread:' + str(counter))
        thread = Thread(name = counter, target = spider)
        counter+=1
        thread.start()
        threads.append(thread)

crawl(links)
