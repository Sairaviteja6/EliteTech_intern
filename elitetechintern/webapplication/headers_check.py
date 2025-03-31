import requests

SECURITY_HEADERS = ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection"]

class HeaderScanner:
    def __init__(self, url):
        self.url = url

    def check_headers(self):
        response = requests.get(self.url)
        missing_headers = [header for header in SECURITY_HEADERS if header not in response.headers]

        if missing_headers:
            print(f"[!] Missing security headers on {self.url}: {', '.join(missing_headers)}")
        else:
            print(f"[+] All security headers are present on {self.url}")
