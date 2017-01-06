import time
import requests

i = 0
while True:
    r = requests.get('http://www.google.com');
    f = open('output.txt', 'w')
    f.write('Working: ' + str(i))
    f.write('\nStatus: ' + str(r.status_code))
    i += 1
    time.sleep(1)
