#!/usr/bin/python
  
#import
import commands

def main():
  string1 = 'Vicente'
  string2 = 'Garrido'
  string3 = '/home/pi/lcd/pruebas/lcd3.py ' + string1 + ' ' + string2
  print(string3)
  
  result=commands.getoutput(string3)

  string1 = 'Matilde'
  string2 = 'Garrido' 
  string3 = '/home/pi/lcd/pruebas/lcd3.py ' + string1 + ' ' + string2
  print(string3)
  
  result=commands.getoutput(string3)
    
if __name__ == '__main__':
  main()
