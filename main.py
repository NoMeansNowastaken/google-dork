from colorama import Fore
import requests
from bs4 import BeautifulSoup
import proxyscrape as ps


def patched():
    print(f'''{Fore.RED}[!]{Fore.RESET} Dork is patched, try another''')
    main()


def statuscheck(engin):
    req = requests.get(url='https://raw.githubusercontent.com/NoMeansNowastaken/google-dork/main/status.json')
    json = req.json()
    if engin == '1' and json['Google']:
        return True
    elif engin == '2' and json['DuckDuckGo']:
        return True
    elif engin == '3' and json['Bing']:
        return True
    elif engin == '4' and json['Yandex']:
        return True
    elif engin == '5' and json['Nintendo']:
        return True
    else:
        return False


def main():
    engine = input(
        f"[{Fore.RED}*{Fore.RESET}] Choose Search Engine\n\n[{Fore.RED}1{Fore.RESET}] Google\n[{Fore.RED}2{Fore.RESET}] DuckDuckGo\n[{Fore.RED}3{Fore.RESET}] Bing\n[{Fore.RED}4{Fore.RESET}] Yandex\n[{Fore.RED}5{Fore.RESET}] Nintendo\n[{Fore.RED}99{Fore.RESET}] Exit\n\n[{Fore.RED}*{Fore.RESET}] ")
    if not statuscheck(engine):
        print(f'''{Fore.RED}[!]{Fore.RESET} Engine is patched, try another''')
        main()
    dork = input(f'''{Fore.BLUE}Enter a dork to use:{Fore.RESET} ''')
    proxy = input(f'''{Fore.BLUE}Use Proxies? (y/n):{Fore.RESET} ''')
    if proxy == 'y':
        try:
            with open('proxies.txt', 'r') as f:
                proxies = f.readlines()
                if proxies == '':
                    print('Scraping proxies...')
                    proxies = ps.scrape_proxies(3000, 30)
        except FileNotFoundError:
            print('Scraping proxies...')
            proxies = ps.scrape_proxies(3000, 30)
    save = input(f'''{Fore.CYAN}Would you like to save to a file?: {Fore.RESET}''')
    if save == 'y':
        overwrite = input(f'''{Fore.CYAN}Would you like to overwrite current results?: {Fore.RESET}''')
        if overwrite == 'y':
            try:
                with open('results.txt', 'w') as f:
                    f.write('')
            except FileNotFoundError:
                print(f'{Fore.LIGHTRED_EX}[*] No results to overwrite')
    rmdupe = input(f'''{Fore.CYAN}Would you like to remove duplicate results?: {Fore.RESET}''')
    try:
        pages = int(input(f'''{Fore.CYAN}How many pages would you like to search?: {Fore.RESET}'''))
    except ValueError:
        print(f'''{Fore.LIGHTRED_EX}[*] {Fore.RESET}Invalid input, defaulting to 20 pages''')
        pages = 20
    if save == 'y' or save == 'Y' or save == 'yes' or save == 'Yes' or save == 'YES':
        save = True
    if dork == '':
        dork = 'intitle:”index of/” “cfdb7_uploads”'
    if proxy == 'y':
        print(f'''{Fore.BLUE}[*] {Fore.RESET} Loaded {len(proxies)} proxies''')
    print(f'''{Fore.GREEN}[*]{Fore.RESET} Dork: {dork}''')
    print(f'''{Fore.GREEN}[*]{Fore.RESET} Searching...''')
    if engine == '1':
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
                        result = i.get('href').split('=')[1].split('&')[0]
                        print(f'''{Fore.GREEN}[+]{Fore.RESET} Found: {result}''')
                        if save:
                            with open('results.txt', 'a') as f:
                                f.write(f'{result}\n')
            else:
                print(f'''{Fore.RED}[!]{Fore.RESET} Something went wrong!''')
                print(r.status_code)
    elif engine == '2':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        url = f'https://duckduckgo.com/html?q={dork}'
        if proxy == 'y':
            proxy = {'http': proxies[1 % len(proxies)].strip()}
            r = requests.get(url, proxies=proxy, headers=headers)
        else:
            r = requests.get(url, headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            thing = soup.find_all('a')
            for i in thing:
                try:
                    if 'http' in i.get('href'):
                        result = i.get('href')
                        print(f'''{Fore.GREEN}[+]{Fore.RESET} Found: {result}''')
                        if save:
                            with open('results.txt', 'a') as f:
                                f.write(f'{result}\n')
                except TypeError:
                    pass
        else:
            if r.status_code == 418:
                patched()
            else:
                print(f'''{Fore.RED}[!]{Fore.RESET} Something went wrong! Error: {r.status_code}''')
    elif engine == '5':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        for b in range(pages):
            url = f'https://www.nintendo.com/search/#category=all&page={b}&query={dork}'
            if proxy == 'y':
                proxy = {'http': proxies[1 % len(proxies)].strip()}
                r = requests.get(url, proxies=proxy, headers=headers)
            else:
                r = requests.get(url, headers=headers)
            if r.status_code == 200:
                html = r.text
                soup = BeautifulSoup(html, 'html.parser')
                thing = soup.find_all('a')
                for i in thing:
                    result = i.get('href')
                    if 'https://' in result:
                        pass
                    elif 'http://' in result:
                        pass
                    else:
                        print(f'''{Fore.GREEN}[+]{Fore.RESET} Found: {result}''')
                        if save:
                            with open('results.txt', 'a') as f:
                                f.write(f'{result}\n')
            else:
                print(f'''{Fore.RED}[!]{Fore.RESET} Something went wrong! Error: {r.status_code}''')
    elif engine == '99':
        exit()
    if rmdupe == 'y' or rmdupe == 'Y' or rmdupe == 'yes' or rmdupe == 'Yes' or rmdupe == 'YES':
        print(f'''{Fore.GREEN}[*]{Fore.RESET} Removing duplicates...''')
        dupes = 0
        with open('results.txt', 'r') as f:
            lines = f.readlines()
        with open('results.txt', 'w') as f:
            for line in lines:
                if line not in lines[lines.index(line) + 1:]:
                    f.write(line)
                else:
                    dupes += 1
        print(f'''{Fore.GREEN}[*]{Fore.RESET} Removed {dupes} duplicates''')
    with open('results.txt', 'r') as f:
        lines = f.readlines()
    input(f'''{Fore.GREEN}[*]{Fore.RESET} Finished! Press Enter to exit...''')


if __name__ == '__main__':
    main()
