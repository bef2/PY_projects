import time
import urllib.request
import urllib.error

def uptime_bot(url):
    while True:
        try:
            conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(f'HTTPError: {e.code} для {url}')
        except urllib.error.URLError as e:
            print(f'URLError: {e.code} для {url}')
        else:
            print(f'{url} поднят')
        time.sleep(5)

if __name__ == '__main__':
    url = 'https://www.reg.ru'
    uptime_bot(url)
