import smbus
import time


I2C_ADDR  = 0x27 # dung lenh sudo i2cdetect -y 1 ban se thay dia chi cua module lcd la 0x27
LCD_WIDTH = 16   # so ki tu tren 1 dong

LCD_CHR = 1 # Gui ki tu
LCD_CMD = 0 # Gui lenh

LCD_LINE_1 = 0x80 # dia chi RAM dong 1
LCD_LINE_2 = 0xC0 # dia chi RAM dong 2


LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# delay
E_PULSE = 0.0005
E_DELAY = 0.0005

#bus = smbus.SMBus(0)  # Pi Rev 1 ban su dung dong nay
bus = smbus.SMBus(1) # Pi Rev 2 ban su dung dong nay

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # ban xem lai nhung lenh co ban o Buoc 2
  lcd_byte(0x32,LCD_CMD) # 
  lcd_byte(0x06,LCD_CMD) # 
  lcd_byte(0x0C,LCD_CMD) # 
  lcd_byte(0x28,LCD_CMD) # 
  lcd_byte(0x01,LCD_CMD) # 
  time.sleep(E_DELAY)

# gui 1 byte xuong LCD
def lcd_byte(bits, mode):
	bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
	bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
	#che do 4 bits: gui byte cao truoc byte thap sau
	# byte cao
	bus.write_byte(I2C_ADDR, bits_high)
	lcd_toggle_enable(bits_high)

	# byte thap
	bus.write_byte(I2C_ADDR, bits_low)
	lcd_toggle_enable(bits_low)

# dua chan E len cao roi thap de truyen du lieu di
def lcd_toggle_enable(bits):
	bus.write_byte(I2C_ADDR, (bits | ENABLE))
	time.sleep(E_PULSE)
	bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
	time.sleep(E_DELAY)

# gui chuoi ki tu xuong LCD
def lcd_string(message,line):
	message = message.ljust(LCD_WIDTH," ")
	lcd_byte(line, LCD_CMD)
	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

lcd_init()
