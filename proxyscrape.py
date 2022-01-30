import requests
from colorama import Fore


def scrape_proxies(timeout, amount):
    url = f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout={timeout}&country=all&ssl=all&anonymity=all&limit={amount}'
    response = requests.get(url)
    proxiez = response.text.split('\n')
    return proxiez


def check_proxy(mode, ip, timeout):
    if mode == 'http' or mode == 'https' or mode == 'socks4' or mode == 'socks5':
        url = 'http://www.google.com/'
        try:
            r = requests.get(url=url, timeout=timeout, proxies={mode: ip})
            if r.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.ProxyError:
            return False
    else:
        print('Invalid proxy mode')


if __name__ == '__main__':
    proxies = scrape_proxies(timeout=5000)
    for proxy in proxies:
        proxy = proxy.strip()
        proxy = 'http://' + proxy
        if check_proxy(mode='http', ip=proxy, timeout=5000):
            print(f'{Fore.GREEN}[+] {Fore.RESET}Working: {proxy}')
        else:
            print(f'{Fore.RED}[-] {Fore.RESET}Not working: {proxy}')
