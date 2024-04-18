import serial.tools.list_ports  # which ports are existing

ports = serial.tools.list_ports.comports()  # which ports are ready
serialInst = serial.Serial()  # creation of Arduino serial destination

portList = []  # creation of empty list

for onePort in ports:  # scan one by one
    portList.append(str(onePort))  # write to the list
    print(str(onePort))  # print the list

val = input("select Port: COM")  # ask user value

for x in range(0, len(portList)):  # execute ports times
    if portList[x].startswith("COM" + str(val)):  # find which is the user port
        portVar = "COM" + str(val)  # connect Arduino with serial destination
        print(portList[x])  # print out

serialInst.baudrate = 9600  # baudrate setting
serialInst.port = "COM" + str(val)  # connect-define virtual port
serialInst.open()

while True:  # continue reading until serial data will stop
    if serialInst.in_waiting:
        packet = serialInst.readline()
        print(packet.decode('utf').rstrip('\n'))
