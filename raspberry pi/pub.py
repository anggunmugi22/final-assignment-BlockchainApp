import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import array
import json
import sys
#library for PZEM-004T V3
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
client=mqtt.Client()
client.connect('192.168.1.14')
print('Connected')
def publish_to_blockchain(t):
    client.publish('Data',str(t))
    print('Data Published to Blockchain')
    #client.disconnect()


# Connect to the slave
serial = serial.Serial(
                       port='/dev/ttyUSB0',
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       xonxoff=0
                      )

master = modbus_rtu.RtuMaster(serial)
master.set_timeout(2.0)
master.set_verbose(True)


while True:
	data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
	power = round((data[3] + (data[4] << 16)) / 10.0,2) # [W]
	print(power)
	#datadummy = 596159691658916935811234123412344564564567897897891111111111113333333333332432523452623256463527364242646281946916492164891269637691659715616579165371695659615969165891693581123412341234456456456789789789111111111111333333333333243252345262325646352736424264628194691649216489126963769165971561657916537169565961596916589169358112341234123445645645678978978911111111111133333333333324325234526232564635273642426462819469164921648912696376916597156165791653716956596159691658916935811234123412344564564567897897891111111111113333333333332432523452623256463527364242646281946916492164891269637691659715616579165371695659615969165891693581123412341234456456456789789789111111111111333333333333243252345262325646352736424264628194691649216489126963769165971561657916537169565961596916589169358112341234123445645645678978978911111111111133333333333324325234526232564635273642426462819469164921648912696376916597156165791653716956596159691658916935811234123412344564564567897897891111111111113333333333332432523452623256463527364242646281946916492164891269637691659715616579165371695659615969165891693581
	#print(datadummy)
	#size = sys.getsizeof(datadummy)
	publish_to_blockchain(power)
	#print(size)
	time.sleep(30)
	