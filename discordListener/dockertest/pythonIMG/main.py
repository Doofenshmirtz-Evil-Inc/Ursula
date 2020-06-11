import requests
import time
print("Hello World from PY")

inp = "fuck yes"
def sendToAPI(value):
    print("sending API... "+value)
    url = 'http://js-test:8080'
    print('EEEIM AMAA MIGONNA GFET EM')
    r = requests.get(url + '/')
    print(r.text)
    x = requests.post(url + '/add', data=value)
    print(x.text)

# I WILL FORCE A BUILD
time.sleep(1)
sendToAPI(inp)