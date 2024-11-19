import requests

url = "http://www.crazyant.net"

r = requests.get(url)

print(r.status_code)
print(r.headers)
print(r.encoding)
print(r.text)
print(r.cookies)