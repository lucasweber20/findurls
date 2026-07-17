import requests
import re
import argparse
import time


DATA = []
REGEX = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--url", help="Set url. Example: -u www.example.com", type=str)
parser.add_argument("-l", "--list", help="Add urls file. Example -u urls.txt", type=str)
parser.add_argument("-o", "--output", help="Save urls in file. Example: -o urls.txt", type=str)

args = parser.parse_args()

def main():

    if args.list:
        file_read = open(args.list).read().splitlines()
        for url in file_read:
            wayback = get_wayback_urls(url)
            commoncrawl = get_commoncrawl_urls(url)
            alienvault = get_alienvault(url)
    else:
        #wayback = get_wayback_urls(args.url)
        #commoncrawl = get_commoncrawl_urls(args.url)
        alienvault = get_alienvault(args.url)

    for host in DATA:
        if args.output:
            with open(args.output, "a") as file:
                file.write(f"{host}\n")
        else:
            with open("urls.txt", "a") as file:
                file.write(f"{host}\n")

def get_wayback_urls(url):
    while True:
        try:
            req = requests.get(f"http://web.archive.org/cdx/search/cdx?url={url}/*&collapse=urlkey").text
            urls = re.findall(REGEX, req)

            for url in urls:
                DATA.append(url)
            return True
        except:
            continue

def get_commoncrawl_urls(url):
    while True:
        try:
            req = requests.get(f"http://index.commoncrawl.org/CC-MAIN-2018-22-index?url={url}/*&output=text").text
            urls = re.findall(REGEX, req)

            for url in urls:
                DATA.append(url)
            return True
        except:
            continue

def get_alienvault(url):
    while True:
        for num in range(1, 50):
            try:
                req = requests.get(f"https://otx.alienvault.com/api/v1/indicators/hostname/{url}/url_list?limit=100&page={num}", timeout=10)
                if "429" in req.status_code:
                    time.sleep(120)
                    req = requests.get(f"https://otx.alienvault.com/api/v1/indicators/hostname/{url}/url_list?limit=100&page={num}", timeout=10)

                req_text = req.text
                urls = re.findall(REGEX, req_text)

                if urls:
                    for url in urls:
                        DATA.append(url)
                else:
                    continue
            except:
                continue
        return True

def get_vtotal_urls(url):
    pass

if __name__ == "__main__":
    main()