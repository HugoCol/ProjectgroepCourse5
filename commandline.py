# import subprocess

# subprocess.Popen(["gnome-terminal", "-e", "myscript.sh"])
import time
import os
os.system('ls -l')
os.system('pwd')
time.sleep(2)

os.chdir('/home/hugo/course5/programs/')
os.system('pwd')
os.system('ls -l')
os.system('muscle -in ./Desktop/Hemaglutininfamilie40.fa -out '
          './Desktop/muscleoutput40.afa')