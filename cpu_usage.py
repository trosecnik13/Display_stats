import psutil
import subprocess

cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
cpu_temp = subprocess.check_output(cmd, shell = True )

print("CPU Load: " + str(psutil.cpu_percent(interval=1)) + "% " + str(cpu_temp, 'utf-8'))