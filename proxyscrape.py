import requests


def scrape_proxies(timeout):
    url = f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout={timeout}&country=all&ssl=all&anonymity=all'
    response = requests.get(url)
    proxies = response.text.split('\n')
    return proxies
