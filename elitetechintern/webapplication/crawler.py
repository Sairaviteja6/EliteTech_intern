import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

class Crawler:
    def __init__(self, base_url, max_threads=5):
        self.base_url = base_url
        self.visited = set()
        self.forms = []
        self.links = []
        self.executor = ThreadPoolExecutor(max_threads)

    def get_links(self, url):
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(self.base_url, a_tag["href"])
                if link not in self.visited and self.base_url in link:
                    self.links.append(link)
        except:
            pass

    def get_forms(self, url):
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            for form in soup.find_all("form"):
                self.forms.append((url, form))
        except:
            pass

    def crawl(self):
        self.visited.add(self.base_url)
        self.get_links(self.base_url)

        # Use multi-threading for faster crawling
        futures = []
        for link in self.links:
            futures.append(self.executor.submit(self.get_forms, link))
            futures.append(self.executor.submit(self.get_links, link))

        # Wait for all threads to finish
        for future in futures:
            future.result()

        return self.links, self.forms
