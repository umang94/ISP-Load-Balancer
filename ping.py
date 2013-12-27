#!usr/bin/ python
import interfaces as constant
import subprocess
from subprocess import call, STDOUT
import redis
import re
import time
def ping(ip, interface):
  ret = subprocess.call("ping -c 1 -I %s  %s" % (interface, ip), shell=True, stdout = open("/dev/null", 'w'),stderr = subprocess.STDOUT)
  print ret
  if(ret == 0):
    return "1"
    #with open('output.log', 'r') as content_file:
    #  content = content_file.read()
    #  match = re.search('([\d]*\.[\d]*)/([\d]*\.[\d]*)/([\d]*\.[\d]*)/([\d]*\.[\d]*)', content)
    #  ping_min = match.group(1)
    #  ping_avg = match.group(2)
    #  ping_max = match.group(3)
    #  match = re.search('(\d*)% packet loss', content)
    #  pkt_loss = match.group(1)
    #return ping_min
  else:
    return "0"
def gettime():
  timestamp = int(time.time())
  return timestamp

def main():
  #print gettime()
  server = redis.Redis("localhost")
  interfaces = constant.INTERFACES
  index = 0
  while 1:
    index = 0
    for interface in interfaces:
      tablename = "ping:"+interface
      timestamp = gettime()
      if index%2 == 0:
	data = str(timestamp) + ":" + ping("8.8.8.8", interface)
      else:
	data = str(timestamp) + ":" + ping("8.8.4.4", interface)
      print "Just pinged %s" %(interface)
      server.zadd(tablename, data, timestamp)
      print data, timestamp
      time.sleep(0.5)
      server.zremrangebyrank(tablename, 0, -60)
      index += 1

main()
