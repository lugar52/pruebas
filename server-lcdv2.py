#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import lcd3 as lcd
import time


import RPi.GPIO as GPIO
# from keypad import keypad

sel = selectors.DefaultSelector()
salida_lcd = ''

# Initialize keypad
GPIO.setwarnings(False)
kp = lcd.keypad(columnCount = 4)
seq = ''   
digit = ''

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            mivalor = data.outb
            print("Estoy aqui " + str(mivalor, encoding='ascii', errors='ignore'))
            show_external_msg_lcd(mivalor)
            salida_lcd = mivalor    
            sent = sock.send(mivalor)  # Should be ready to write
            data.outb = data.outb[sent:]


def show_external_msg_lcd(Mivar):
    # Mivar = variable que contiene el valor a mostrar en el display
    # Inicializa el display
    #lcd.lcd_init()
    
    largo = len((str(Mivar, encoding='ascii', errors='ignore')))
    mimsg = str(Mivar, encoding='ascii', errors='ignore')
    lin = mimsg.split(":")
        
    if len(lin) == 2:
        linea1 = lin[0]
        linea2 = lin[1]
    else:
        linea1 = lin[0]
        linea2 = ''

    if largo > 0:
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(linea1,2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string(linea2,2)
        time.sleep(3)
    else:
        pass

def p_lcd(Mivar, var2):
    # Mivar = variable que contiene el valor a mostrar en el display
    # var2 indica desde donde se llama la funcion; 0 señala que es la llamada de entrada y mantiene el reloj en el display
    #                                               1 indica qie la llamada es por un valor externo que se debe desplegar en el display
    # Inicializa el display
    #lcd.lcd_init()
    if var2 == None:
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(time.strftime("%d-%m-%Y"+ "    V2"),2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string(time.strftime("%H:%M:%S"),2)
    else:
        seq = str(Mivar)
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(seq,2)
        
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string('',1)
                
host, port = 'localhost', 65439
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
lcd.lcd_init()
flag = 0
msg = ""
timeout = 0.1
keycounter = 0
try:
    while flag == 0:
        
        events = sel.select(timeout)
        timeout = 0.1
        if events:
            flag == 1
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
                    flag = 0
        else:
            digit = kp.getKey()
            if digit is not None:
                if digit == '#':
                    msg = ""
                else:
                    msg = msg + str(digit)
                    p_lcd(msg, digit)
                    keycounter = 0
                    timeout = 0.5
                #time.sleep(0.5)
            else:
                if msg == "":
                    p_lcd(' ',digit)
                else:
                    keycounter += 1
                    if keycounter > 100:
                        msg = ""
            
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()