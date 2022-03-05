from printrun.printcore import printcore
p = printcore('COM5',115200)

while True:
    command = input()
    p.send_now(command)
    
p.disconnect()