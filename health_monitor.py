#!usr/bin/ python
import interfaces as constant
import subprocess
from subprocess import call
import redis
import time

def get_health(interface):
  server = redis.Redis("localhost")
  interface = 'ping:'+interface #To make it compatible with our table names
  delay_data = server.zrevrange(interface,0,60) #Returns the latest 60 ping values
  #server.remrangebyrank(interface, 0, 10)     #Removes the oldest 10 ping values
  up_count = 0
  
  for delay in delay_data:
    if(delay[-1] != "0"):
      up_count = up_count+1
  print up_count 
  return up_count

def active_interfaces(interfaces, threshold):
  active_interfaces = []
  
  for interface in interfaces:
    health = get_health(interface)
    if(health >= threshold):
      active_interfaces.append(interface)
  
  return active_interfaces
      
def main():
  allowed_interfaces = constant.INTERFACES
  while 1:
    currently_active = active_interfaces(allowed_interfaces, 30)
    print currently_active
    index = 0
    for interface in allowed_interfaces:
      index = index + 1
      if interface in currently_active:
	subprocess.call("ifmetric %s %s" %(interface, str(index)), shell=True, stdout=open("/dev/null", "w"))
      else:
        subprocess.call("ifmetric %s 100" %(interface), shell=True, stdout=open("/dev/null", "w"))
    time.sleep(1)    
      

main()

