import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from datetime import datetime

import subprocess

RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0

font = ImageFont.load_default()

startTimestamp = datetime.timestamp(datetime.now())

while True:

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    cmd = "hostname -I |cut -f 1 -d ' '"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "python3 /home/pi/Stats/cpu_usage.py"
    CPU = str(subprocess.check_output(cmd, shell = True ), "utf-8")
    cmd = "vcgencmd measure_clock arm |cut -f 2 -d '='"
    CPU_clock = int(int(subprocess.check_output(cmd, shell = True )) / 1000000)
    if CPU_clock >= 1000:
        CPU_clock = "CPU Clock: " + str(CPU_clock / 1000) + " GHz"
    else:
        CPU_clock = "CPU Clock: " + str(CPU_clock) + " MHz"
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    cpu_temp = subprocess.check_output(cmd, shell = True )
    cmd = '''echo "$(python3 /home/pi/Stats/AdafruitDHT.py 11 4 |cut -f 2 -d '='|cut -f 1 -d '*')'C"'''
    out_temp = subprocess.check_output(cmd, shell = True )

    draw.text((x, top), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((x, top+9), CPU, font=font, fill=255)
    draw.text((x, top+18), CPU_clock, font=font, fill=255)
    draw.text((x, top+27), str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((x, top+36), str(Disk,'utf-8'), font=font, fill=255)
    draw.text((x, top+45), "Case temp: " + str(out_temp,'utf-8'), font=font, fill=255)
    sec = datetime.timestamp(datetime.now()) - startTimestamp

    if sec < 60:
        uptime = "Uptime: " + str(int(sec)) + "s"
    if sec > 60:
        min = int(sec / 60)
        if ((sec / 60) > 60):
            hod = int((sec / 60) / 60)
            uptime = "Uptime: " + str(hod) + "hod, " + str(int((sec/60)-(60*hod))) + "min"
        else:
            uptime = "Uptime: " + str(min) + "min, " + str(int(sec-(60*min))) + "s" 

    draw.text((x, top+54), uptime, font=font, fill=255)

    disp.image(image)
    disp.display()
