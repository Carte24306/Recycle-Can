import subprocess
import os

# Install required modules
subprocess.call(['apt-get', 'install', 'python3-tk'])  # Install tkinter on Ubuntu
subprocess.call(['pip', 'install', 'paho-mqtt'])
subprocess.call(['pip', 'install', 'gpiod'])

# Delete the script after installation
os.remove(__file__)
