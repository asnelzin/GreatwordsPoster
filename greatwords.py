import lxml.html
import urllib.request

QUOTE_URL = 'http://greatwords.ru/random/'
XPATH_QUOTE = '//*[@id="content"]/p/text()'
XPATH_AUTHOR = '//*[@id="content"]/h2/a/text()'


def get_quote():
    page = urllib.request.urlopen(QUOTE_URL)
    doc = lxml.html.document_fromstring(page.read())
    
    quote = doc.xpath(XPATH_QUOTE)[0][:-1]
    author = doc.xpath(XPATH_AUTHOR)[0]
    return quote, author


def find_cut(quote):
    max_cut = 0
    for i in range(len(quote)):
        if (quote[i] == ' ') and (max_cut < i) and (i <= 134) and (len(quote) - (i + 1) > 30):
            max_cut = i
    return max_cut


def get_statuses():
    statuses = []
    while True:
        quote, author = get_quote()
        if (len(quote) + len(author) + 17) <= 140:
            statuses = ['«%s». %s. #greatwords' % (quote, author)]
            break
        if (len(quote) + len(author) + 26) <= 280:
            cut = find_cut(quote)
            first_half, second_half = quote[:cut], quote[cut+1:]
            if (len(first_half) + 6 <= 140) and (len(second_half) + len(author) + 20 <= 140):
                statuses = ['«%s...».' % first_half, '«...%s». %s. #greatwords' % (second_half, author)]
                break
    return statuses