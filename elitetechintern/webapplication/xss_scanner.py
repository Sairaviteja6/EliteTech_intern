import requests
from concurrent.futures import ThreadPoolExecutor

XSS_PAYLOADS = ['<script>alert("XSS")</script>', '" onmouseover="alert(1)"']

class XSSScanner:
    def __init__(self, forms, max_threads=5):
        self.forms = forms
        self.executor = ThreadPoolExecutor(max_threads)

    def test_xss(self):
        futures = []
        for url, form in self.forms:
            futures.append(self.executor.submit(self.scan_form, url, form))

        for future in futures:
            future.result()

    def scan_form(self, url, form):
        for payload in XSS_PAYLOADS:
            data = {}
            for input_tag in form.find_all("input"):
                if input_tag.get("name"):
                    data[input_tag.get("name")] = payload

            response = requests.post(url, data=data)
            if payload in response.text:
                print(f"[!] XSS vulnerability found on {url}")
                return
