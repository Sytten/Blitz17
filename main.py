import time

i = 0
while True:
   f = open('output.txt', 'w')
   f.write('Working: ' + str(i))
   i += 1
   time.sleep(1) 
