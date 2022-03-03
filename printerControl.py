from printrun.printcore import printcore
p = printcore('COM3',115200) on Windows

while True:
    command = input()
    p.send_now(command)
    
p.disconnect()