import urllib2
from urlparse import urljoin

from pysqlite2 import dbapi2 as sqlite

from BeautifulSoup import *


ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self, table, field, value, createnew=True):
        cur = self.con.execute("select rowid from %s where %s='%s'" % (table,field,value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    # Index indv page
    def addtoindex(self, url, soup):
        if self.isindexed(url): return
        print 'Indexing ' + url

        # Get individual words
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # Get URL id
        urlid = self.getentryid('urllist', 'url', url)

        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid, wordid, location) \
                              values (%d,%d,%d)" % (urlid, wordid, i))


    # Extract text from HTML (no tags)
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # Separate words by any non-whitespace char
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!= '']

    # Return true if this url is already indexed
    def isindexed(self, url):
        return False

    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    """
    Starting with a list of pages, do bfs to the given depth
    and indexing pages as we go
    """

    def crawl(self, pages, depth=2):
        pass

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                    soup = BeautifulSoup(c.read())
                    self.addtoindex(page, soup)
                    links = soup('a')
                    for link in links:
                        if ('href' in dict(link.attrs)):
                            url = urljoin(page, link['href'])
                            if url.find("'") != -1: continue
                            url = url.split('#')[0]
                            if url[0:4] == 'http' and not self.isindexed(url):
                                newpages.add(url)
                            linkText = self.gettextonly(link)
                            self.addlinkref(page, url, linkText)
                except:
                    print('Could not open %s' % page)

                self.dbcommit()

            pages = newpages

    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()


if __name__ == '__main__':
    crawler = crawler('searchindex.db')
    crawler.createindextables()

    pages = ['http://www.anandtech.com']
    crawler.crawl(pages)