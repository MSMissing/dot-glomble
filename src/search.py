import html.parser
import http.client
import urllib.parse

def from_items(items):
    d = {}
    for item in items:
        d[item[0]] = item[1]
    return d

class HTMLSearcher(html.parser.HTMLParser):
    result = []
    progress = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == 'card mb-3 border-0':
                        self.progress = 1
        if tag == 'a' and self.progress == 1:
            a = from_items(attrs)
            self.result.append('https://glomble.com' + a['href'])
            self.progress = 0

def search(query: str):
    print('Establishing connection with glomble.com...')
    connection = http.client.HTTPSConnection('glomble.com')
    print('Connected. Sending query...')
    connection.request('GET', f'/?query={urllib.parse.quote_plus(bytes(query, 'utf-8'))}')

    response = connection.getresponse()
    if response.status != 200:
        raise ConnectionError(f'Expected HTTP response 200 OK, but got {response.status} {response.reason}')
    print('Got response from glomble.com.')

    document = str(response.read(), 'utf-8')
    connection.close()

    print('Parsing videos...')
    searcher = HTMLSearcher()
    searcher.feed(document)
    return searcher.result

