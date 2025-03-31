import argparse
from crawler import Crawler
from sql_scanner import SQLScanner
from xss_scanner import XSSScanner
from headers_check import HeaderScanner

def main():
    parser = argparse.ArgumentParser(description="Multi-threaded Web Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target website URL")
    args = parser.parse_args()

    print("[+] Crawling website...")
    crawler = Crawler(args.url)
    links, forms = crawler.crawl()

    print("[+] Running SQL Injection scan...")
    sql_scanner = SQLScanner(forms)
    sql_scanner.test_sql_injection()

    print("[+] Running XSS scan...")
    xss_scanner = XSSScanner(forms)
    xss_scanner.test_xss()

    print("[+] Checking security headers...")
    header_scanner = HeaderScanner(args.url)
    header_scanner.check_headers()

    print("[✔] Scan completed!")

if __name__ == "__main__":
    main()
