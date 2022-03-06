from printrun.printcore import printcore
import serial.tools.list_ports
import time, sys
from config import *

# Set up commlink
ports = serial.tools.list_ports.comports()
print("available ports:")
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

# If there is more than one port, ask user to choose
if len(ports) > 1:
    port = input("select port> ")
    if port == "": port = sorted(ports)[0][0]
else:
    ports = []
    while len(ports) == 0:
        ports = serial.tools.list_ports.comports()
    port = ports[0][0]
p = printcore(port, 115200)
time.sleep(1)
print("Connected to " + port)

def set_pos(x = False, y = False, z = False):
    message = "G1 "
    if x: message += f"X{x}"
    if y: message += f"Y{y}"
    if z: message += f"Z{z}"
    p.send_now(message)

def conv_printer_coords(x, y):
    size = 600
    # Get in terms of lower left corner
    y = size - y
    # Scale - actual size is 150mm 
    x /= size/150
    y /= size/150
    # Add offset
    x += X
    y += Y
    return x, y

def press():
    set_pos(z=Z_UP)
    set_pos(z=Z_MID)
    set_pos(z=Z_DOWN)
    set_pos(z=Z_MID)
    set_pos(z=Z_UP)

def typeLetter(letter):
    pos = MARKERS[MARKER_LABELS.index(letter)]
    pos = conv_printer_coords(pos[0], pos[1])
    set_pos(x=pos[0], y=pos[1])
    press()

def typeWord(word):
    # Type letter
    for letter in word:
        typeLetter(letter)
        time.sleep(2)
    typeLetter("/")
    # Move out of the way
    set_pos(x=1, y=1, z=50)

# Auto home
def home():
    print("Running auto home...")
    p.send_now("G28 X Y Z W")
    time.sleep(10)

# Set X, Y, Z to default
def ready_position():
    print("Moving to ready position...")
    set_pos(z=Z_UP)
    set_pos(x=X, y=Y)

def disconnect():
    print("Disconnecting...")
    p.disconnect()

# Command input
if __name__ == "__main__":
    if len(sys.argv) == 1:
        home()
    ready_position()
    while True:
        try:
            command = input()
            if len(command.split()) == 1:
                typeWord(command)
            else:
                p.send_now(command)
        except KeyboardInterrupt:
            break
    disconnect()