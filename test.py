from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost
from lcd import *
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime

# choose the sensor
sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BCM)

# set up the pin
sensor_pin = 25

# update after 5 seconds
while (1):
	# get temp and humidity
	humid, temp = Adafruit_DHT.read_retry(sensor, sensor_pin)
	print ("Temp = {0:0.1f}  Hummidity = {1:0.1f}\n").format(temp, humid)

	# get current time
	currentDT = datetime.datetime.now()
	day = str(currentDT.day)
	month = str(currentDT.month)
	year = str(currentDT.year)
	hour = str(currentDT.hour)
	minute = str(currentDT.minute)
	second = str(currentDT.second)

	# lcd
        lcd_string("Temp: {0}".format(temp), LCD_LINE_1)
        lcd_string("Humid: {0}%".format(humid), LCD_LINE_2)

	# upload to website
	your_blog = Client('http://192.168.43.88/xmlrpc.php', 'ramen', 'ramen')
	myposts=your_blog.call(posts.GetPosts())
	post = WordPressPost()
	post.title = 'Brisbane Weather'
	post.slug='Brisbane_Weather'
	post.content ='''Temperature: {0} Celsius degree
	Humidity: {1}%
	Last updated on {2}/{3}/{4}\t{5}:{6}:{7}'''.format(temp, humid,
	day.rjust(2, '0'), month.rjust(2, '0'), year, hour.rjust(2, '0'),
	minute.rjust(2, '0'), second.rjust(2, '0'))

	#post.id = your_blog.call(posts.NewPost(post))
	post.post_status = 'publish'
	your_blog.call(posts.EditPost(28, post))
	time.sleep(5)
