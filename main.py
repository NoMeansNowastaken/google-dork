from colorama import Fore
import requests
from bs4 import BeautifulSoup
import proxyscrape


def main():
    dork = input(f'''{Fore.BLUE}Enter a dork to use (default is intitle:”index of/” “cfdb7_uploads”):{Fore.RESET} ''')
    proxy = input(f'''{Fore.BLUE}Use Proxies? (y/n):{Fore.RESET} ''')
    if proxy == 'y':
        try:
            with open('proxies.txt', 'r') as f:
                proxies = f.readlines()
                if proxies == '':
                    print('No proxies found in proxies.txt')
                    print('Scraping proxies')
                    proxies = proxyscrape.scrape_proxies(7000)
        except FileNotFoundError:
            print('proxy file not found')
            print('Scraping proxies')
            proxies = proxyscrape.scrape_proxies(7000)
    save = input(f'''{Fore.CYAN}Would you like to save to a file?: {Fore.RESET}''')
    overwrite = input(f'''{Fore.CYAN}Would you like to overwrite current results?: {Fore.RESET}''')
    if overwrite == 'y':
        try:
            with open('results.txt', 'w') as f:
                f.write('')
        except FileNotFoundError:
            print(f'{Fore.RED}[!] No results to overwrite')
    rmdupe = input(f'''{Fore.CYAN}Would you like to remove duplicate results?: {Fore.RESET}''')
    pages = input(f'''{Fore.CYAN}How many pages would you like to search?: {Fore.RESET}''')
    try:
        pages = int(pages)
    except ValueError:
        print(f'''{Fore.RED}[!] {Fore.RESET}Invalid input, defaulting to 10 pages''')
        pages = 10
    if save == 'y' or save == 'Y' or save == 'yes' or save == 'Yes' or save == 'YES':
        save = True
    if dork == '':
        dork = 'intitle:”index of/” “cfdb7_uploads”'
    if proxy == 'y':
        print(f'''{Fore.BLUE}[*] {Fore.RESET} Loaded {len(proxies)} proxies''')
    print(f'''{Fore.GREEN}[+]{Fore.RESET} Dork: {dork}''')
    print(f'''{Fore.GREEN}[+]{Fore.RESET} Searching...''')
    for a in range(pages):
        url = f'https://www.google.com/search?q={dork}&start={a * 10}'
        if proxy == 'y':
            proxy = {'http': proxies[a % len(proxies)].strip()}
            r = requests.get(url, proxies=proxy)
        else:
            r = requests.get(url)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            thing = soup.find_all('a')
            for i in thing:
                if 'http' in i.get('href') and 'google' not in i.get('href'):
                    temp = i.get('href')
                    temp = temp.split('=')
                    temp = temp[1]
                    temp = temp.split('&')
                    result = temp[0]
                    print(f'''{Fore.GREEN}[+]{Fore.RESET} Found: {result}''')
                    if save:
                        with open('results.txt', 'a') as f:
                            f.write(f'{result}\n')
        else:
            print(f'''{Fore.RED}[!]{Fore.RESET} Something went wrong!''')
            print(r.status_code)
    if rmdupe == 'y' or rmdupe == 'Y' or rmdupe == 'yes' or rmdupe == 'Yes' or rmdupe == 'YES':
        print(f'''{Fore.GREEN}[+]{Fore.RESET} Removing duplicates...''')
        dupes = 0
        with open('results.txt', 'r') as f:
            lines = f.readlines()
        with open('results.txt', 'w') as f:
            for line in lines:
                if line not in lines[lines.index(line)+1:]:
                    f.write(line)
                else:
                    dupes += 1
        print(f'''{Fore.GREEN}[+]{Fore.RESET} Removed {dupes} duplicates''')
    with open('results.txt', 'r') as f:
        lines = f.readlines()
    print(f'''{Fore.GREEN}[+]{Fore.RESET} Finished!''')


if __name__ == '__main__':
    main()
