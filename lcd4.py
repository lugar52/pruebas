
#!/usr/bin/python

import time
import sys
import lcd3 as lcd

def main():
  lcd.lcd_init()
  
  largo = len(sys.argv)
  print(largo)
  while True:
    if largo == 1 or largo > 3:
      time.sleep(1)
    elif largo == 3:
      lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
      lcd.lcd_string(sys.argv[1],2)
      lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
      lcd.lcd_string(sys.argv[2],2)
      time.sleep(3)
    else:
      lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
      lcd.lcd_string(sys.argv[1],2)
      time.sleep(3)
      
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string(time.strftime("%d-%m-%Y"),1)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string(time.strftime("%H:%M:%S"),3)
    time.sleep(3)
    
      
if __name__ == '__main__':
  main()
