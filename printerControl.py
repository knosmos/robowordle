from printrun.printcore import printcore
import serial.tools.list_ports
import time

# Baseline values (X, Y) point to lower left corner
X = 79.5
Y = 82.5
Z_UP = 27
Z_DOWN = 22

MARKERS = [
    (196, 370),
    (218, 371),
    (241, 371),
    (265, 370),
    (287, 370),
    (312, 370),
    (334, 372),
    (358, 369),
    (381, 370),
    (403, 370),
    (207, 412),
    (228, 412),
    (252, 413),
    (275, 412),
    (300, 412),
    (324, 414),
    (347, 414),
    (370, 414),
    (395, 414),
    (231, 451),
    (254, 452),
    (278, 453),
    (299, 454),
    (325, 452),
    (347, 452),
    (370, 453),
    (201, 452)
]
MARKER_LABELS = "qwertyuiopasdfghjklzxcvbnm"

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

# Auto home
print("Running auto home...")
p.send_now("G28 X Y Z W")

# Set X, Y, Z to default
print("Moving to ready position...")
set_pos(z=Z_UP)
set_pos(x=X, y=Y)

# Command input
while True:
    try:
        command = input()
        if command == "press":
            set_pos(z=Z_UP)
            set_pos(z=Z_DOWN)
            set_pos(z=Z_UP)
        elif command.isalpha():
            pos = MARKERS[MARKER_LABELS.index(command)]
            pos = conv_printer_coords(pos[0], pos[1])
            set_pos(x=pos[0], y=pos[1])
        else:
            p.send_now(command)
    except KeyboardInterrupt:
        break
    
print("Disconnecting...")
p.disconnect()