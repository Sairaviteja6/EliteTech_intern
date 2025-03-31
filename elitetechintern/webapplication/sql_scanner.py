import requests
from concurrent.futures import ThreadPoolExecutor

SQL_PAYLOADS = ["'", "' OR 1=1 --", '" OR 1=1 --']

class SQLScanner:
    def __init__(self, forms, max_threads=5):
        self.forms = forms
        self.executor = ThreadPoolExecutor(max_threads)

    def test_sql_injection(self):
        futures = []
        for url, form in self.forms:
            futures.append(self.executor.submit(self.scan_form, url, form))

        for future in futures:
            future.result()

    def scan_form(self, url, form):
        for payload in SQL_PAYLOADS:
            data = {}
            for input_tag in form.find_all("input"):
                if input_tag.get("name"):
                    data[input_tag.get("name")] = payload
            
            response = requests.post(url, data=data)
            if "error" in response.text.lower() or "syntax" in response.text.lower():
                print(f"[!] SQL Injection vulnerability found on {url}")
                return
