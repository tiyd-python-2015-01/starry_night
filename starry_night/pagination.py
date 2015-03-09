import re

def parse_link(link):
    regex = r'<(.+?page=(\d+))>; rel="(.+?)"'
    match = re.match(regex, link)
    url, page, rel = match.group(1, 2, 3)
    return rel, int(page), url

class Paginator:
    def __init__(self, resp, page=1):
        link = resp._resp.getheader("link")
        links = [parse_link(link) for link in link.split(", ")]
        self.first = 1
        self.current = page
        self.prev = None
        self.next = None
        self.last = page
        self.links = {}
        for link in links:
            setattr(self, link[0], link[1])
            self.links[link[0]] = link[2]