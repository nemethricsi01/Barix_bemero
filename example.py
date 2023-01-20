from lcd_lib import LCD_1inch3
import machine
import time
from machine import UART
from machine import Timer
from machine import Pin
machine.freq()          # get the current frequency of the CPU
machine.freq(200000000) # set the CPU frequency to 240 MHz
uart = UART(0, 9600)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

LCD = LCD_1inch3()
LCD.fill(LCD.black)

LCD.write_text('Size 1',x=0,y=0,size=1,color=LCD.green)
LCD.write_text('Size 2',x=0,y=50,size=2,color=LCD.white)
LCD.write_text('Size 3',x=0,y=100,size=3,color=LCD.white)

LCD.show()
time.sleep(1)
LCD.fill(LCD.black)
LCD.show()
adc = machine.ADC(26)
buf = bytearray(20)
size = 0
prelltime = 5
prelltimer = 0
laststate = 0
actstate = 0
ledstate = 0
def handleInterrupt(timer):#timer interrupt handler
    global prelltimer
    if prelltimer > 0:
        prelltimer = prelltimer -1
    
tim = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))#start of timer
tim.init(period=10, mode=Timer.PERIODIC, callback=handleInterrupt)#timer interrupt for display multiplexing
keyA = Pin(15,Pin.IN,Pin.PULL_UP)
led = Pin(25,Pin.OUT)    
laststate = keyA.value()
actstate = laststate
while True:
    actstate = keyA.value()
    
    if actstate != laststate:
        prelltimer = 5
        
        while prelltimer != 0:
            actstate = keyA.value()
            if actstate != laststate:
                prelltimer = 5
                laststate = actstate
                
        if laststate == 0:
            led.value(ledstate)
            ledstate = ledstate ^1
    
    LCD.fill_rect(0,0,240,30,LCD.black)
    LCD.write_text('adc: %.2fV'%( ( adc.read_u16()>>4 ) * (3.3/4096) ),x=0,y=10,size=2,color=LCD.green)
    #uart.write('adc:%d\n\r'%(adc.read_u16()))   # write the 3 characters
    if uart.any() != 0:
        size = uart.any()
        uart.readinto(buf,size)
        if (buf[0] == 68) and (buf[1] == 83):
            LCD.fill_rect(0,50,240,30,LCD.black)
            LCD.write_text('lerak',0,50,2,LCD.green)
            
        if (buf[0] == 68) and (buf[1] <= 57) and (buf[1] >= 48):
            LCD.fill_rect(0,50,240,30,LCD.black)
            out_string = buf.decode('utf-8')
            LCD.write_text('hivas:'+out_string,0,50,2,LCD.green)
            
        LCD.fill_rect(0,90,240,30,LCD.black)
        out_string = buf.decode('utf-8')
        LCD.write_text(out_string,0,90,2,LCD.green)    
        print(buf[1])
        buf = bytearray(20)
        
    LCD.show()
    pass
    
        
